import sqlite3

DB_FILE = "../data/database.db"


def is_valid_login(username: str, password: str) -> bool:
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?;", (username, password))
    return not c.fetchone() is None

