import time

from flask import Flask, render_template, request, redirect, url_for
from flask_mqtt import Mqtt

from config import BROKER_URL
from utils import *

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = BROKER_URL

terminal_id = "MASTER"
client = Mqtt(app)


# zacznij subskrybować temat od razu po połączeniu z brokerem
@client.on_connect()
def handle_connect(client, userdata, flags, rc):
    client.subscribe(("card/check/+", 2))
    client.subscribe(("card/register/+", 2))


# metoda dla konkretnego tematu
@client.on_topic("card/check/+")
def handle_card_id(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if message_decoded[1] == "GET_ACTIVE":
        if validate_terminal(message_decoded[0]):
            active_clients = get_active_clients_id()
            all_clients = get_clients_id()
            client.publish("card/check/" + terminal_id, all_clients + "." + "ALL", )
            client.publish("card/check/" + terminal_id, active_clients + "." + "ACTIVE", )
        else:
            pass
    elif message_decoded[1] == "ACTIVATE":
        if validate_terminal(message_decoded[0]):
            print(time.ctime() + ", " + message_decoded[2] + " used the RFID card to " + message_decoded[1]
                  + " : " + message_decoded[0])
            t = time.ctime().split()
            client_a = get_client_data(int(message_decoded[2]))
            enter_client(int(message_decoded[2]), t[3], client_a)
        else:
            pass
    elif message_decoded[1] == "DEACTIVATE":
        if validate_terminal(message_decoded[0]):
            print(time.ctime() + ", " + message_decoded[2] + " used the RFID card to " + message_decoded[1]
                  + " : " + message_decoded[0])
            get_away_client(int(message_decoded[2]))
        else:
            pass
    else:
        print(message_decoded[0] + " : " + message_decoded[1])


# metoda dla konkretnego tematu
@client.on_topic("card/register/+")
def handle_add_card(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if message_decoded[1] == "ADD":
        if validate_terminal(message_decoded[0]):
            print(
                message_decoded[0] + " : " + message_decoded[1] + ' : ' + message_decoded[2] + " : " + message_decoded[
                    3])
            add_card_to_pending(message_decoded[0], message_decoded[2], message_decoded[3])
        else:
            pass
    if message_decoded[1] == "REMOVE":
        if validate_terminal(message_decoded[0]):
            print(
                message_decoded[0] + " : " + message_decoded[1] + ' : ' + message_decoded[2] + " : " + message_decoded[
                    3])
            add_to_unregister()
        else:
            pass
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
    if add_terminal(new_id, gate_type):
        return terminals()
    else:
        return render_template("message.html", message="Terminal o podanej nazwie już istnieje")


@app.route('/<terminal_id>/remove_gate')
def remove_gate(terminal_id):
    remove_terminal(terminal_id)
    return terminals()


@app.route('/remove_client/<client_card_number>')
def remove_client(client_card_number):
    if unregister(client_card_number):
        return clients()
    else:
        return render_template("message.html", message="Karta nie znajduje sie na liście wyrejestrowanych. Przeciągnij ponownie przez czytnik")


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


@app.route("/history")
def history():
    entrances = get_history_of_all_entrances()
    return render_template("history.html", entrances=entrances)


@app.route("/history-of-client/<client_card_number>")
def history_of_client(client_card_number):
    entrances = get_history_of_clients_entrances(int(client_card_number))
    return render_template("history.html", entrances=entrances)


@app.route("/history/generate", methods=['POST'])
def history_generate():
    convert_to_csv()
    entrances = get_history_of_all_entrances()
    return render_template("history.html", entrances=entrances)


if __name__ == "__main__":
    app.run()
