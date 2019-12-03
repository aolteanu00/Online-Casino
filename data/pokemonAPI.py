from urllib.request import Request, urlopen
import sqlite3
import json
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_and_store_pokemon():
    """
    Gets information on the first and second generation pokemon (National Dex 1 to 252):
    The data is stored in the "data" directory as a JSON file.
    The JSON file is an array of array. The nested array data is ordered as followed:
        0: name
        1: number of types
        2: first type
        3: second type
        4: image of pokemon (sprite)
    """
    pokemons = []

    # We are only using first and second gen pokemon
    for pokemon_id in range(1, 252):
        request = Request("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id), headers=headers)
        response = urlopen(request).read()
        data = json.loads(response)

        number_of_types = len(data["types"])
        pokemon_info = [
            data['name'],
            number_of_types,
            # The primary type is index 1 and secondary type is index 0
            data["types"][1]["type"]["name"] if number_of_types == 2 else data["types"][0]["type"]["name"],
            data["types"][0]["type"]["name"] if number_of_types == 2 else data["types"][0]["type"]["name"],
            data["sprites"]["front_default"]
        ]
        pokemons.append(pokemon_info)

        # We are limited to 100 request per minute, so we need to pause for 1 second at an arbitrary middle
        if pokemon_id % 90 == 0:
            time.sleep(1)

    file = open("data/pokemon.json", 'w')
    file.write(str(json.dumps(pokemons)))
    print("Got pokemon and cached to data/pokemon.json")


def get_and_store_types():
    """
    Gets information on every type (even those not in first generation pokemon).
    The data is stored in the "data" directory as a JSON file.
    The JSON file is an array of array. The nested array data is ordered as followed:
        0: name
        1: double damage to
        2: half damage to
        3: no damage to
    """
    types = []

    # Even though we are using first and second gen pokemon, we should still store ALL types to make
    # expandability easier and for cleaner code (don't need to have a lot of if statements)
    for type_id in range(1, 19):
        request = Request("https://pokeapi.co/api/v2/type/{}".format(type_id), headers=headers)
        response = urlopen(request).read()
        data = json.loads(response)

        type_info = [
            data["name"],
            flatten_object_array(data["damage_relations"]["double_damage_to"]),
            flatten_object_array(data["damage_relations"]["half_damage_to"]),
            flatten_object_array(data["damage_relations"]["no_damage_to"])
        ]
        types.append(type_info)

    file = open("data/pokemon_types.json", 'w')
    file.write(json.dumps(types))
    print("Got pokemon types and cached to data/pokemon_types.json")


def flatten_object_array(dictionary_array: list):
    """
    Converts an array of dictionaries with key "name" into a comma separated string with all the value for key "name"
    """
    output = ""
    for dictionary in dictionary_array:
        output += dictionary["name"] + ","
    return output


def enter_database():
    """
    Gets first generation pokemon and all the types (even those not in first generation) to store on the database.
    The first time this function is called, the API data receieved will be cached in the "data" directory. Sequential
    calls to this function will use the cached data instead.

    Make sure the database has been created before this is called.
    """
    database = sqlite3.connect("data/database.db")
    c = database.cursor()

    # Pokemon data
    if not os.path.exists("data/pokemon.json"):
        get_and_store_pokemon()
    with open('data/pokemon.json', 'r') as pokemon_file:
        # The file is an array of array of pokemon data
        pokemon_insert = [tuple(pokemon_data) for pokemon_data in json.loads(pokemon_file.read())]
        c.executemany("INSERT INTO pokemon VALUES (?, ?, ?, ?, ?)", pokemon_insert)

    # Pokemon type data
    if not os.path.exists("data/pokemon_types.json"):
        get_and_store_types()
    with open('data/pokemon_types.json', 'r') as pokemon_types_file:
        # The file is an array of array of type information
        type_insert = [tuple(type_info) for type_info in json.loads(pokemon_types_file.read())]
        c.executemany("INSERT INTO pokemon_types VALUES (?, ?, ?, ?)", type_insert)

    database.commit()
    database.close()


def initialize():
    enter_database()
