"""
an Algo in an FSM which :
- computes its pl through a book
- send orders according to a stream2order callable
- acknowledges execs and update position accordingly
- runs from idle to idle state
- can be monitored
"""

from enum import Enum

from .fsm import Fsm
# from ..market.dealing import Order
# from ..market.dealing import STATUS_EXEC
# from ..streams.abstract import STREAM_TYPE

# consts
ALGO_STATES = Enum('Algo_States', ['IDLE', 'SIGNAL', 'PL', 'CHECK_PL', 'STOPPED'])

#stream2order
class Stream2Order:
    def __init__(self, stream_id, logic):
        self.sid = stream_id
        self.logic = logic

    def __call__(self, data):
        return self.logic(data)

# book
class BookAsset:
    def __init__(self, instr):
        self.instr = instr
        self.cash = 0.0
        self.position = 0.0
        self.last = None
        self.pl_last = 0.0

    def to_num(self):
        return self.instr.to_num(self.position, self.last) + self.cash

    def update_last(self, last):
        self.last = last
        self.pl_last = self.to_num()

# class
class Algo(Fsm):
    def __init__(self, order_q, exec_q, ticker_traded, signal, pl_limit):
        # FSM
        t_tbl = { ALGO_STATES.IDLE: self.trans_idle,
                  ALGO_STATES.PL: self.trans_pl,
                  ALGO_STATES.CHECK_PL: self.trans_check_pl,
                  ALGO_STATES.SIGNAL: self.trans_signal,
                  ALGO_STATES.STOPPED: self.trans_stop }
        to_tbl = { ALGO_STATES.IDLE: self.to_idle }
        from_tbl = {}
        super().__init__(ALGO_STATES.IDLE, t_tbl, from_tbl, to_tbl, [ALGO_STATES.STOPPED])
        # TRADER
        self.pl_limit = pl_limit
        self.book = { a: BookAsset(a) for a in ticker_traded }
        self.pl_last = 0.0

    # algo run from idle to idle ie it is looping on idle state
    def one_loop(self, data):
        yield from self.next_to(data, ALGO_STATES.IDLE)

    # pl
    def compute_pl(self):
        # can use reduce here
        pl = 0.0
        for k, v in self.book.items():
            pl += v.to_num()
        return pl

    # end transition fun
    def to_idle(self, data):
        """ we check exec before idle state """
        while self.exec_q:
            e = self.exec_q.pop()
            if e.status != STATUS_EXEC.DONE:
                continue
            cash_amt = self.book[e.ticker].instr.to_num(e.qty, e.price)
            self.book[e.ticker].cash += cash_amt
            self.book[e.ticker].position += e.qty

    #fonctions de transition
    def trans_stop(self, data):
        return ALGO_STATES.STOPPED

    def trans_idle(self, data):
        if data.type == STREAM_TYPE.DATA:
            pass
        if data.ticker not in self.positions:
            return ALGO_STATES.SIGNAL
        return ALGO_STATES.PL

    def trans_pl(self, data):
        if data.ticker in self.book:
            if self.book[data.ticker].position != 0:
                return ALGO_STATES.CHECK_PL
        return ALGO_STATES.SIGNAL

    def trans_check_pl(self, data):
        # we know that it s a traded asset
        self.book[data.ticker].valo = data.last
        self.pl_last = self.compute_pl()
        if self.pl_last < self.pl_limit:
            return ALGO_STATES.STOPPED
        return ALGO_STATES.SIGNAL

    def trans_signal(self, data):
        # change this
        ret = self.signal(data)
        if abs(ret) > 10:
            self.order_q.append(Order(data.ticker, -ret/abs(ret)))
        return ALGO_STATES.IDLE
