from enum import Enum

CYCLES_PER_STAGE = 2

class GameState(Enum):
    # Waiting for more players to join (by committing a guess).
    COMMITTING = 1

    # We have enough players now. Waiting for the broker to reveal his position.
    REVEALING = 2

    # Winning players can claim their payout by revealing their guesses.
    CLAIMING = 3

    # The game has ended. Remaining funds have been returned to the broker.
    ENDED = 4

    # Broker did not reveal on time. The deposit is released to the players.
    FORFEIT = 5

class Game:
    def __init__(self, initial_cycle, broker, salt, commitment, cups_count, players_count):
        self.initial_cycle = initial_cycle
        self.broker        = broker
        self.salt          = salt
        self.commitment    = commitment
        self.cups_count    = cups_count
        self.players_count = players_count
        self.position      = None
        self.bets          = []

    def current_state(self, current_cycle):
        pass

    def add_bet(self, bet):
        if len(self.bets) >= self.players_count:
            return False

        self.bets.append(bet)

        if len(self.bets) == self.players_count:
            self.state = GameState.REVEALING

        return True
