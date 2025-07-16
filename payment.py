import razorpay
from flask import Blueprint, render_template, request, redirect, url_for

payment = Blueprint('payment', __name__)

# Replace with your Razorpay keys
razorpay_client = razorpay.Client(auth=("rzp_test_vF1ZbSA33iyWxi", "VgcwERiivrJUtbZV8pWWBbyW"))

@payment.route("/checkout")
def checkout():
    return render_template("checkout.html")

@payment.route("/create_order", methods=["POST"])
def create_order():
    amount = int(request.form["amount"]) * 100  # amount in paise
    payment_order = razorpay_client.order.create(dict(amount=amount, currency="INR", payment_capture=1))
    return render_template("checkout.html", order_id=payment_order["id"], amount=amount, key="YOUR_KEY_ID")

@payment.route("/payment_success", methods=["POST"])
def payment_success():
    return render_template("success.html")

@payment.route("/payment_failed")
def payment_failed():
    return render_template("failure.html")
