from flask import Flask, render_template
from datetime import datetime
import urllib, json

def rickandmortyapi():
    url = urllib.request.urlopen("https://rickandmortyapi.com/api/character/")
    response = url.read()
    data = json.loads(response)
    print(data)
    # Use a for loop to add every element to the database
    return 0;

rickandmortyapi()
