import json
from GameLogic import find_all_shared_teammates
import os


questions = {"0": ['Omer Atzili', 'Eran Zahavi'],
             "1": ['Eitan Tibi', 'Itamar Shviro'],
             "2": ["Dor Peretz", 'Tomer Hemed'],
             "3": ['Guy Melamed', 'Dan Biton'],
             "4": ['Niv Zrihan', 'Josh Cohen'],
             "5": ['Eran Zahavi', 'Hanan Maman'],
             "6": ['Nir Bitton', 'Shoval Gozlan'],
             "7": ['Dor Peretz', 'Ofek Biton'],
             "8": ['Ofir Kriaf', 'Frantzdy Pierrot']}


def add_shared_teammates_to_json(player1, player2, record_name):
    # Call the find_shared_teammates function to get the shared teammates
    shared_teammates = find_all_shared_teammates(player1, player2)

    # Create a new data dict if the file doesn't exist
    if not os.path.isfile('players.json'):
        data = {}
    else:
        # Load the existing data from the JSON file
        with open('players.json', 'r') as f:
            data = json.load(f)

    # Check if the record already exists in the data
    if record_name in data:
        # If it does, update the list of shared teammates
        data[record_name]['players'].append(player1)
        data[record_name]['players'].append(player2)
        data[record_name]['shared_teammates'] += shared_teammates
    else:
        # If it doesn't, add a new record with the shared teammates
        data[record_name] = {'players': [player1, player2], 'shared_teammates': shared_teammates}

    # Write the updated data back to the JSON file
    with open('players.json', 'w') as f:
        json.dump(data, f)


def main():

    for key in questions:
        players = questions[key]
        add_shared_teammates_to_json(player1=players[0], player2=players[1], record_name=key)


if __name__ == "__main__":
    main()

