"""
a signal is a callable with persisted state
"""

from collections import deque

class Signal():
    def __call__(self, data):
        return None


class AvgSignal:
    """
    pretty useless can adapt to Z score signal
    """
    def __init__(self, l):
        self.q = deque()
        self.max_len = l
        self.m = 0.0

    def __call__(self, value):
        if len(self.q) < self.max_len:
            self.q.append(value)
            self.m += value
            if len(self.q) == self.max_len:
                return value - self.m / self.max_len
            return 0.0
        old_val = self.q.popleft()
        self.m += value - old_val
        self.q.append(value)
        return value - self.m / self.max_len
