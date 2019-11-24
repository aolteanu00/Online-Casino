import random
from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from pokemon_game.pokemon_game import get_pokemon, get_four_random_pokemons, user_balance_lost

pokemon_game = Blueprint("pokemon_game", __name__)


@pokemon_game.route("/pokemon")
def pokemon():
    if "username" not in session:
        return redirect(url_for("login"))

    if "game_state" not in session:
        print("Pregame state")
        session["current_game"] = "pokemon_game.pokemon"
        session["game_state"] = []
        print("----")
        print(str(session["game_state"]))
        print("----")

    if not session["paid"]:
        # User needs to pay
        return redirect(url_for("bet"))

    if "initialized" not in session["game_state"]:
        print("initializng game")
        # Initialize Game
        session["computer_pokemons"] = get_four_random_pokemons()
        session["user_pokemons"] = get_four_random_pokemons()
        session["computer_selected_pokemon"] = random.choice(session["computer_pokemons"])
        session["game_state"].append("initialized")

    if "result" in session["game_state"]:
        user_change_balance = user_balance_lost(session["user_selected_pokemon"], session["computer_selected_pokemon"], session["bet_amount"])
        if user_change_balance == 0:
            winner_message = "Tie!"
        elif user_change_balance > 0:
            winner_message = "You won!"
        else:
            winner_message = "You lost"
        del session["game_state"]
        return render_template("pokemon/result.html",
                               computer_pokemons=[get_pokemon(name) for name in session["computer_pokemons"]],
                               computer_selected_pokemon=get_pokemon(session["computer_selected_pokemon"]),
                               user_pokemons=[get_pokemon(name) for name in session["user_pokemons"]],
                               user_selected_pokemon=get_pokemon(session["user_selected_pokemon"]),
                               winner_message=winner_message)
    else:
        return render_template("pokemon/play.html", user_pokemons=[get_pokemon(name) for name in session["user_pokemons"]])


@pokemon_game.route("/api/pokemon/select", methods=["POST"])
def api_pokemon_select():
    if request.form["pokemon"] in session["user_pokemons"]:
        session["user_selected_pokemon"] = request.form["pokemon"]
        session["game_state"].append("result")
    else:
        flash("Please choose a pokemon")
    return redirect(url_for("pokemon_game.pokemon"))