from data import database_query as query
from collections import namedtuple
import random

characters = dict()

for character in query.rickandmorty_getinfo():
    characters[character[0]] = character[1]

def get_random_character():
    return random.choice(list(characters.keys()))

def get_character_image(name: str):
    if name not in characters.keys():
        print("{} is not a character we have".format(name))
    return characters[name]

def get_three_random_characters() -> list:
    return [get_random_character() for _ in range(0, 3)]

def get_nine_random_characters() -> list:
    return [get_random_character() for _ in range(0, 9)]

def user_balance_lost_rickandmorty(user_choices: list, correct_ans: list, bet_amount: int) -> int:
    """
    Determine winner based on the number of correct answers from the questionaire.

    User gets zero questions correct: user loses all of the money bet
    User gets one questions correct: user loses half of the money bet
    User gets two questions correct: user does not lose any of the money bet
    User gets all questions correct: user doubles up

    :param number_correct:
    :return: Negative if user answered zero to one questions correctly,
    zero if user answers two questions correctly,
    positive if user answers all questions correctly.
    """

    number_correct = 0
    index = 0
    for choice in user_choices:
        if choice == correct_ans[index]:
            number_correct += 1
        index += 1

    if number_correct == 0:
        return 0
    elif number_correct == 1:
        return bet_amount * .5
    elif number_correct == 2:
        return bet_amount
    elif number_correct == 3:
        return bet_amount * 2
