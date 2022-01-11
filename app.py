from flask import Flask, render_template, request

# from flask_mqtt import Mqtt
from config import BROKER_URL
from utils import get_clients, get_clients_on_gym, get_terminals, add_terminal, remove_terminal

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = BROKER_URL


# client = Mqtt(app)
#
#
# #zacznij subskrybować temat od razu po połączeniu z brokerem
# @client.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     client.subscribe('card/id')
#
#
# #metoda dla konkretnego tematu
# @client.on_topic('card/id')
# def handle_card_id(client, userdata, message):
#     # Decode message.
#     message_decoded = (str(message.payload.decode("utf-8"))).split(".")
#
#     # Print message to console.
#     if message_decoded[0] != "Client connected" and message_decoded[
#             0] != "Client disconnected":
#         print(time.ctime() + ", " + message_decoded[0] +
#               " used the RFID card.")
#     else:
#         print(message_decoded[0] + " : " + message_decoded[1])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/addclient")
def add_client():
    return render_template("addclient.html")


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


@app.route("/terminals")
def terminals():
    terminals = get_terminals()
    return render_template("terminals.html", terminals=terminals)


@app.route("/ongym")
def on_gym():
    clients = get_clients_on_gym()
    return render_template("ongym.html", clients=clients)
