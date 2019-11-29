import sqlite3
import atexit

DB_FILE = "data/database.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()


def does_username_exist(username: str) -> bool:
    return c.execute("SELECT COUNT(username) FROM users WHERE username = ?", (username,)).fetchone()[0] == 1


def is_valid_login(username: str, password: str) -> bool:
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?;", (username, password))
    return not c.fetchone() is None


def create_account(username: str, password: str):
    c.execute("INSERT INTO users(username, password, balance) VALUES (?, ?, 1000)", (username, password))
    db.commit()

def rickandmortydb(id: int, full_name: str, image_link: str):
    c.execute("INSERT INTO rickandmorty(id, full_name, image_link) VALUES (?, ?, ?)", (id, full_name, image_link))
    db.commit()

def rickandmorty_getinfo(id: int):
    # this function takes a random id and returns a list containing the name and image link for a character from rick and morty
    info = list(c.execute("SELECT full_name, image_link FROM rickandmorty WHERE id = ?;", (id, )))
    return info


def pokemon_type_info() -> list:
    """
    :return: List of tuple of name, double damage to, half damage to and no damage to
    """
    return c.execute("SELECT * FROM pokemon_types").fetchall()


def pokemon_info() -> list:
    """
    :return: List of tuple of name, number of types, first type, second type, and image. First and second type can be identical
    """
    return c.execute("SELECT * FROM pokemon").fetchall()


def update_balance(username: str, new_balance: int):
    c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
    db.commit()


def get_balance(username: str) -> int:
    return c.execute("SELECT balance FROM users WHERE username = ?", (username,)).fetchone()[0]


def currency_to_MAWDollars(amount: float, currency: str) -> int:
    """
    1 MAWDollar = $1 USD
    User balance will NEVER contain cents, only whole dollars.
    Rounding down to nearest integer.
    """
    ratio = c.execute("SELECT ratio FROM currency_rates WHERE name = ? ", (currency,)).fetchone()[0]
    return int(amount / ratio)


def MAWDollars_to_currency(amount: int, currency: str) -> float:
    """
    1 MAWDollar = $1 USD
    Do no round down to nearest integer.
    """
    ratio = c.execute("SELECT ratio FROM currency_rates WHERE name = ? ", (currency,)).fetchone()[0]
    return amount * ratio


def close_db():
    db.commit()
    db.close()

atexit.register(close_db)
