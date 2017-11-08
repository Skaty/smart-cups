from flask import Flask, jsonify, request
from server.bet import Bet
from server.clock import Clock
from server.game import Game
from server.user import make_user
from server.serializer import serialize_game

CYCLE_LENGTH = 60
BET = 1
REWARD = 2

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

    if broker.balance < players_count * REWARD:
        return jsonify(status='error', message='Broker does not have enough fund for deposit'), 422

    broker.balance -= players_count * REWARD

    game = Game(clock.current_cycle(), broker, salt, commitment, cups_count, players_count)
    games.append(game)

    return jsonify(game_id=len(games))

@app.route('/games/<int:game_id>', methods=['GET'])
def game_details(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    return jsonify(serialize_game(game))

@app.route('/games/<int:game_id>/commit', methods=['POST'])
def commit_guess(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    if game.cycles_elapsed(clock.current_cycle()) >= 2 or len(game.bets) >= game.players_count:
        return jsonify(status='error', message='Game is not accepting bets'), 422

    commit_params = request.json

    user_id = commit_params['user_id']
    if user_id not in users:
        return jsonify(status='error', message='User not found'), 404

    user = users[user_id]

    if user.balance < BET:
        return jsonify(status='error', message='User does not have enough fund'), 422

    user.balance        -= BET
    game.broker.balance += BET

    commitment = commit_params['commitment']

    bet = Bet(user, commitment)
    game.bets.append(bet)

    return jsonify(status='ok')

@app.route('/games/<game_id>/reveal', methods=['POST'])
def reveal_guess(game_id):
    reveal_params = request.json

    print("Player {} revealing guess {}".format(reveal_params['user_id'], reveal_params['guess']))

    return jsonify(status='ok')
