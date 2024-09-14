import os
import sqlite3

def init_db():
    if not os.path.exists(os.getenv('DATA_PATH')): os.mkdir(os.getenv('DATA_PATH'))
    conn = sqlite3.connect(f"{os.getenv('DATA_PATH')}tracked_accounts.db")
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS user (id TEXT PRIMARY KEY, username TEXT, lastest_tweet TEXT);
        CREATE TABLE IF NOT EXISTS channel (id TEXT PRIMARY KEY, server_id TEXT);
        CREATE TABLE IF NOT EXISTS notification (user_id TEXT, channel_id TEXT, role_id TEXT, enabled INTEGER DEFAULT 1, FOREIGN KEY (user_id) REFERENCES user (id), FOREIGN KEY (channel_id) REFERENCES channel (id), PRIMARY KEY(user_id, channel_id));
    """)
    conn.commit()
    conn.close()