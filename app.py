import os
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
    return render_template("game.html")


@app.route("/bet", methods=["GET"])
def bet():
    if "add_funds" in request.args:
        print("User is adding funds: ")
        return redirect(url_for("pay"))
    elif "spending_amount" in session:
        print("User is spending: " + request.args["spending_amount"])
        new_balance = database_query.get_balance(session["username"]) - int(request.args["spending_amount"])
        if new_balance < 0:
            flash("Not enough money in your account, please add more")
        else:
            database_query.update_balance(session["username"], new_balance)
            session["paid"] = True
    return redirect(url_for(session["current_game"]))


@app.route("/pay")
def pay():
    return render_template("pay.html")


@app.route("/pokemon")
def pokemon():
    session["current_game"] = "pokemon"
    return render_template("bet.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
