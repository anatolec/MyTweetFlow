import sqlite3

conn = sqlite3.connect('../my_tweet_flow.db')
c = conn.cursor()

try:
    c.execute("DROP TABLE user_metrics")
    conn.commit()
except:
    pass

c.execute('''CREATE TABLE user_metrics
             (user_id text, screen_name text, tweets_per_hour real, rt_ratio real, latest_access date, latest_update date)''')

conn.commit()
conn.close()