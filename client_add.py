import tkinter
from random import randint
from tkinter import CENTER
import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "Gate1"
# The broker name or IP address.
# broker = "192.168.56.1"
# broker = "127.0.0.1"
# broker = "10.0.0.1"
broker = "localhost"

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()


def send_message(mess):
    client.publish("card/id", mess + "." + terminal_id, )


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def draw_id():
    random_id = random_with_N_digits(6)  # losowe id
    # tu warto sprawdzić czy już go nie ma w bazie
    client.publish("card/id", str(random_id) + "." + terminal_id, )


def add_card_window():
    window.geometry("300x200")
    window.title("Add RFID Card")
    window.configure(bg="#353836")

    intro_label = tkinter.Label(window, text="Swipe your card here:", padx=15, pady=15, bg="#1d1f1d", fg="white",
                                width="200", font=("Sans-serif", 12, "bold"))
    intro_label.pack()

    add_button = tkinter.Button(window, text="SWIPE", command=lambda: draw_id(), padx=15, pady=15,
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
