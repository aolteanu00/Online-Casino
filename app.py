import os, random
from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_builder, database_query


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
    return render_template("game.html")


@app.route("/rickandmorty")
def rickandmortygame():
    character_id = int(random.randrange(1, 494, 1))
    character_info = database_query.rickandmorty_getinfo(character_id)
    print(character_info)
    # character_info is a 2-D array with [0][0] being the name and [0][1] being the image link
    return render_template("rickandmorty.html", image = character_info[0][1])



if __name__ == "__main__":
    app.debug = True
    app.run()
