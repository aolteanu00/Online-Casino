import sqlite3

db = sqlite3.connect("database.db")
c = db.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
balance INTEGER
)""")

c.execute("""
CREATE TABLE IF NOT EXISTS rickandmorty(
id INTEGER,
full_name TEXT,
image_link TEXT
)""")

db.commit()
db.close()
