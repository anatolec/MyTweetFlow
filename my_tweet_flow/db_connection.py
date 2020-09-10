import sqlite3
import pkg_resources

db_name = pkg_resources.resource_filename('my_tweet_flow', "my_tweet_flow.db")

def get_db_connection():
    conn = sqlite3.connect(db_name)
    return conn