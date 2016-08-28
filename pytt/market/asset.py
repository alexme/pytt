"""
Instrument core class definition
an instrument is a tradable asset I think
"""

from enum import Enum

from ..streams.utils import coroutine
from .dealing import ORDER_STATUS
from .dealing import EXEC_STATUS
from .dealing import DONE_STATUS

class Instrument:
    def __init__(self, asset):
        self.asset = asset
        self.orders = []
        self.mkt = None # no market binded not tradable

    def send_order(self, order_tpe, qty):
        cr = self._o(order_tpe, qty)
        self.orders.append(cr)
        return cr

    # @coroutine
    # def _o(self, qty):
    #     """
    #     very simple here the market gives us a status
    #     which is always done and a price
    #     we could imagine a much more complicated logic
    #     this method would then probably comprise a couple of yield
    #     statements instead of only 2
    #     """
    #     status, pce = (yield)
    #     yield (self, qty, pce)

    @coroutine
    def _o(self, status, qty):
        yield
        while True:
            # here we can imagine more complex execs pce would
            # then be a more complex structure
            status, pce = (yield (status, qty))
            if status in DONE_STATUS:
                break
            yield
        # here cancel order book ? should be ok as orders are popped from market
        return (status, pce, qty)

    # to be tradable an instrumen needs to be binded to a MarketStream
    # which will take car of the exec
    def _bind_market(self, mkt):
        self.mkt = mkt

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
