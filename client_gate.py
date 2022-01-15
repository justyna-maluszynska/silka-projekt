import random
import time
import tkinter


from tkinter import CENTER
import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "Gate3"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

active_list = []
random_card = 0

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()


def send_message(mess):
    client.publish("card/check/" + terminal_id, terminal_id + "." + mess, 2)


def send_id():
    global active_list
    global random_card
    send_message("GET_ACTIVE")
    client.on_message = process_message
    time.sleep(1)
    if random_card in active_list:
        send_message("DEACTIVATE" + "." + str(random_card))
    else:
        send_message("ACTIVATE" + "." + str(random_card))


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    print(message_decoded[0] + " : " + message_decoded[1])
    a_list = message_decoded[0].split()

    if message_decoded[1] == "ALL":
        client_list = a_list
        global random_card
        random_card = random.choice(client_list)
    else:
        global active_list
        active_list = a_list


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
    client.subscribe(("card/check/+", 2))
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
