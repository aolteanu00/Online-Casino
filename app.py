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
import to21help as help
import random

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(pokemon_game)
app.register_blueprint(payment)


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
        return redirect(url_for("game"))

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
    return "Instructions"


@app.route("/to21")
def to21():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("to21home.html")


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
    userStartAmount = help.drawCard(deckid) + help.drawCard(deckid)
    dealerStartAmount = help.drawCard(deckid) + help.drawCard(deckid)

    #deal to the user and dealer
    command = "UPDATE gameinfo SET userTotal = '{}', dealerTotal = '{}';".format(userStartAmount, dealerStartAmount)
    help.runsqlcommand(command)
    command = "UPDATE gameinfo SET userNumCards = 2, dealerNumCards = 2;"
    help.runsqlcommand(command)
    userNumCards = help.getUserNumCards()
    dealerNumCards = help.getDealerNumCards()

    return render_template("to21start.html", USA = userStartAmount, UNUM = userNumCards, DSA = dealerStartAmount, DNUM = dealerNumCards, deckid = deckid)


@app.route("/to21/live")
def to21live():
    if "username" not in session:
        return redirect(url_for("login"))

    #VARIABLES
    deckid = help.getdeckid()
    userCurrentAmount = help.getUserAmt()
    userNumCards = help.getUserNumCards()
    dealerCurrentAmount = help.getDealerAmt()
    dealerNumCards = help.getDealerNumCards()

    return render_template("to21live.html", UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)


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

    #if user draws an ace
    if newVal == 0:
        if (userCurrentAmount + 10) < 21:
            newVal = 11
        else:
            newVal = 1
    newVal += userCurrentAmount
    command = "UPDATE gameinfo SET userTotal = '{}', userNumCards = '{}';".format(newVal, numCards)
    help.runsqlcommand(command)

    #if the user exceeds 21 terminate game
    if help.getUserAmt() > 21:
        return redirect(url_for("to21results"))

    return redirect(url_for("to21live"))


@app.route("/to21/results")
def to21results():
    if "username" not in session:
        return redirect(url_for("login"))

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
        newVal += help.getDealerAmt()
        numCards = help.getDealerNumCards()
        numCards += 1
        command = "UPDATE gameinfo SET dealerTotal = '{}', dealerNumCards = '{}';".format(newVal, numCards)
        help.runsqlcommand(command)
        additionalCards += 1
    additionalCards = str(additionalCards)
    dealerCurrentAmount = help.getDealerAmt()
    dealerNumCards = help.getDealerNumCards()

    #calculate automatic wins and losses
    if userCurrentAmount > 21 and dealerCurrentAmount > 21:
        tie = True
        win = False
        message = "Y'all both drew too high. You keep your money."
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)
    if userCurrentAmount < 21 and dealerCurrentAmount > 21:
        tie = False
        win = True
        message = "The dealer drew too high. Congrats!"
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)
    if userCurrentAmount > 21 and dealerCurrentAmount < 21:
        tie = False
        win = False
        message = "You drew too high. Ha!"
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)

    #calulate win if both parties fall under 21
    if userCurrentAmount <21:
        userTemp = 21 - userCurrentAmount
    if dealerCurrentAmount < 21:
        dealerTemp = 21 - dealerCurrentAmount

    if userTemp == dealerTemp:
        tie = True
        win = False
        message = "Y'all tied. You keep your money"
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)
    if userTemp < dealerTemp:
        tie = False
        win = True
        message = "Congrats!"
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)
    else:
        tie = False
        win = False
        message = "Ha!"
        return render_template("to21results.html", ac = additionalCards, message = message, tie = tie, win = win,  UCA = userCurrentAmount, UNUM = userNumCards, DCA = dealerCurrentAmount, DNUM = dealerNumCards, deckid = deckid)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.globals.update(get_balance=lambda: database_query.get_balance(session["username"]))
    app.run()
