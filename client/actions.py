from user import User

import connector, utils

class Actions(object):
    def __init__(self):
        self.tick = 0
        self.users = [User(x['id']) for x in connector.get_users()]
        self.games = []
        self.actions = {
            'cu': self.create_users,
            'cg': self.create_game,
            'claim': self.claim_game,
            'commit': self.commit_game,
            'forfeit': self.forfeit_game,
            'pg': self.print_all_games,
            'pu': self.print_all_users,
            'refund': self.refund_deposit,
            'reveal': self.reveal_position,
            'state': self.print_state,
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
            'refund': 'Refunds deposit to broker (after game ends)',
            'reveal': 'Broker reveals the position',
            'state': 'Prints the state of system',
            'tick': 'Advances PTC clock',
        }

    def prompt_choices(self, choice_fx, question_msg):
        num_choices = choice_fx()
        raw_value = input(question_msg)
        try:
            int_value = int(raw_value)
            if int_value >= 0 and int_value < num_choices:
                return int_value
            else:
                raise ValueError
        except ValueError:
            print('Invalid choice. Please try again!')
            return self.prompt_choices(choice_fx, question_msg)

    def create_users(self, num):
        num = int(num)
        self.users.extend([User.from_response(connector.create_user()) for i in range(num)])
        print("Created", num, "users!")

    def print_all_games(self):
        self.games = connector.get_games()
        for idx, game in enumerate(self.games):
            print(idx, ':', game)

        return len(self.games)

    def print_all_users(self):
        for idx, usr in enumerate(self.users):
            usr.update(connector.get_user(usr.uid))
            print(idx, ':', usr)

        return len(self.users)

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
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ') + 1
        game = self.games[gid - 1]

        usr_idx = self.prompt_choices(self.print_all_users, 'Please select a user who is committing: ')
        usr = self.users[usr_idx]

        rval = utils.random_r()
        usr.add_bet(gid, rval, guess)

        connector.commit_game(gid, usr.uid, game['salt'], rval, guess)

    def forfeit_game(self):
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ') + 1
        connector.forfeit_game(gid)

    def reveal_position(self):
        usr_idx = self.prompt_choices(self.print_all_users, 'Please select a user who is revealling: ')
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ') + 1
        usr = self.users[usr_idx]
        bet = usr.get_bet(gid)

        connector.reveal_position(gid, usr.uid, bet['r'], bet['pos'])

    def refund_deposit(self):
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ') + 1

        connector.refund_deposit(gid)

    def claim_game(self):
        gid = self.prompt_choices(self.print_all_games, 'Please select the game: ') + 1
        uid = self.prompt_choices(self.print_all_users, 'Please select a user who is claiming: ')
        usr = self.users[uid]
        bet_obj = usr.get_bet(gid)
        rval = '0'

        if bet_obj is None:
            rval = input('Please enter R value: ')
        else:
            rval = bet_obj['r']

        connector.claim_winnings(gid, usr.uid, rval)

    def print_state(self):
        print('====== LIST OF GAMES IN PTC ======')
        self.print_all_games()
        print('====== LIST OF USERS IN PTC ======')
        self.print_all_users()

    def tick_clock(self):
        connector.advance_clock()
        self.tick += 1
        print('Current tick:', self.tick)

