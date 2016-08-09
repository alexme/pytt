"""
"""

from fsm import Fsm
from market.dealing import Order
from market.dealing import STATUS_EXEC

# consts
STATES = Enum('IDLE', 'SIGNAL', 'PL', 'CHECK_PL', 'STOPPED')

# book
class BookAsset:
    def __init__(self, instr):
        self.instr = instr
        self.cash = 0.0
        self.position = 0.0
        self.valo = None

    def to_num(self):
        return self.instr.to_num(self.position, self.valo) + self.cash

# class
class Algo(Fsm):
    def __init__(self, order_q, exec_q, ticker_traded, signal, pl_limit):
        # FSM
        t_tbl = { STATES.IDLE: self.trans_idle,
                  STATES.PL: self.trans_pl,
                  STATES.CHECK_PL: self.trans_check_pl,
                  STATES.SIGNAL: self.trans_signal,
                  STATES.STOPPED: self.trans_stop }
        to_tbl = { STATES.IDLE: self.to_idle }
        from_tbl = {}
        super().__init__(STATES.IDLE, t_tbl, from_tbl, to_tbl, [STATES.STOPPED])
        # TRADER
        self.pl_limit = pl_limit
        self.book = { a: BookAsset(a) for a in ticker_traded }
        self.pl_asset_last = { a: 0.0 for a in ticker_traded }
        self.pl_last = 0.0

    # algo run from idle to idle ie it is looping on idle state
    def one_loop(self, data):
        yield from self.next_to(data, STATES.IDLE)

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
    def trans_idle(self, data):
        if data.ticker not in self.positions:
            return STATES.SIGNAL
        return STATES.PL

    def trans_pl(self, data):
        if data.ticker in self.book:
            if self.book[data.ticker].position != 0:
                return STATES.CHECK_PL
        return STATES.SIGNAL

    def trans_check_pl(self, data):
        # we know that it s a traded asset
        self.book[data.ticker].valo = data.last
        self.pl_last = self.compute_pl()
        if self.pl_last < self.pl_limit:
            return STATES.STOPPED
        return STATES.SIGNAL

    def trans_signal(self, data):
        # change this
        ret = self.signal(data)
        if abs(ret) > 10:
            self.order_q.append(Order(data.ticker, -ret/abs(ret)))
        return STATES.IDLE
