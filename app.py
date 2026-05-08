import os
import stripe
from flask import Flask, render_template_string, request, redirect

stripe.api_key = "sk_test_51P6WshRu8vW8f7fTM85H1pBeH7O20Z248p1mE7m4w7Y8u2u6Z5y3O1p9X8e7r6t5"

app = Flask(_name_)

@app.route('/')
def index():
    return '<body style="font-family:sans-serif;text-align:center;padding:50px;"><h1>Detector Muzica AI - 1€</h1><form action="/pay" method="POST"><button style="padding:10px 20px;background:#6772e5;color:white;border:none;border-radius:5px;cursor:pointer;" type="submit">Plateste 1€ si Verifica</button></form></body>'

@app.route('/pay', methods=['POST'])
def pay():
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': 'Verificare AI'}, 'unit_amount': 100}, 'quantity': 1}],
        mode='payment',
        success_url=request.host_url + 'upload?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.host_url
    )
    return redirect(session.url, code=303)

@app.route('/upload')
def upload():
    return '<h1>Plata reusita!</h1><p>Incarca fisierul (Sistemul de analiza se incarca...)</p><a href="/">Inapoi</a>'

if _name_ == "_main_":
    app.run()
