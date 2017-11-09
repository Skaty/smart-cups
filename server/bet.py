from enum import Enum

class BetState(Enum):
    PENDING = 1
    CLAIMED = 2

class Bet:
    def __init__(self, user, commitment):
        self.state = BetState.PENDING
        self.user = user
        self.commitment = commitment
        self.claimed = False
