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
            'claim': self.claim_game,
            'commit': self.commit_game,
            'forfeit': self.forfeit_game,
            'pg': self.print_all_games,
            'pu': self.print_all_users,
            'tick': self.tick_clock,
        }
        self.helptext = {
            'cg' : 'Creates a new game (cg <number of cups> <player count> <winning position>)',
            'claim': 'Claim winnings from a game (claim)',
            'commit' : 'Commits a bet (commit <guess>)',
            'forfeit': 'Forfeits a game (forfeit)',
            'cu' : 'Creates a number of users',
            'pg': 'Prints all games',
            'pu' : 'Prints all users',
            'tick': 'Advances PTC clock',
        }

    def prompt_choices(self, choice_fx, question_msg):
        choice_fx()
        raw_value = input(question_msg)
        try:
            return int(raw_value)
        except ValueError:
            print('Invalid choice. Please try again!')
            return self.prompt_choices(choice_fx, limit, question_msg)

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
        broker_id = self.prompt_choices(self.print_all_users, 'Please select a user as a broker: ')

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
        g_idx = self.prompt_choices(self.print_all_games, 'Please select the game: ')
        game = self.games[g_idx]
        gid = game[1]['game_id']

        usr_idx = self.prompt_choices(self.print_all_users, 'Please select a user who is committing: ')
        usr = self.users[usr_idx]

        rval = utils.random_r()
        usr.add_bet(gid, rval, guess)

        connector.commit_game(gid, usr.uid, rval, guess)

    def forfeit_game(self):
        g_idx = self.prompt_choices(self.print_all_games, 'Please select the game: ')
        connector.forfeit_game(g_idx)

    def reveal_position(self):
        uid = self.prompt_choices(self.print_all_users, 'Please select a user who is revealling: ')
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ')
        bet = self.get_bet(g_idx)

        connector.reveal_position(gid, uid, bet['r'], bet['pos'])

    def refund_deposit(self):
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ')

        connector.refund_deposit(gid)

    def claim_game(self):
        g_idx = self.prompt_choices(self.print_all_games, 'Please select the game: ')
        usr_idx = self.prompt_choices(self.print_all_users, 'Please select a user who is claiming: ')
        rval = self.get_bet(g_idx)['r']

        connector.claim_winnings(g_idx, usr_idx, rval)

    def tick_clock(self):
        connector.advance_clock()
        self.tick += 1
        print('Current tick:', self.tick)

