import json
from flask import Flask, render_template

from utils import enter_client, get_clients, increase_new_card_number, process_card, register_client

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("hello.html")
