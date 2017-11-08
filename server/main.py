from flask import Flask, jsonify, request
from server.clock import Clock
from server.game import Game
from server.user import make_user

CYCLE_LENGTH = 30

clock = Clock(CYCLE_LENGTH)

users = {}
games = []

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    user = make_user()
    users[user.id] = user
    return jsonify(user_id=user.id)

@app.route('/users/<user_id>', methods=['GET'])
def user_details(user_id):
    if user_id not in users:
        return jsonify(status='error', message='User not found'), 404

    user = users[user_id]
    return jsonify(balance=user.balance)

@app.route('/games', methods=['POST'])
def create_game():
    game_params = request.json

    user_id = game_params['user_id']
    if user_id not in users:
        return jsonify(status='error', message='User not found'), 404

    broker        = users[user_id]
    salt          = game_params['salt']
    commitment    = game_params['commitment']
    cups_count    = game_params['cups_count']
    players_count = game_params['players_count']

    game = Game(clock.current_cycle(), broker, salt, commitment, cups_count, players_count)
    games.append(game)

    return jsonify(game_id=len(games))

@app.route('/games/<game_id>/commit', methods=['POST'])
def commit_guess(game_id):
    commit_params = request.json

    print("Player {} commiting guess: {}".format(commit_params['user_id'], commit_params['commitment']))

    return jsonify(status='ok')

@app.route('/games/<game_id>/reveal', methods=['POST'])
def reveal_guess(game_id):
    reveal_params = request.json

    print("Player {} revealing guess {}".format(reveal_params['user_id'], reveal_params['guess']))

    return jsonify(status='ok')
