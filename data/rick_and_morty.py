from flask import Flask, render_template
from data import database_builder, database_query
import urllib, json

def rickandmorty_apitodict():
    count = 493 # this is the total number of characters in rick and morty
    page = 1
    data = {}
    data['characters'] = []
    while count > 0:
        url = urllib.request.urlopen("https://rickandmortyapi.com/api/character/?page=" + str(page))
        response = url.read()
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
    with open('rickandmortydata.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('rickandmortydata.json') as json_file:
        data = json.load(json_file)
        for i in data['characters']:
            database_query.rickandmortydb(i['id'], i['name'], i['image_link'])
    return 0


def rickandmorty_dicttodb():
    with open('rickandmortydata.json') as json_file:
        data = json.load(json_file)
        for i in data['characters']:
            database_query.rickandmortydb(i['id'], i['name'], i['image_link'])
    return 0

rickandmorty_dicttodb()
# rickandmorty_apitodict() this only needs to be called once.
# the resulting file should be uploaded to github as a static file which we can pull from

# create a csv file and a function to read from the api and write to the csv file.
# use the above function to read from said file and create the database instead of directly requesting from the API
# this speeds things up instead of taking 20-30 seconds every time
