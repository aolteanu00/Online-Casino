from flask import Blueprint, redirect, url_for, flash, session, render_template, request
from data.database_query import update_balance, get_balance, MAWDollars_to_currency, get_supported_currencies

payment = Blueprint("payment", __name__)


@payment.route("/pay")
def pay():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("payment/pay.html")


@payment.route("/pay/processed", methods=["POST"])
def pay_processed():
    if "username" not in session:
        return redirect(url_for("login"))

    # Make sure user filled out all categories
    if all(keys in ["card_number", "month", "year", "cvv", "pay_amount"] for keys in request.form.keys()):
        # All fields filled out

        update_balance(session["username"], get_balance(session["username"]) + int(request.form["pay_amount"]))
        return render_template("payment/result.html", pay_amount=request.form["pay_amount"])
    else:
        flash("Please fill out all fields")
        return redirect(url_for(".pay"))


@payment.route("/redeem", methods=["GET"])
def redeem():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("payment/redeem.html", currencies=get_supported_currencies())


@payment.route("/redeem/processed", methods=["POST"])
def redeem_processed():
    if "username" not in session:
        return redirect(url_for("login"))

    # Make sure we have all the required fields
    if all(keys in ["email", "currency", "amount"] for keys in request.form.keys()):
        # Make sure we are withdrawing integers only
        if "." in str(request.form["amount"]):
            flash("Please withdraw WHOLE NUMBERS MAWDollars only")
            return redirect(url_for(".redeem"))

        requested_MAWDollars = int(request.form["amount"])
        current_balance = get_balance(session["username"])
        if current_balance < requested_MAWDollars:
            flash(f"You do not have enough MAWDollars. (Requested{request.form['amount']}. Have {current_balance})")
            return redirect(url_for(".redeem"))
        else:
            update_balance(session["username"], get_balance(session["username"]) - requested_MAWDollars)
            amount_currency = MAWDollars_to_currency(requested_MAWDollars, request.form["currency"])
            return render_template("payment/redeem_result.html", amount_MAWD=requested_MAWDollars,
                                                                 amount_currency=amount_currency,
                                                                 currency=request.form["currency"])
    else:
        flash("Please fill out al fields")
        return redirect(url_for(".redeem"))