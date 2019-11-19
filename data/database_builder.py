import sqlite3

db = sqlite3.connect("database.db")
c = db.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
password TEXT,
balance INTEGER
)""")

db.commit()
db.close()
