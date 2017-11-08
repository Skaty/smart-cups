from uuid import uuid4 as uuid

INITIAL_BALANCE = 1000

class User:
    def __init__(self, id, balance = INITIAL_BALANCE):
        self.id = id
        self.balance = balance

def make_user():
    return User(uuid().hex)
