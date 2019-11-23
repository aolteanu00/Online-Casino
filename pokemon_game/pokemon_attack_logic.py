from data import database_query as query
from pokemon_game import type_logic
from collections import namedtuple
import random

Pokemon = namedtuple("pokemon", ["name", "number_types", "first_type", "second_type", "image"])
pokemons = dict()

for pokemon in query.pokemon_info():
    pokemon_name = pokemon[0]
    pokemons[pokemon_name] = Pokemon(*pokemon)


def get_random_pokemon():
    return random.choice(list(pokemons.values()))


def get_pokemon(name: str):
    if name not in pokemons.keys():
        print("{} is not a pokemon we have".format(name))
    return pokemons[name]


def user_balance_lost(user_pokemon: Pokemon, computer_pokemon: Pokemon, bet_amount) -> int:
    """
    Determine winner based on pokemon chosen by user and computer.
    Pokemon A, and B:
    Formula:
    (A type 1 attacks B type 1 + A type 1 attacks B type 2) -
    (B type 1 attacks A type 1 + B type 1 attacks A type 2)
    If difference is:

    Equal to 0: No money shared. User keeps what is bet
    Between [.5 and 1.5]: Winner takes 1/2 of what loser bet
    Rest: Winner takes all

    Example:
    (User) Pokemon A: Bug, Ice
    (Computer) Pokemon B: Fire Fighting
    A attacks: Bug attacks fire and fighting, which is 1/2 + 1/2 = 1
    B attacks: Fire attacks bug and ice, which is 2 + 2 = 4
    Difference is 3 in favor of B. Therefore the computer gets everything the user bet.

    :param user_pokemon:
    :param computer_pokemon:
    :return: Negative if user lost, positive is user won. Returned amount is the change in balance.
             For example, if it is -2 then the user lost 2 dollars and the website owner won 2 dollars
    """
    user_attack = type_logic.damage_to(user_pokemon.first_type, computer_pokemon.first_type) + type_logic.damage_to(user_pokemon.first_type, computer_pokemon.second_type)
    computer_attack = type_logic.damage_to(computer_pokemon.first_type, user_pokemon.first_type) + type_logic.damage_to(computer_pokemon.first_type, user_pokemon.second_type)
    difference = abs(user_attack - computer_attack)
    print("{} attacks {} for {}".format(user_pokemon.name, computer_pokemon.name, difference))

    money_exchange = 0
    if difference == 0:
        # 45% of this happening
        money_exchange = 0
    if .5 <= difference <= 1.5:
        # 33% of this happening
        money_exchange = .5 * bet_amount
    else:
        # 22% of this happening
        money_exchange = bet_amount

    return -money_exchange if user_attack < computer_attack else money_exchange
