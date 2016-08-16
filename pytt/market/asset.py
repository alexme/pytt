"""
Instrument core class definition
an instrument is a tradable asset I think
"""

from enum import Enum

from ..streams.utils import coroutine

class Instrument:
    def __init__(self, asset):
        self.asset = asset
        self.orders = []

    def send_order(self, qty):
        self.orders.append(self._o(qty))

    @coroutine
    def _o(self, qty):
        """
        very simple here the market gives us a status
        which is always done and a price
        we could imagine a much more complicated logic
        this method would then probably comprise a couple of yield
        statements instead of only 2
        """
        status, pce = (yield)
        yield (self.asset, qty, pce)

class Asset:
    def __init__(self, ticker):
        self.ticker = ticker

    def to_num(self, qty, level):
        return None


class Future(Asset):
    def __init__(self, ticker, pv):
        super().__init__(ticker)
        self.pv = pv

    def to_num(self, qty, level):
        return - self.pv * qty * level
