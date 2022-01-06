import json
from flask import Flask, render_template

from utils import enter_client, get_clients, increase_new_card_number, process_card, register_client

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("hello.html")

@app.route("/addclient")
def add_client():
    return render_template("addclient.html")

@app.route("/addgate")
def add_gate():
    return render_template("addgate.html")

@app.route("/clients")
def clients():
    return render_template("clients.html")

@app.route("/ongym")
def on_gym():
    return render_template("ongym.html")
