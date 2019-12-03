#PROVIDES FUNCTIONS AND HELP FOR TO21
from flask import Flask, render_template
from urllib.request import urlopen, Request
import json, sqlite3, csv

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}
#------------------------------------------------------------------------------
#DATABSE WORK
#faciliates usage of sql commands
def runsqlcommand(command):
    DB_FILE = "glit.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops
    c.execute(command)
    if "select" in command.lower():
        return c.fetchall()
    db.commit()  # save changes
    db.close()  # close database


#create table to store game data
def createDB():
    command = "CREATE TABLE gameinfo(deckid TEXT, userTotal INT, userNumCards INT, dealerTotal INT, dealerNumCards INT);"
    runsqlcommand(command)


#initilizes gameinfo database, runs only once per game
def initializeDB():
    deckid = createDeck()
    deckid = str(deckid)
    command = "INSERT INTO gameinfo(deckid, userTotal, userNumCards, dealerTotal, dealerNumCards) VALUES('{}',0,0,0,0);".format(deckid)
    runsqlcommand(command)


#retrieves deckid
def getdeckid():
    command = "SELECT deckid FROM gameinfo;"
    deckid = runsqlcommand(command)
    return str(deckid[0][0])


#retrives user's current amount
def getUserAmt():
    command = "SELECT userTotal FROM gameinfo;"
    userAmt = runsqlcommand(command)
    return int(userAmt[0][0])


#retrieves number of cards user has drawn
def getUserNumCards():
    command = "SELECT userNumCards FROM gameinfo;"
    userAmt = runsqlcommand(command)
    return int(userAmt[0][0])


#retrives dealer's current amount
def getDealerAmt():
    command = "SELECT dealerTotal FROM gameinfo;"
    dealerAmt = runsqlcommand(command)
    return int(dealerAmt[0][0])


#retrieves number of cards dealer has drawn
def getDealerNumCards():
    command = "SELECT dealerNumCards FROM gameinfo;"
    userAmt = runsqlcommand(command)
    return int(userAmt[0][0])
#------------------------------------------------------------------------------
#FUNCTIONS
#creates a deck and returns it's id
def createDeck():
    deckid = ""
    request = Request("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1", headers=headers)
    response = urlopen(request).read()
    data = json.loads(response)
    deckid = data['deck_id']
    return deckid


#draw a card from a deck given its id
# def drawCard(deckid):
#     request = Request("https://deckofcardsapi.com/api/deck/{id}/draw/?count=1".format(id = deckid), headers=headers)
#     response = urlopen(request).read()
#     data = json.loads(response)
#     temp = data['cards']
#     value = temp[0]['value']
#     if value == "KING" or value == "QUEEN" or value == "JACK":
#         return 10
#     if value == "ACE":
#         return 1 #decide value of ace during game
#     else:
#         return int(value)

def drawCard(deckid):
    request = Request("https://deckofcardsapi.com/api/deck/{id}/draw/?count=1".format(id = deckid), headers=headers)
    response = urlopen(request).read()
    data = json.loads(response)
    return data

def getValue(deckData):
    temp = deckData['cards']
    value = temp[0]['value']
    if value == "KING" or value == "QUEEN" or value == "JACK":
        return 10
    if value == "ACE":
        return 1 #decide value of ace during game
    else:
        return int(value)

def getImage(deckData):
    temp = deckData['cards']
    image = temp[0]['image']
    return image
