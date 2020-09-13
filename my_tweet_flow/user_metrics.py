import requests

from datetime import datetime, timezone
from my_tweet_flow.params import *
from my_tweet_flow import get_db_connection


endpoint_following = 'https://api.twitter.com/1.1/friends/ids.json?screen_name={}'
endpoint_tweets = 'https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={}&count={}&exclude_replies=true'
headers = {'authorization': 'Bearer {}'.format(token)}


def get_following_list(username):
    return [str(i) for i in requests.get(url=endpoint_following.format(username), headers=headers).json()['ids']]


def get_user_metrics(user_id, depth=200):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT screen_name, tweets_per_hour, rt_ratio, latest_update FROM user_metrics WHERE user_id=?", (user_id,))
    results = c.fetchmany()
    now = datetime.now()
    if len(results) == 1:
        latest_update = datetime.fromisoformat(results[0][3])
        if (now - latest_update).days < refresh_days:
            screen_name, tph, rt_ratio, latest_update = results[0]
            c.execute("UPDATE user_metrics SET latest_access = ? WHERE user_id=?", (now, user_id))
            conn.commit()
            return screen_name, tph, rt_ratio
        else:
            screen_name, tph, rt_ratio = query_user_metrics(user_id, depth=depth)
            c.execute("""
            UPDATE user_metrics 
            SET latest_access = ?,
            latest_update = ?,
            tweets_per_hour = ?, 
            screen_name = ?,
            rt_ratio = ?
            WHERE user_id=?
            """, (now, now, tph, screen_name, rt_ratio, user_id))
            conn.commit()
            return screen_name, tph, rt_ratio
    if len(results) == 0:
        screen_name, tph, rt_ratio = query_user_metrics(user_id, depth=depth)
        c.execute("""
        INSERT INTO user_metrics 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, screen_name, tph, rt_ratio, now, now))
        conn.commit()
        return screen_name, tph, rt_ratio


def query_user_metrics(user_id, depth=200):
    latest_tweets = requests.get(url=endpoint_tweets.format(user_id, depth), headers=headers).json()

    if 'error' in latest_tweets:
        return 'Not authorized.', 0, 0

    tweets = len(latest_tweets)

    if tweets < 10:
        return 'Too few tweets', 0, 0

    screen_name = latest_tweets[0]['user']['screen_name']

    rts = 0

    for tweet in latest_tweets:
        if tweet['text'][:2] == 'RT':
            rts += 1

    rt_ratio = rts/tweets

    datetime_first_tweet = datetime.strptime(latest_tweets[-1]['created_at'], '%a %b %d %H:%M:%S %z %Y')
    now = datetime.now(timezone.utc)
    td = now - datetime_first_tweet
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    total_hours = days * 24 + hours + remainder / 3600

    tph = 2 * tweets / total_hours

    return screen_name, tph, rt_ratio


def get_total_tweet_flow(username):
    total = 0
    for user_id, screen_name, tph, rt_ratio in get_tweet_flow_contributors(username, with_percentages=False):
        total += tph
    return total


def get_tweet_flow_contributors(username, with_percentages=True, max_results=100):
    following_list = get_following_list(username)
    contributors = []
    total_tph = 0
    for user_id in following_list:
        screen_name, tph, rt_ratio = get_user_metrics(user_id)
        contributors.append((user_id, screen_name, tph, rt_ratio))
        total_tph += tph
    contributors.sort(key=lambda tup: -tup[2])

    if with_percentages:
        result = []
        for user_id, screen_name, tph, rt_ratio in contributors:
            result.append((user_id, screen_name, tph, tph/total_tph, rt_ratio))

        return result[:max_results]

    return contributors[:max_results]
