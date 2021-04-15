import requests

from streamlit import secrets
from requests_oauthlib import OAuth1


endpoint_mentions = 'https://api.twitter.com/2/tweets/search/recent?query=to:MyTweetFlow&expansions=author_id&since_id={}'
endpoint_answer = 'https://api.twitter.com/1.1/statuses/update.json'
headers = {'authorization': 'Bearer {}'.format(secrets['token'])}


def get_mentions(since_id):
    answer = requests.get(endpoint_mentions.format(since_id), headers=headers).json()
    if 'data' not in answer:
        return []
    tweets = [(tweet['id'], tweet['author_id']) for tweet in answer['data']]
    users = {user['id']: user['username'] for user in answer['includes']['users']}

    result = []

    for id, author_id in tweets:
        result.append((id, users[author_id]))

    return result


def send_answer(text, tweet_id):
    data = {
        'status': f'{text}',
        'in_reply_to_status_id': f'{tweet_id}'
    }
    requests.post(endpoint_answer, data=data, auth=OAuth1(secrets['key'],
                                                          secrets['secret_key'],
                                                          secrets['access'],
                                                          secrets['secret_access']))
