"""
Session data:
- "paid" (bool): True if user paid, false if user has not paid. This should be set to False when user finishes a game
- "current_game" (str): This should be the route to the entrance of your game. This should work when you run redirect(url_for(session["current_game"]))
- "bet_amount" (int): Amount the user is betting on the game.

Session is all cleared when user logouts
"""
import os, random
from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_query
from pokemon_game.routes import pokemon_game
from payments.routes import payment
from rickandmorty_game.routes import rickandmorty_game
import to21help as help
import random

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(pokemon_game)
app.register_blueprint(payment)
app.register_blueprint(rickandmorty_game)

@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("game"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if len(request.form) == 2:
        # User entered login information
        username: str = request.form["username"]
        password: str = request.form["password"]

        if database_query.is_valid_login(username, password):
            session["username"] = username
            print("Logged into account with username: " + username)
            return redirect(url_for("game"))
        else:
            flash("Wrong username or password")

    return render_template("login.html")


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if len(request.form) == 3:
        # User entered create account information
        username: str = request.form["username"]
        password: str = request.form["password"]
        password_repeat: str = request.form["password_repeat"]

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
    session.clear()
    return redirect(url_for("login"))


@app.route("/game")
def game():
    if "username" not in session:
        return redirect(url_for("login"))
    if "current_game" in session:
        return redirect(url_for(session["current_game"]))
    session["paid"] = False
    return render_template("game.html")

@app.route("/bet", methods=["GET"])
def bet():
    if "username" not in session:
        return redirect(url_for("login"))
    print("Choosing amount to bet on")
    if "current_game" not in session:
        return redirect(url_for("game"))

    # If user leaves midgame to bet page, we do not want to double charge
    if session["paid"]:
        return redirect(url_for(session["current_game"]))

    if "add_funds" in request.args:
        print("User is adding funds:")
        return redirect(url_for("payment.pay"))
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
            if session["current_game"] == "to21":
                return redirect(url_for("to21initilize"))
            return redirect(url_for(session["current_game"]))
    elif "go_back" in request.args:
        print("Did not pay. Leaving " + session["current_game"])
        del session["current_game"]
        return redirect(url_for("game"))
    elif "instruction" in request.args:
        print("Request information for " + session["current_game"])
        return redirect(url_for("instruction"))
    return render_template("bet.html", game=session["current_game"])


@app.route("/instruction")
def instruction():
    if "username" not in session:
        return redirect(url_for("login"))

    if session["current_game"] == "pokemon_game.pokemon":
        return redirect(url_for("pokemon_game.pokemon_instructions"))

    if session["current_game"] == "to21":
        return redirect(url_for("to21rules"))

    return "Instructions"


@app.route("/to21")
def to21():
    if "username" not in session:
        return redirect(url_for("login"))

    #cannot play two games at once
    if "current_game" in session and session["current_game"] != "to21":
        print("Trying to play To21 but is already playing " + session["current_game"])
        return redirect(url_for("game"))

    session["current_game"] = "to21"

    return render_template("to21home.html")

@app.route("/to21/rules")
def to21rules():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("to21rules.html")


#initializes database
@app.route("/to21/initilize")
def to21initilize():
    if "username" not in session:
        return redirect(url_for("login"))

    #if database already exists, delete it
    command = "DROP TABLE IF EXISTS gameinfo;"
    help.runsqlcommand(command)

    #initialize database
    help.createDB()
    help.initializeDB()

    return redirect(url_for("to21start"))


@app.route("/to21/start")
def to21start():
    if "username" not in session:
        return redirect(url_for("login"))

    #VARIABLES
    deckid = help.getdeckid()

    session["userHand"] = []
    session["dealerHand"] = []

    session["userHand"].append(help.drawCard(deckid))
    session["userHand"].append(help.drawCard(deckid))

    session["dealerHand"].append(help.drawCard(deckid))
    session["dealerHand"].append(help.drawCard(deckid))

    userStartAmount = session["userHand"][0] + session["userHand"][1]
    dealerStartAmount = session["dealerHand"][0] + session["dealerHand"][1]

    #deal to the user and dealer
    command = "UPDATE gameinfo SET userTotal = '{}', dealerTotal = '{}';".format(userStartAmount, dealerStartAmount)
    help.runsqlcommand(command)
    command = "UPDATE gameinfo SET userNumCards = 2, dealerNumCards = 2;"
    help.runsqlcommand(command)
    userNumCards = help.getUserNumCards()
    dealerNumCards = help.getDealerNumCards()

    return render_template("to21start.html", USA = userStartAmount, DSA = dealerStartAmount)


@app.route("/to21/live")
def to21live():
    if "username" not in session:
        return redirect(url_for("login"))

    print("we are in live")
    print(session["userHand"])
    #VARIABLES
    deckid = help.getdeckid()
    userCurrentAmount = help.getUserAmt()
    dealerCurrentAmount = help.getDealerAmt()

    return render_template("to21live.html", dealerCards = session["dealerHand"], UCA = userCurrentAmount, DCA = dealerCurrentAmount)


@app.route("/to21/dealCard")
def dealCard():
    if "username" not in session:
        return redirect(url_for("login"))

    #VARIABLES AND ADJUSTING DATABASE
    deckid = help.getdeckid()
    userCurrentAmount = help.getUserAmt()
    numCards = help.getUserNumCards()
    numCards += 1
    newVal = help.drawCard(deckid)

    print(session["userHand"])
    print("hello")

    #if user draws an ace
    if newVal == 1:
        if (userCurrentAmount + 10) <= 21:
            newVal = 11
        else:
            newVal = 1
    dog = session["userHand"][:]
    dog.append(newVal)
    session["userHand"] = dog
    newVal += userCurrentAmount

    command = "UPDATE gameinfo SET userTotal = '{}', userNumCards = '{}';".format(newVal, numCards)
    help.runsqlcommand(command)


    #if the user exceeds 21 terminate game
    if help.getUserAmt() > 21:
        return redirect(url_for("to21results"))

    print(session["userHand"])
    return redirect(url_for("to21live"))


@app.route("/to21/results")
def to21results():
    if "username" not in session:
        return redirect(url_for("login"))

    del session["current_game"]
    session["paid"] = False


    #VARIABLES
    deckid = help.getdeckid()
    userCurrentAmount = help.getUserAmt()
    userNumCards = help.getUserNumCards()
    userTemp = 0
    dealerTemp = 0
    additionalCards = 0

    #dealer "ai"
    while help.getDealerAmt() < 18:
        newVal = help.drawCard(deckid)
        session["dealerHand"].append(newVal)
        newVal += help.getDealerAmt()
        numCards = help.getDealerNumCards()
        numCards += 1
        command = "UPDATE gameinfo SET dealerTotal = '{}', dealerNumCards = '{}';".format(newVal, numCards)
        help.runsqlcommand(command)
        additionalCards += 1
    additionalCards = str(additionalCards)
    dealerCurrentAmount = help.getDealerAmt()
    dealerNumCards = help.getDealerNumCards()

    #CALCULATE AUTOMATIC WINS AND LOSSES
    #if user and dealer exceed 21
    if userCurrentAmount > 21 and dealerCurrentAmount > 21:
        message = "Y'all tied! Everyone keeps their MAWDollars."

        current_balance = database_query.get_balance(session["username"])
        new_balance = current_balance + session["bet_amount"]
        database_query.update_balance(session["username"], new_balance)

        print("both parties over 21")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message, UCA = userCurrentAmount, DCA = dealerCurrentAmount)

    #if dealer exceeds 21
    if userCurrentAmount <= 21 and dealerCurrentAmount > 21:
        message = "You won and doubled your wager!"

        current_balance = database_query.get_balance(session["username"])
        new_balance = current_balance + session["bet_amount"] + session["bet_amount"]
        database_query.update_balance(session["username"], new_balance)

        print("dealer over 21")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message, UCA = userCurrentAmount, DCA = dealerCurrentAmount)

    #if user exceeds 21
    if userCurrentAmount > 21 and dealerCurrentAmount <= 21:
        message = "You lost the game and your wager!"

        current_balance = database_query.get_balance(session["username"])
        bet_amount = session["bet_amount"]
        new_balance = current_balance
        database_query.update_balance(session["username"], new_balance)

        print("user over 21")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message,  UCA = userCurrentAmount, DCA = dealerCurrentAmount)

    #CALCULATE IF BOTH PARTIES FALL UNDER 21
    if userCurrentAmount <21:
        userTemp = 21 - userCurrentAmount
    if dealerCurrentAmount < 21:
        dealerTemp = 21 - dealerCurrentAmount

    #simple tie
    if userTemp == dealerTemp:
        message = "Y'all tied! Everyone keeps their MAWDollars."

        current_balance = database_query.get_balance(session["username"])
        bet_amount = session["bet_amount"]
        new_balance = current_balance + bet_amount
        database_query.update_balance(session["username"], new_balance)

        print("tie, same score")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message,  UCA = userCurrentAmount,  DCA = dealerCurrentAmount)

    #user wins
    if userTemp < dealerTemp:
        message = "You won and doubled your wager!"

        current_balance = database_query.get_balance(session["username"])
        bet_amount = session["bet_amount"]
        new_balance = current_balance + bet_amount + bet_amount
        database_query.update_balance(session["username"], new_balance)

        print("user wins")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message,  UCA = userCurrentAmount, DCA = dealerCurrentAmount)

    #dealer wins
    else:
        message = "You lost the game and your wager!"

        current_balance = database_query.get_balance(session["username"])
        bet_amount = session["bet_amount"]
        new_balance = current_balance
        database_query.update_balance(session["username"], new_balance)

        print("dealer wins")
        return render_template("to21results.html", userCards = session["userHand"], dealerCards = session["dealerHand"], ac = additionalCards, message = message,  UCA = userCurrentAmount, DCA = dealerCurrentAmount)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.globals.update(get_balance=lambda: database_query.get_balance(session["username"]))
    app.run()
