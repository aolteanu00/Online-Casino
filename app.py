import os, random
from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_query
from pokemon_game import pokemon_game
import random

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("game"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET"])
def login():
    if len(request.args) == 2:
        # User entered login information
        username: str = request.args["username"]
        password: str = request.args["password"]

        if database_query.is_valid_login(username, password):
            session["username"] = username
            print("Logged into account with username: " + username)
            return redirect(url_for("game"))
        else:
            flash("Wrong username or password")

    return render_template("login.html")


@app.route("/create-account", methods=["GET"])
def create_account():
    if len(request.args) == 3:
        # User entered create account information
        username: str = request.args["username"]
        password: str = request.args["password"]
        password_repeat: str = request.args["password_repeat"]

        if password != password_repeat:
            flash("Passwords do not match")
        elif len(password.strip()) == 0:
            flash("Passwords must not be blank")
        elif len(username.strip()) == 0:
            flash("Username must not be blank")
        elif database_query.does_username_exist(username):
            flash("Username already exists")
        else:
            database_query.create_account(username, password)
            print("Created account with username: " + username)
            session["username"] = username
            return redirect(url_for("game"))

    return render_template("create-account.html")


@app.route("/logout")
def logout():
    flash("You logged out")
    print("Logged out of session (username " + session["username"] + ")")
    del session["username"]
    return redirect(url_for("login"))


@app.route("/game")
def game():
    if "username" not in session:
        return redirect(url_for("login"))
    session["paid"] = False
    return render_template("game.html")


@app.route("/rickandmorty")
def rickandmortygame():
    character_id = int(random.randrange(1, 494, 1))
    character_info = database_query.rickandmorty_getinfo(character_id)
    print(character_info)
    # character_info is a 2-D array with [0][0] being the name and [0][1] being the image link
    return render_template("rickandmorty.html", image = character_info[0][1])


@app.route("/bet", methods=["GET"])
def bet():
    if "username" not in session:
        return redirect(url_for("login"))
    print("Choosing amount to bet on")
    if "current_game" not in session:
        # If user: 1. Selects a game to play
        #          2. Clicks "go back"
        #          3. Manually go back in history
        # The server will crash
        return redirect(url_for("game"))

    if "add_funds" in request.args:
        print("User is adding funds:")
        return redirect(url_for("pay"))
    elif "spending_amount" in request.args:
        print("User is spending: " + request.args["spending_amount"])
        new_balance = database_query.get_balance(session["username"]) - int(request.args["spending_amount"])
        if new_balance < 0:
            print("Not enough in user's balance")
            flash("Not enough money in your account, please add more")
        else:
            print("Entering " + session["current_game"])
            database_query.update_balance(session["username"], new_balance)
            session["paid"] = True
            session["bet_amount"] = int(request.args["spending_amount"])
            return redirect(url_for(session["current_game"]))
    elif "go_back" in request.args:
        print("Did not pay. Leaving " + session["current_game"])
        del session["current_game"]
        return redirect(url_for("game"))
    elif "instruction" in request.args:
        print("Request information for " + session["current_game"])
        return redirect(url_for("instruction"))
    return render_template("bet.html", game=session["current_game"])


@app.route("/pay")
def pay():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("pay.html")


@app.route("/instruction")
def instruction():
    if "username" not in session:
        return redirect(url_for("login"))
    return "Instructions"


@app.route("/pokemon")
def pokemon():
    if "username" not in session:
        return redirect(url_for("login"))

    if "game_state" not in session:
        print("Pregame state")
        session["current_game"] = "pokemon"
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
        session["computer_pokemons"] = pokemon_game.get_four_random_pokemons()
        session["user_pokemons"] = pokemon_game.get_four_random_pokemons()
        session["computer_selected_pokemon"] = random.choice(session["computer_pokemons"])
        session["game_state"].append("initialized")

    if "result" in session["game_state"]:
        user_change_balance = pokemon_game.user_balance_lost(session["user_selected_pokemon"], session["computer_selected_pokemon"], session["bet_amount"])
        if user_change_balance == 0:
            winner_message = "Tie!"
        elif user_change_balance > 0:
            winner_message = "You won!"
        else:
            winner_message = "You lost"
        del session["game_state"]
        return render_template("pokemon/result.html",
                               computer_pokemons=[pokemon_game.get_pokemon(name) for name in session["computer_pokemons"]],
                               computer_selected_pokemon=pokemon_game.get_pokemon(session["computer_selected_pokemon"]),
                               user_pokemons=[pokemon_game.get_pokemon(name) for name in session["user_pokemons"]],
                               user_selected_pokemon=pokemon_game.get_pokemon(session["user_selected_pokemon"]),
                               winner_message=winner_message)
    else:
        return render_template("pokemon/play.html", user_pokemons=[pokemon_game.get_pokemon(name) for name in session["user_pokemons"]])


@app.route("/api/pokemon/select", methods=["POST"])
def api_pokemon_select():
    if request.form["pokemon"] in session["user_pokemons"]:
        session["user_selected_pokemon"] = request.form["pokemon"]
        session["game_state"].append("result")
    else:
        flash("Please choose a pokemon")
    return redirect(url_for("pokemon"))


if __name__ == "__main__":
    app.debug = True
    app.run()
