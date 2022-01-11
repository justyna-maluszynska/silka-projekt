import json

from config import CLIENTS_DATA_FILENAME, TERMINALS_DATA_FILENAME


def load_data(filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)

    return file_data


def get_clients():
    file_data = load_data(CLIENTS_DATA_FILENAME)

    return file_data["clients"]


def get_clients_on_gym():
    file_data = load_data(CLIENTS_DATA_FILENAME)

    return file_data["active_clients"]


def get_new_card_number():
    file_data = load_data(CLIENTS_DATA_FILENAME)

    return file_data["next_card_number"]


def increase_new_card_number():
    file_data = load_data(CLIENTS_DATA_FILENAME)
    file_data["next_card_number"] += 1
    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def get_pending_cards():
    file_data = load_data(CLIENTS_DATA_FILENAME)
    return file_data["pending"]


def get_client_data(card_number: int):
    clients = get_clients()
    client_data = list(
        filter(lambda x: x["card_number"] == card_number, clients))[0]
    return client_data


# dodaj nowego klienta
def register_client(new_name, new_surname, new_birthday, card_number):
    clients = load_data(CLIENTS_DATA_FILENAME)
    clients['clients'].append({
        "name": new_name,
        "surname": new_surname,
        "date_of_birth": new_birthday,
        "card_number": card_number
    })

    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(clients, file, indent=4)


# klient wchodzi na siłkę
def enter_client(card_number, entry_time, client_data):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    file_data['active_clients'].append({
        "name": client_data["name"],
        "surname": client_data["surname"],
        "card_number": card_number,
        "entry_time": entry_time
    })

    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


# klient wychodzi z siłki
def get_away_client(card_number):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    active_clients = list(filter(lambda x: x["card_number"] != card_number, file_data['active_clients']))
    file_data['active_clients'] = active_clients

    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


# przetwarzanie karty
def process_card(card_number, time):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    client = list(filter(lambda x: x["card_number"] == card_number, file_data['active_clients']))

    if len(client) > 0:
        get_away_client(card_number)
    else:
        enter_client(card_number, time, client[0])


# usun oczekujaca karte z pending
def remove_pending_card(card_number):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    pending = list(filter(lambda x: x["card_number"] != card_number, file_data['pending']))
    file_data['pending'] = pending

    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def get_terminals():
    file_data = load_data(TERMINALS_DATA_FILENAME)
    return file_data["terminals"]


def add_terminal(new_id, gate_type):
    file_data = load_data(TERMINALS_DATA_FILENAME)
    file_data['terminals'].append({
        "terminal_id": new_id,
        "type": gate_type
    })
    with open(TERMINALS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def remove_terminal(terminal_id):
    file_data = load_data(TERMINALS_DATA_FILENAME)
    terminals = list(filter(lambda x: x["terminal_id"] != terminal_id, file_data['terminals']))
    file_data['terminals'] = terminals

    with open(TERMINALS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


