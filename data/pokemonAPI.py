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


def pokemon_info():
    store = dict()

    for pokemon_id in range(1, 152):
        # We are only using first gen pokemon
        request = Request("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id), headers=headers)
        response = urlopen(request).read()
        data = json.loads(response)

        pokemon_info = dict()

        num_types = len(data["types"])
        types = []

        pokemon_info["name"] = data['name']
        pokemon_info["number_types"] = num_types
        pokemon_info["first_type"] = data["types"][0]["type"]["name"]
        if num_types == 1:
            pokemon_info["second_type"] = pokemon_info["first_type"]
        else:
            pokemon_info["second_type"] = data["types"][1]["type"]["name"]
        pokemon_info["image"] = data["sprites"]["front_default"]
        store[pokemon_id] = pokemon_info
        print(pokemon_info["image"])
        time.sleep(1)

    file = open("pokemon.json", 'w')
    file.write(str(json.dumps(store)))


def type_info():
    store = dict()

    for type_id in range(1, 19):
        # Even though we are using first gen pokemon, we should still store ALL types to make
        # expandability easier and for cleaner code (don't need to have a lot of if statements)
        request = Request("https://pokeapi.co/api/v2/type/{}".format(type_id), headers=headers)
        response = urlopen(request).read()
        data = json.loads(response)

        type_info = dict()
        type_info["name"] = data["name"]
        type_info["double_damage_from"] = flatten_object_array(data["damage_relations"]["double_damage_from"])
        type_info["double_damage_to"] = flatten_object_array(data["damage_relations"]["double_damage_to"])
        type_info["half_damage_from"] = flatten_object_array(data["damage_relations"]["half_damage_from"])
        type_info["half_damage_to"] = flatten_object_array(data["damage_relations"]["half_damage_to"])
        type_info["no_damage_from"] = flatten_object_array(data["damage_relations"]["no_damage_from"])
        store[type_id] = type_info

    file = open("pokemon_type.json", 'w')
    file.write(json.dumps(store))


def flatten_object_array(pokemon_types: list):
    output = ""
    for pokemon_type in pokemon_types:
        output += pokemon_type["name"] + ","
    return output


def enter_database():
    database = sqlite3.connect("database.db")
    c = database.cursor()

    # Pokemon data
    with open('pokemon.json', 'r') as pokemon_file:
        pokemon_insert = []
        for pokemon_data in json.loads(pokemon_file.read()).values():
            pokemon_insert.append((pokemon_data["name"],
                                   pokemon_data["number_types"],
                                   pokemon_data["first_type"],
                                   pokemon_data["second_type"],
                                   pokemon_data["image"]))
        c.executemany("INSERT INTO pokemon VALUES (?, ?, ?, ?, ?)", pokemon_insert)

    # Pokemon type data
    with open('pokemon_type.json', 'r') as pokemon_type_file:
        type_insert = []
        for type_data in json.loads(pokemon_type_file.read()).values():
            type_insert.append((type_data["name"],
                                type_data["double_damage_from"],
                                type_data["double_damage_to"],
                                type_data["half_damage_from"],
                                type_data["half_damage_to"],
                                type_data["no_damage_from"]))
        c.executemany("INSERT INTO pokemon_types VALUES (?, ?, ?, ?, ?, ?)", type_insert)

    database.commit()
    database.close()


if __name__ == "__main__":
    enter_database()
