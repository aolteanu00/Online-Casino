#PROVIDES FUNCTIONS AND HELP FOR TO21
from flask import Flask, render_template
from urllib.request import urlopen, Request
import to21help as help
import json, sqlite3, csv

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

deckid = help.createDeck()
deckData = help.drawCardTemp(deckid)
print(help.getImage(deckData))
