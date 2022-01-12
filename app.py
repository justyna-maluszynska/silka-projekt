from flask import Flask, render_template, request

from flask_mqtt import Mqtt
from config import BROKER_URL
from utils import *
import time

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = BROKER_URL

terminal_id = "MASTER"
client = Mqtt(app)


# zacznij subskrybować temat od razu po połączeniu z brokerem
@client.on_connect()
def handle_connect(client, userdata, flags, rc):
    client.subscribe('card/id')


# metoda dla konkretnego tematu
@client.on_topic('card/id')
def handle_card_id(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if message_decoded[1] == "GET_ACTIVE":
        active_clients = get_active_clients_id()
        all_clients = get_clients_id()
        client.publish("card/list", all_clients + "." + "ALL", )
        client.publish("card/list", active_clients + "." + "ACTIVE", )
    elif message_decoded[1] == "ACTIVATE":
        print(time.ctime() + ", " + message_decoded[0] + " used the RFID card to " + message_decoded[1])
        t = time.ctime().split()
        client = get_client_data(int(message_decoded[0]))
        enter_client(int(message_decoded[0]), t[3], client)
    elif message_decoded[1] == "DEACTIVATE":
        print(time.ctime() + ", " + message_decoded[0] + " used the RFID card to " + message_decoded[1])
        get_away_client(int(message_decoded[0]))
    else:
        print(message_decoded[0] + " : " + message_decoded[1])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/addcard")
def add_card():
    pending_cards = get_pending_cards()
    return render_template("addcard.html", pending_cards=pending_cards)


@app.route("/addcard-form/<card_number>")
def add_card_form(card_number):
    return render_template("addclientform.html", card_number=card_number)


@app.route("/addgate")
def add_gate():
    return render_template("addgate.html")


@app.route("/addgate_handle", methods=['POST'])
def addgate_handle():
    new_id = request.form['terminal_id']
    gate_type = request.form['type']
    add_terminal(new_id, gate_type)
    return terminals()


@app.route('/<terminal_id>/remove_gate')
def remove_gate(terminal_id):
    remove_terminal(terminal_id)
    return terminals()


@app.route("/clients")
def clients():
    clients = get_clients()
    return render_template("clients.html", clients=clients)


@app.route("/addclient_handle", methods=['POST'])
def addclient_handle():
    new_name = request.form['client_name']
    new_surname = request.form['client_surname']
    new_birthday = request.form['client_birthday']
    card_number = int(request.form['card_number'])
    register_client(new_name, new_surname, new_birthday, card_number)
    remove_pending_card(card_number)
    return add_card()


@app.route("/terminals")
def terminals():
    terminals = get_terminals()
    return render_template("terminals.html", terminals=terminals)


@app.route("/ongym")
def on_gym():
    clients = get_clients_on_gym()
    return render_template("ongym.html", clients=clients)


if __name__ == "__main__":
    app.run()
