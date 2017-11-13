from user import User

import connector, utils

class Actions(object):
    def __init__(self):
        self.tick = 0
        self.users = []
        self.games = []
        self.actions = {
            'cu': self.create_users,
            'cg': self.create_game,
            'commit': self.commit_game,
            'pg': self.print_all_games,
            'pu': self.print_all_users,
            'tick': self.tick_clock,
        }
        self.helptext = {
            'cg' : 'Creates a new game (cg <number of cups> <player count> <winning position>)',
            'commit' : 'Commits a bet (commit <guess>)',
            'cu' : 'Creates a number of users',
            'pg': 'Prints all games',
            'pu' : 'Prints all users',
            'tick': 'Advances PTC clock',
        }

    def create_users(self, num):
        num = int(num)
        self.users.extend([User.from_response(connector.create_user()) for i in range(num)])
        print("Created", num, "users!")

    def print_all_games(self):
        for idx, game in enumerate(self.games):
            print(idx, ':', game)

    def print_all_users(self):
        for idx, usr in enumerate(self.users):
            usr.update(connector.get_user(usr.uid))
            print(idx, ':', usr)

    def create_game(self, num_cups, num_players, position):
        self.print_all_users()
        broker_id = int(input('Please select a user as a broker: '))

        if broker_id < 0 or broker_id >= len(self.users):
            print('Choice invalid!')
            return

        usr = self.users[broker_id]
        num_cups = int(num_cups)
        num_players = int(num_players)
        rval = utils.random_r()
        position = int(position)

        new_game_obj = connector.create_game(usr.uid, num_cups, num_players, rval, position)

        self.games.append(new_game_obj)
        usr.add_bet(new_game_obj[1]['game_id'], rval, position)

        print('Created game:', new_game_obj[1]['game_id'])

    def commit_game(self, guess):
        guess = int(guess)
        self.print_all_games()
        g_idx = int(input('Please select the game: '))
        game = self.games[g_idx]
        gid = game[1]['game_id']

        self.print_all_users()
        usr_idx = int(input('Please select a user who is committing: '))
        usr = self.users[usr_idx]

        rval = utils.random_r()
        usr.add_bet(gid, rval, guess)

        connector.commit_game(gid, usr.uid, rval, guess)

    def tick_clock(self):
        connector.advance_clock()
        self.tick += 1
        print('Current tick:', self.tick)

