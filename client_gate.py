import random
import tkinter
from tkinter import CENTER
import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "Gate1"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"


class Record:
    active_list = []
    random_card = 101  # Access through class


current_record = Record()

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()


def send_message(mess):
    client.publish("card/id", terminal_id + "." + mess, )


def send_id():
    send_message("GET_ACTIVE")
    client.on_message = process_message
    if current_record.random_card in current_record.active_list:
        client.publish("card/id", str(current_record.random_card) + "." + "DEACTIVATE", )
    else:
        client.publish("card/id", str(current_record.random_card) + "." + "ACTIVATE", )


def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    if message_decoded[1] == "ALL":
        print(message_decoded[0] + " : " + message_decoded[1])
        a_list = message_decoded[0].split()
        map_object = map(int, a_list)
        client_list = list(map_object)
        current_record.random_card = random.choice(client_list)
    else:
        print(message_decoded[0] + " : " + message_decoded[1])
        a_list = message_decoded[0].split()
        map_object = map(int, a_list)
        current_record.active_list = list(map_object)


def add_card_window():
    window.geometry("300x200")
    window.title("Gym Gate")
    window.configure(bg="#353836")

    intro_label = tkinter.Label(window, text="Swipe your card here:", padx=15, pady=15, bg="#1d1f1d", fg="white",
                                width="200", font=("Sans-serif", 12, "bold"))
    intro_label.pack()

    add_button = tkinter.Button(window, text="SWIPE", command=lambda: send_id(), padx=15, pady=15,
                                bg="#36802d", fg="white", font=("Sans-serif", 14, "bold"))
    add_button.place(relx=0.5, rely=0.5, anchor=CENTER)


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    client.loop_start()
    # Set subscriber
    client.subscribe('card/list')
    print("anything")
    # Send message about conenction.
    send_message("Client connected")


def disconnect_from_broker():
    # Send message about disconenction.
    send_message("Client disconnected")
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_sender():
    connect_to_broker()

    # create_main_window()
    add_card_window()

    # Start to display window (It will stay here until window is displayed)
    window.mainloop()

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
