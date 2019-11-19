import os
from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_builder, database_query

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def root():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("game"))


@app.route("/login", methods=["GET"])
def login():
    if len(request.args) == 2:
        # User entered log in information
        username = request.args["username"]
        password = request.args["password"]

        if database_query.is_valid_login(username, password):
            session["username"] = username
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
            session["username"] = username
            return redirect(url_for("game"))

    return render_template("create-account.html")


@app.route("/game")
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
