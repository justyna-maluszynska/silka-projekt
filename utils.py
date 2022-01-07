import json

from config import DATA_FILENAME


def load_data():
    with open(DATA_FILENAME, 'r+') as file:
        file_data = json.load(file)

    return file_data


def get_clients():
    file_data = load_data()

    return file_data["clients"]

def get_clients_on_gym():
    file_data = load_data()

    return file_data["active_clients"]


def get_new_card_number():
    file_data = load_data()

    return file_data["next_card_number"]


def increase_new_card_number():
    file_data = load_data()
    file_data["next_card_number"] += 1
    with open(DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


#dodaj nowego klienta
def register_client(new_client):
    clients = get_clients()
    clients.append(new_client)
    with open(DATA_FILENAME, 'w') as file:
        json.dump(clients, file, indent=4)


def get_client_data(card_number: int):
    clients = get_clients()
    client_data = list(
        filter(lambda x: x["card_number"] == card_number, clients))[0]
    return client_data


#klient wchodzi na siłkę
def enter_client(card_number, entry_time, client_data):
    file_data = load_data()
    file_data['active_clients'].append({
        "name": client_data["name"],
        "surname": client_data["surname"],
        "card_number": card_number,
        "entry_time": entry_time
    })

    with open(DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


#klient wychodzi z siłki
def get_away_client(card_number):
    file_data = load_data()
    active_clients = list(filter(lambda x: x["card_number"] != card_number, file_data['active_clients']))
    file_data['active_clients'] = active_clients

    with open(DATA_FILENAME, 'w') as file:
        json.dump(file_data, file, indent=4)


#przetwarzanie karty 
def process_card(card_number, time):
    file_data = load_data()
    client = list(filter(lambda x: x["card_number"] == card_number, file_data['active_clients']))
    
    if len(client) > 0:
        get_away_client(card_number)
    else:
        enter_client(card_number, time, client[0])