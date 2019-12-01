from urllib.request import Request, urlopen
import sqlite3
import json
from datetime import datetime
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_and_store_exchanges():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    request = Request(url, headers=headers)
    response = urlopen(request).read()
    data = json.loads(response)

    retrieved_info = dict()
    retrieved_info["time_last_updated"] = data["time_last_updated"]
    # Stores an array of tuple (str currency name, float ratio)
    retrieved_info["rates"] = data["rates"]

    with open("data/currency_exchange.json", 'w') as file:
        print("Caching currency exchange")
        json.dump(retrieved_info, file)


def enter_database():
    # detect types to allow for automatic conversion of sqlite TIMESTAMP to python datetime
    connection = sqlite3.connect("data/database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = connection.cursor()

    now = datetime.now()
    currency_last_updated = c.execute("SELECT last_updated FROM cache_time WHERE table_name = 'currency_rates'").fetchone()
    if currency_last_updated is None or (abs(currency_last_updated[0] - now)).seconds / 3600 > 12:
        # Have not stored currency or currency exchange rates are out of date (> 12 hours)
        print("Currency is out of date. Refreshing")
        get_and_store_exchanges()
        with open("data/currency_exchange.json") as file:
            data = json.loads(file.read())
            retrieval_time = datetime.fromtimestamp(data["time_last_updated"])
            currency_input = data["rates"].items()
            c.execute("INSERT OR REPLACE INTO cache_time VALUES(?, ?)", ("currency_rates", retrieval_time))
            c.executemany("INSERT OR REPLACE INTO currency_rates VALUES(?, ?)", currency_input)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    enter_database()
    #get_and_store_exchanges()
