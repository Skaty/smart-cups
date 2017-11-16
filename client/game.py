def pretty_print_game(game):
    try:
        broker_id = game['broker']['id'][:6]
        bets = len(game['bets'])
        players = game['players_count']
        start_tick = game['initial_cycle']
        ended = game['ended']
        return 'Broker: {}, # bets: {}, # players: {}, Start: {}, Has Ended? {}'.format(broker_id, bets, players, start_tick, ended)
    except ValueError:
        return game