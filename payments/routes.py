from flask import Blueprint, redirect, url_for, flash, session, render_template, request
from data.database_query import update_balance, get_balance

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
