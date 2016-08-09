"""
Interface for assets
"""

class Asset:
    def __init__(self, ticker):
        self.ticker = ticker

    def to_num(self, qty, level):
        return None


class Fut(Asset):
    def __init__(self, ticker, pv):
        super().__init__(ticker)
        self.pv = pv

    def to_num(self, qty, level):
        return - self.pv * qty * level