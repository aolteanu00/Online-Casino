from urllib.request import Request, urlopen
import json
import time

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

store = dict()

for pokemon_id in range(1, 152):
    # We are only using first gen pokemon
    request = Request("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id), headers=hdr)
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
