import tkinter
from random import randint
from tkinter import CENTER
import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()


def send_message(mess):
    client.publish("card/id", mess + "." + terminal_id, )


def get_random_id_from_db():
    #kod wyciągania dostępnych id z bazy i losowania jedengo
    return "123456"


def get_active():
    #kod wyciągania listy osob obecnie na silowni
    return "list"


def send_id():
    random_id = get_random_id_from_db()  # losowe id z istniejących w baze
    active_list = get_active()  # lista osób obecnie na silowni
    # sprawdzenie czy dana osoba jest i odpowiednia informacja zwrotna
    client.publish("card/id", "jakies info" + "." + terminal_id, )


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
