import os
from flask import Flask, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("game"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/create-account")
def create_account():
    return render_template("create-account.html")


@app.route("/game")
def game():
    return render_template("game.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
