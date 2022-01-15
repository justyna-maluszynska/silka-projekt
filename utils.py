import json
from random import choice

from config import CLIENTS_DATA_FILENAME, TERMINALS_DATA_FILENAME, ENTRANCES_HISTORY


def load_data(filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)

    return file_data


def get_clients():
    file_data = load_data(CLIENTS_DATA_FILENAME)

    return file_data["clients"]


def get_clients_id():
    all_clients = get_clients()
    all_clients_id = ""
    for cl in all_clients:
        all_clients_id += str(cl['card_number'])
        all_clients_id += " "
    return all_clients_id


def get_active_clients_id():
    active_clients = get_clients_on_gym()
    active_clients_id = ""
    for cl in active_clients:
        active_clients_id += str(cl['card_number'])
        active_clients_id += " "
    return active_clients_id


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


def get_history_of_all_entrances():
    file_data = load_data(ENTRANCES_HISTORY)
    return file_data["entrances"]


def get_history_of_clients_entrances(client_card_number: int):
    file_data = load_data(ENTRANCES_HISTORY)["entrances"]
    filtered_data = list(filter(lambda entrance: entrance["card_number"] == client_card_number, file_data))
    return filtered_data


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


def increment_next_card_number():
    current_next = get_new_card_number()
    file_data = load_data(CLIENTS_DATA_FILENAME)
    file_data['next_card_number'] = (current_next + 1)
    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def add_card_to_pending(terminal, date, time):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    file_data['pending'].append({
        "terminal": terminal,
        "date": date,
        "time": time,
        "card_number": get_new_card_number()
    })
    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)
    increment_next_card_number()


# usun oczekujaca karte z pending
def remove_pending_card(card_number):
    file_data = load_data(CLIENTS_DATA_FILENAME)
    pending = list(filter(lambda x: x["card_number"] != card_number, file_data['pending']))
    file_data['pending'] = pending

    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def add_to_unregister():
    file_data = load_data(CLIENTS_DATA_FILENAME)
    card_numbers = [x["card_number"] for x in file_data['clients']]
    card_number = choice(card_numbers)
    unregister_client = list(filter(lambda x: x["card_number"] == card_number, file_data['clients']))
    file_data['unregister'].append(unregister_client)
    with open(CLIENTS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def unregister(card_number):
    card_number = int(card_number)
    file_data = load_data(CLIENTS_DATA_FILENAME)
    unregister = list(filter(lambda x: x["card_number"] == card_number, file_data['unregister']))
    if len(unregister) > 0:
        clients = list(filter(lambda x: x["card_number"] != card_number, file_data['clients']))
        new_unregister_list = list(filter(lambda x: x["card_number"] != card_number, file_data['unregister']))
        file_data['clients'] = clients
        file_data['unregister'] = new_unregister_list
        with open(CLIENTS_DATA_FILENAME, 'w') as file:
            json.dump(file_data, file, indent=4)
            return True
    else:
        return False


def get_terminals():
    file_data = load_data(TERMINALS_DATA_FILENAME)
    return file_data["terminals"]


def add_terminal(new_id, gate_type):
    file_data = load_data(TERMINALS_DATA_FILENAME)
    terminal_with_id = list(filter(lambda x: x["terminal_id"] == new_id, file_data['terminals']))
    if len(terminal_with_id) > 0:
        return False
    else:
        file_data = load_data(TERMINALS_DATA_FILENAME)
        file_data['terminals'].append({
            "terminal_id": new_id,
            "type": gate_type
        })
        with open(TERMINALS_DATA_FILENAME, 'w') as file:
            json.dump(file_data, file, indent=4)
    return True


def remove_terminal(terminal_id):
    file_data = load_data(TERMINALS_DATA_FILENAME)
    terminals = list(filter(lambda x: x["terminal_id"] != terminal_id, file_data['terminals']))
    file_data['terminals'] = terminals

    with open(TERMINALS_DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


def validate_terminal(terminal_id):
    terminals = get_terminals()
    return any(terminal["terminal_id"] == terminal_id for terminal in terminals)
