"""
"""

from fsm import Fsm

# consts
STATES = Enum('IDLE', 'SIGNAL', 'PL', 'CHECK_PL', 'STOPPED')

# book
class BookAsset:
    def __init__(self, ticker, Instr):
        self.ticker = ticker
        self.instr = Instr
        self.cash = None
        self.position = None
        self.valo = None

# class
class Algo(Fsm):
    def __init__(self, order_q, exec_q, ticker_traded, signal):
        # FSM
        t_tbl = { STATES.IDLE: self.trans_idle,
                  STATES.PL: self.trans_pl,
                  STATES.CHECK_PL: self.trans_check_pl,
                  STATES.SIGNAL: self.trans_signal,
                  STATES.STOPPED: self.trans_stop }
        to_tbl = { STATES.SIGNAL: self.to_signal,
                   STATES.IDLE: self.to_idle }
        from_tbl = {}
        super().__init__(STATES.IDLE, t_tbl, from_tbl, to_tbl, [STATES.STOPPED])
        # TRADER
        self.book = { a: BookAsset(a) for a in ticker_traded }
        self.pl_last = { a: None for a in ticker_traded }

    #
    def compute_pl(self):
        for k, i in self.book.items():
            self.book[i].update()

    #fonctions de transition
    def trans_idle(self, data):
        if data.ticker not in self.positions:
            return STATES.SIGNAL
        return STATES.PL

    def trans_pl(self, data):
        
        return STATES.CHECK_PL

    def trans_check_pl(self, data):
        pass

    def trans_signal(self, data):
        pass