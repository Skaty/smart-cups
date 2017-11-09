from flask import Flask, jsonify, request
from server.bet import Bet
from server.clock import MockClock
from server.game import Game
from server.user import make_user
from server.serializer import serialize_game
from server.util import compute_commitment

CYCLE_LENGTH = 60
BET = 1
REWARD = 2

clock = MockClock(CYCLE_LENGTH)

users = {}
games = []

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def system_info():
    return jsonify(cycle=clock.current_cycle())

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

@app.route('/games/<int:game_id>/reveal', methods=['POST'])
def reveal_guess(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    cycles_elapsed = game.cycles_elapsed(clock.current_cycle())
    if (cycles_elapsed < 2 and len(game.bets) < game.players_count) or cycles_elapsed >= 4:
        return jsonify(status='error', message='Invalid action'), 422

    if game.position is not None:
        return jsonify(status='error', message='Invalid action'), 422

    reveal_params = request.json

    broker_id = reveal_params['broker_id']
    if broker_id != game.broker.id:
        return jsonify(status='error', message='Invalid user'), 403

    r = reveal_params['r']
    position = reveal_params['position']
    expected_commitment = compute_commitment(game.salt, r, position)

    if expected_commitment != game.commitment:
        return jsonify(status='error', message='Invalid commitment'), 422

    game.position = position

    return jsonify(status='ok')

@app.route('/games/<int:game_id>/claim', methods=['POST'])
def claim_reward(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    if game.position is None or game.cycles_elapsed(clock.current_cycle()) >= 6:
        return jsonify(status='error', message='Invalid action'), 422

    claim_params = request.json
    user_id = claim_params['user_id']
    r = claim_params['r']
    expected_commitment = compute_commitment(game.salt, r, game.position)

    for bet in game.bets:
        if not bet.claimed and bet.commitment == expected_commitment and bet.user.id == user_id:
            bet.user.balance += REWARD
            bet.claimed = True

    return jsonify(status='ok')

@app.route('/games/<int:game_id>/refund_deposit', methods=['POST'])
def refund_deposit(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    if game.cycles_elapsed(clock.current_cycle()) < 6 or game.ended:
        return jsonify(status='error', message='Invalid action'), 422

    game.ended = True

    winning_bets_count = sum(bet.claimed for bet in game.bets)
    refund_amount = (game.players_count - winning_bets_count) * REWARD
    game.broker.balance += refund_amount

    return jsonify(status='ok')

@app.route('/games/<int:game_id>/forfeit', methods=['POST'])
def forfeit_game(game_id):
    if game_id > len(games):
        return jsonify(status='error', message='Game not found'), 404

    game = games[game_id - 1]

    if game.cycles_elapsed(clock.current_cycle()) < 4 or game.position is not None or game.ended:
        return jsonify(status='error', message='Invalid action'), 422

    game.ended = True

    committed_bets_count = len(game.bets)
    payout_per_bet = game.players_count * REWARD / committed_bets_count

    for bet in game.bets:
        bet.user.balance += payout_per_bet

    return jsonify(status='ok')

@app.route('/clock/tick', methods=['POST'])
def next_tick():
    clock.tick()
    return jsonify(status='ok')
