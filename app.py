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
            redirect(url_for("game.html"))
        else:
            flash("Wrong username or password")

    return render_template("login.html")


@app.route("/create-account", methods=["GET"])
def create_account():
    return render_template("create-account.html")


@app.route("/game")
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
