# from urllib.request import Request, urlopen
import sqlite3
import json
import time
import os
import urllib.request

# rickandmorty_apitodict() this only needs to be called once.
# the resulting file should be uploaded to github as a static file which we can pull from

# create a csv file and a function to read from the api and write to the csv file.
# use the above function to read from said file and create the database instead of directly requesting from the API
# this speeds things up instead of taking 20-30 seconds every time

def get_and_store_RandMcharacters():
    """
    Gets information on every character from Rick and Morty.
    The data is stored in the "data" directory as a JSON file.
    The JSON file is an array of array. The nested array data is ordered as followed:
        0: id of character
        1: name of character
        2: image link for character
    """
    count = 493 # this is the total number of characters in rick and morty
    page = 1
    data = {}
    data['characters'] = []
    while count > 0:
        request = urllib.request.urlopen("https://rickandmortyapi.com/api/character/?page=" + str(page))
        response = request.read()
        result = json.loads(response)
        # Use a for loop to add every element to the database
        for i in result['results']:
            data['characters'].append({
                'id' : i['id'],
                'name' : i['name'],
                'image_link' : i['image']
            })
            count -= 1
        page += 1
    with open('data/rickandmortydata.json', 'w') as outfile:
        json.dump(data, outfile)
    print("Got character info and cached into data/rickandmortydata.json")

def enter_database():
    """
    Gets first generation pokemon and all the types (even those not in first generation) to store on the database.
    The first time this function is called, the API data receieved will be cached in the "data" directory. Sequential
    calls to this function will use the cached data instead.

    Make sure the database has been created before this is called.
    """
    database = sqlite3.connect("data/database.db")
    c = database.cursor()

    # rick and morty data
    if not os.path.exists("data/rickandmortydata.json"):
        get_and_store_RandMcharacters()
    with open('data/rickandmortydata.json') as json_file: # change this to not use database_query fucntion
        data = json.load(json_file)
        for i in data['characters']:
            c.execute("INSERT INTO rickandmorty(id, full_name, image_link) VALUES (?, ?, ?)", (i['id'], i['name'], i['image_link']))

    database.commit()
    database.close()


if __name__ == "__main__":
    enter_database()
