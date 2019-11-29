"""
Session data created by pokemon game (these will also be deleted upon finishing the game):
- "game_state": Determines which route to use. The possible values (str):
    - "pregame": User did not pay yet, but did select pokemon as the game he/she wants to play
    - "selecting": The user sees the page for selecting which pokemon he/she wants, but did not select one yet
    - "result": The user had selected a pokemon card and the result is shown to the user. At this point, the session
    data created by this Blueprint is deleted and the session["paid"] is set to False
- "computer_pokemons" (list of str): A list of names of the pokemon the computer has
- "user_pokemons" (list of str): A list of names of the pokemon the user has
- "computer_selected_card" (str): The name of the pokemon the computer randomly selected

Session data updated
- "paid": Will be set to False once the game is completed
- "bet_amount": Will be set to 0 once the game is finished
- "current_game" Will be deleted
"""

import random
from flask import Blueprint, session, render_template, redirect, url_for, request
from pokemon_game.pokemon_game import get_pokemon, get_four_random_pokemons, user_balance_lost
from data.database_query import update_balance, get_balance

pokemon_game = Blueprint("pokemon_game", __name__)


@pokemon_game.route("/pokemon")
def pokemon():
    # Must be logged in to play a game
    if "username" not in session:
        return redirect(url_for("login"))

    # Cannot play multiple games at once
    if "current_game" in session and session["current_game"] != "pokemon_game.pokemon":
        print("Trying to play pokemon but is already playing " + session["current_game"])
        return redirect(url_for("game"))
    else:
        session["current_game"] = "pokemon_game.pokemon"
        # If the user is already playing this game and either goes back in history from browser / manually enter url,
        # bring them to the route they are supposed to be on
        if "game_state" in session:
            if session["game_state"] == "selecting":
                return redirect(url_for(".pokemon_select"))
            elif session["game_state"] == "result":
                return redirect(url_for("./pokemon_result"))
        else:
            print("User is now playing pokemon")
            session["game_state"] = "pregame"

    # Must pay before
    if session["paid"]:
        session["game_state"] = "selecting"
        return redirect(url_for(".pokemon_select"))
    else:
        return redirect(url_for("bet"))


@pokemon_game.route("/pokemon/select")
def pokemon_select():
    # Must be logged in to play
    if "username" not in session:
        return redirect(url_for("login"))

    # Make sure the user is playing the pokemon game
    if "current_game" not in session or session["current_game"] != "pokemon_game.pokemon":
        # User did not select a game or user is playing another game
        return redirect(url_for(".pokemon"))

    # Make sure the user is on the right page
    if session["game_state"] != "selecting":
        return redirect(url_for(".pokemon"))

    # Prevents user from refreshing the cards on page reload
    if "user_pokemons" not in session:
        session["computer_pokemons"] = get_four_random_pokemons()
        session["user_pokemons"] = get_four_random_pokemons()
        session["computer_selected_pokemon"] = random.choice(session["computer_pokemons"])

    user_pokemons = [get_pokemon(name) for name in session["user_pokemons"]]
    return render_template("pokemon/select.html", user_pokemons=user_pokemons)


@pokemon_game.route("/pokemon/result", methods=["POST"])
def pokemon_result():
    # Must be logged in to play
    if "username" not in session:
        return redirect(url_for("login"))

    # Make sure the user is playing the pokemon game
    if "current_game" not in session or session["current_game"] != "pokemon_game.pokemon":
        # User did not select a game or user is playing another game
        return redirect(url_for(".pokemon"))

    # User must select a pokemon to reach this page
    if len(request.form) != 1 or "pokemon_selected" not in request.form:
        return redirect(url_for(".pokemon"))

    if ("game_state" not in session) or session["game_state"] != "selecting":
        return redirect(url_for(".pokemon"))

    session["game_state"] = "result"
    user_selected_pokemon = get_pokemon(request.form["pokemon_selected"])
    # Make sure the pokemon selected is one that the user was given
    if user_selected_pokemon.name not in session["user_pokemons"]:
        print("Pokemon {} was not given to user".format(user_selected_pokemon.name))
        del session["game_state"]
        session["paid"] = False
        session["bet_amount"] = 0
        del session["computer_selected_pokemon"]
        del session["computer_pokemons"]
        del session["user_pokemons"]
        del session["current_game"]
        return "Nice try cheating, still took your money though"
    else:
        user_change_balance = user_balance_lost(user_selected_pokemon.name, session["computer_selected_pokemon"],
                                                session["bet_amount"])
        user_current_balance = get_balance(session["username"])
        if user_change_balance == 0:
            winner_message = "Tie!"
            balance_message = f"The {session['bet_amount']} MAWDollars you bet was returned"
            new_balance = user_current_balance + session["bet_amount"]
        elif user_change_balance > 0:
            winner_message = "You won!"
            # If user won, he/she gets back what was bet and what was won
            new_balance = user_current_balance + session["bet_amount"] + user_change_balance
            balance_message = f"You won {user_change_balance}"
        else:
            winner_message = "You lost"
            # If user lost, he/she lost what was bet and what was lost
            new_balance = user_current_balance + user_change_balance
            balance_message = f"You lost {-user_change_balance}"

        print("User old balance: {}\nUser new Balance: {}".format(user_current_balance, new_balance))
        update_balance(session["username"], new_balance)

    computer_slected_pokemon = get_pokemon(session["computer_selected_pokemon"])
    computer_pokemons = [get_pokemon(name) for name in session["computer_pokemons"]]
    user_pokemons = [get_pokemon(name) for name in session["user_pokemons"]]

    del session["game_state"]
    session["paid"] = False
    session["bet_amount"] = 0
    del session["computer_selected_pokemon"]
    del session["computer_pokemons"]
    del session["user_pokemons"]
    del session["current_game"]

    return render_template("pokemon/result.html",
                           computer_pokemons=computer_pokemons,
                           computer_selected_pokemon=computer_slected_pokemon,
                           user_pokemons=user_pokemons,
                           user_selected_pokemon=user_selected_pokemon,
                           winner_message=winner_message,
                           balance_message=balance_message)
