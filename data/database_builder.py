import sqlite3

db = sqlite3.connect("data/database.db")
c = db.cursor()

# This is the owner of website information
# Stores balance of website (user's lost money goes here)
c.execute("""
CREATE TABLE IF NOT EXISTS admin(
balance INTEGER
)""")

c.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
balance INTEGER
)""")

c.execute("""
CREATE TABLE IF NOT EXISTS rickandmorty(
full_name TEXT,
image_link TEXT
)""")

c.execute("""
CREATE TABLE IF NOT EXISTS pokemon(
name TEXT PRIMARY KEY,
number_types INTEGER,
first_type TEXT,
second_type TEXT,
image TEXT
)""")

c.execute("""
CREATE TABLE IF NOT EXISTS pokemon_types(
name TEXT PRIMARY KEY,
double_damage_to TEXT,
half_damage_to TEXT,
no_damage_to TEXT
)""")

db.commit()
db.close()
