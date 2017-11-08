import math
import time

class Clock:
    def __init__(self, cycle_length):
        self.cycle_length = cycle_length
        self.first_tick = time.monotonic()

    def current_cycle(self):
        now = time.monotonic()
        return math.floor((now - self.first_tick) / self.cycle_length)
