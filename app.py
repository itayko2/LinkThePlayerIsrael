from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
from GameLogic import find_all_shared_teammates, all_players
app = Flask(__name__)

# List of target strings
# targets = ["Eitan Tibi", "Neta Lavi", "Omer Atzili", "Eran Zahavi", "Gal Alberman"]
players = all_players()


def get_players_by_number(number):
    with open('players.json', 'r') as f:
        data = json.load(f)
    return data[str(number)]['players'][0], data[str(number)]['players'][1]


def get_targets_by_number(number):
    with open('players.json', 'r') as f:
        data = json.load(f)
    return  data[str(number)]['shared_teammates']


# Index route that shows the game interface
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's guess from the form
        guess = request.form['guess']
        # Check if the guess is correct
        if guess.lower() in set([name.lower() for name in session['target']]):
            # Update the score
            session['score'] += 1
            # Update the guesses
            session['guesses'] = 5
            # Update the history
            session['history'] = []
            # Update the players
            session['player1'], session['player2'] = get_players_by_number(session['score'])

            # Next Level
            session['target'] = get_targets_by_number(session['score'])
            message = f"Can you find a player who played with" \
                      f" {session['player1']} and {session['player2']} ?"
        else:
            message = f"Wrong guess. Try again.\n Can you find a player who played with" \
                          f" {session['player1']} and {session['player2']} ?"
            # Add the guess to the history
            session['history'].append(guess)
            # Decrement the remaining guesses
            session['guesses'] -= 1
            # Check if the game is over
            if session['guesses'] == 0:
                return render_template('gameover.html',
                                       score=session['score'],
                                       history=session['history'],
                                       answers=find_all_shared_teammates(session['player1'], session['player2']))
    else:
        # Initialize the session variables
        session['score'] = 0
        session['level'] = 1
        session['guesses'] = 5
        session['history'] = []
        session['player1'], session['player2'] = get_players_by_number(session['score'])
        session['target'] = get_targets_by_number(session['score'])
        # Render the game interface
        message = f"Can you find a player who played with" \
                  f" {session['player1']} and {session['player2']} ?"

    # Render the game interface
    return render_template('index.html',
                           score=session['score'],
                           level=session['level'],
                           guesses=session['guesses'],
                           history=session['history'],
                           message=message,
                           targets=players)


# Reset route that resets the game
@app.route('/reset', methods=['POST'])
def reset():
    # Reset the session variables
    session['score'] = 0
    session['guesses'] = 5
    session['history'] = []
    session['player1'], session['player2'] = get_players_by_number(session['score'])
    session['target'] = get_targets_by_number(session['score'])
    # Render the game interface
    return redirect(url_for('index'))


# Start the Flask application
if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
