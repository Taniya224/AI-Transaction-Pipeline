import sqlite3

conn = sqlite3.connect("jobs.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    status TEXT,
    result TEXT
)
""")

conn.commit()