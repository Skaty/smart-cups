class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.balance = 1000
        self.bets = {}

    def __str__(self):
        '''String representation of User'''
        return '{} (Balance: {})'.format(self.uid, self.balance)

    def print_all(self):
        print(self)
        print('Bets: {}'.format(self.bets))

    def update(self, resp):
        '''Update user according to API response'''
        if 'balance' in resp:
            self.balance = resp['balance']

    def add_bet(self, gid, rval, position):
        '''Adds a new bet'''
        self.bets[gid] = {
            'r': rval,
            'pos': position
        }

    def get_bet(self, gid):
        if gid in self.bets:
            return self.bets[gid]
        else:
            return None

    @staticmethod
    def from_response(resp):
        if 'user_id' not in resp:
            return None
        return User(resp['user_id'])