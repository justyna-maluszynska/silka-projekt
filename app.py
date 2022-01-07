import json
from flask import Flask, render_template

from utils import enter_client, get_clients, increase_new_card_number, process_card, register_client, get_clients_on_gym

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/addclient")
def add_client():
    return render_template("addclient.html")

@app.route("/addgate")
def add_gate():
    return render_template("addgate.html")

@app.route("/clients")
def clients():
    clients = get_clients()
    return render_template("clients.html", clients=clients)

@app.route("/ongym")
def on_gym():
    clients = get_clients_on_gym()
    return render_template("ongym.html", clients=clients)
