import my_tweet_flow
import time

from my_tweet_flow import get_db_connection
from datetime import datetime


def run():
    db_conn = get_db_connection()
    c = db_conn.cursor()
    while True:
        since_id = c.execute("SELECT TWEET_ID FROM LATEST_TWEET").fetchall()[0][0]

        mentions = my_tweet_flow.get_mentions(since_id)

        print(f"Found {len(mentions)} mentions")
        for tweet_id, username in mentions:
            contributors = my_tweet_flow.get_tweet_flow_contributors(username, max_results=3, with_percentages=False)
            tph = my_tweet_flow.get_total_tweet_flow(username)

            text = produce_text(username, tph, contributors)

            my_tweet_flow.send_answer(text, tweet_id)
            c.execute("UPDATE LATEST_TWEET SET TWEET_ID = ?", (tweet_id,))
            c.execute("INSERT INTO USER_RESULTS VALUES (?, ?, ?, ?)", (username, 0, tph, datetime.now()))
            db_conn.commit()
        time.sleep(10)


def produce_text(username, tph, contributors, max=3):
    text = \
        f"""Hi @{username} !

You should get on average {round(tph)} tweets per hour and here are your first {max} contributors :
"""
    for i in range(max):
        text += \
            f"""
@{contributors[i][1]} ({round(contributors[i][2])} tweets per hour)        
"""
    text += \
        """
Get more insights at mytweetflow.com !
"""

    return text
