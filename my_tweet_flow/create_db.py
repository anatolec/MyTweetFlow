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

c.execute('''
CREATE TABLE "latest_tweet" (
	"tweet_id"	INTEGER
)''')

c.execute('''
CREATE TABLE "user_metrics" (
	"user_id"	text NOT NULL,
	"screen_name"	text,
	"tweets_per_hour"	real,
	"rt_ratio"	real,
	"latest_access"	date,
	"latest_update"	date NOT NULL,
	PRIMARY KEY("user_id")
)''')

c.execute('''
CREATE TABLE "user_results" (
	"username"	TEXT,
	"user_id"	TEXT,
	"tph"	REAL
)''')
conn.commit()
conn.close()