def serialize_user(user):
    return { 'id': user.id, 'balance': user.balance }

def serialize_bet(bet):
    return { 'user': serialize_user(bet.user), 'commitment': bet.commitment }

def serialize_game(game):
    return {
        'initial_cycle': game.initial_cycle,
        'broker': serialize_user(game.broker),
        'salt': game.salt,
        'commitment': game.commitment,
        'cups_count': game.cups_count,
        'players_count': game.players_count,
        'position': game.position,
        'bets': list(map(serialize_bet, game.bets))
    }
