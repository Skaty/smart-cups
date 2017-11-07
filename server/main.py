from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    return jsonify(user_id='this is random')

@app.route('/users/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(balance=100)

@app.route('/games', methods=['POST'])
def create_game():
    game_params = request.json

    print("Broker: {}".format(game_params['broker_id']))
    print("Cups: {}".format(game_params['cups_count']))
    print("Players: {}".format(game_params['players_count']))

    return jsonify(game_id=1)

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
