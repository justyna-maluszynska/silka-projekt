import time
import tkinter
from datetime import date
from random import randint
from tkinter import CENTER

import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "Gate1"
# The broker name or IP address.
broker = "192.168.56.1"
# broker = "127.0.0.1"
# broker = "10.0.0.1"
# broker = "localhost"

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()


def send_message(mess):
    client.publish("card/register/" + terminal_id, terminal_id + "." + mess, 0)


def send_date():
    currTime = time.ctime().split()
    today = date.today()
    d = today.strftime("%d-%m-%Y")
    unregister = randint(0, 100)
    if unregister > 80:
        send_message('REMOVE' + '.' + d + '.' + currTime[3])
    else:
        send_message('ADD' + '.' + d + '.' + currTime[3])


def add_card_window():
    window.geometry("300x200")
    window.title("Add RFID Card")
    window.configure(bg="#353836")

    intro_label = tkinter.Label(window, text="Swipe your card here:", padx=15, pady=15, bg="#1d1f1d", fg="white",
                                width="200", font=("Sans-serif", 12, "bold"))
    intro_label.pack()

    add_button = tkinter.Button(window, text="SWIPE", command=lambda: send_date(), padx=15, pady=15,
                                bg="#f07f13", fg="white", font=("Sans-serif", 14, "bold"))
    add_button.place(relx=0.5, rely=0.5, anchor=CENTER)


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    # Send message about conenction.
    send_message("Client connected")


def disconnect_from_broker():
    # Send message about disconenction.
    send_message("Client disconnected")
    # Disconnet the client.
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
