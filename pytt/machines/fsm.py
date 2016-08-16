### FSM

# consts


# exception
class EndStateException(Exception):
    pass

# class
class Fsm:
    """
    - transitions are given by transition table
    - from_state table contains function to execute BEFORE transition
    - to_state table contains function to execute AFTER transition
    If an end state is reached then after executing to_state (if any)
    will raise an EndStateException
    """
    def __init__(self, state_start, trans_table, from_trans_tbl, to_trans_tbl, end_states):
        self.transitions = trans_table
        self.from_state = from_trans_tbl
        self.to_state = to_trans_tbl
        self.state = state_start
        self.end_states = set(end_states)

    def next(self, *args):
        # try:
        #     yield from self.from_state[self.state](*args)
        # except KeyError:
        #     pass
        self.state = self.transitions[self.state](*args)
        # try:
        #     yield from self.to_state[self.state](*args)
        # except KeyError:
        #     pass
        if self.state in self.end_states:
            raise EndStateException()

    def next_to(self, tgt_state, *args):
        # yield from self.next(*args)
        self.next(*args)
        while self.state != tgt_state:
            self.next(*args)
            # yield from self.next(*args)
