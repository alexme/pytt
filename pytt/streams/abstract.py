"""
Streams are a forest each SrcStream being the root of one tree
this is a strong limitation as you can t have a leaf stream depending on
more than one signal

very lasy update that could be simplified via
simple acessor BUT this lazinees is potentially dangerous
and could lead to inconsistent signals in the tree
"""

from enum import Enum
from .utils import coroutine

from ..market.dealing import ORDER_STATUS

import pdb

STREAM_TYPE = Enum('StreamType', ['DATA', 'EXEC'])

class SrcStream:
    pass

class LeafStream:
    pass

class ParentStream:
    def __init__(self):
        self.m = None
        self.q = []

    def _add_stream(self, stm):
        self.stm_q.append(stm) #only needed for events
        self.q.append(stm._f())



class GenStream(SrcStream, ParentStream):
    def __init__(self, sid, g):
        self.sid = sid
        self.g = g
        self.q = []
        self.m = None
        self.stm_q = []

    def read(self):
        self.m = next(self.g)
        for x in self.q:
            x.send(self.m)
        yield self.m
        # return ParentStream.update_childs(self)


class CStream(LeafStream, ParentStream):
    def __init__(self, sid, prt_stm, fun):
        self.sid = sid
        self.x = None
        self.f = fun
        self.prt_stm = prt_stm
        self.prt_stm._add_stream(self)
        self.q = []
        self.stm_q = []
        self.m = -27

    # needs addtitional coding here to replace the
    # update of child nodes which could lead to
    # inconsistency in child states
    # is it better ?
    @coroutine
    def _f(self):
        while True:
            self.x = (yield)
            self.m = self.f(self.x)
            for y in self.q:
                y.send(self.m)

    def read(self):
        # self.m = self.f(self.x)
        # return ParentStream.update_childs(self)
        yield self.m

class MStream(LeafStream):
    """
    to keep the signal tree structure only one source
    can feed a market stream seveal assets => src stream in R**n n>1
    instr_list elements are market.asset.Instrument
    """
    def __init__(self, sid, instr_list, prt_stm):
        self.sid = sid
        self.order_book = {x: None for x in instr_list}
        self.instr_list = instr_list
        self.prt_stm = prt_stm
        self.prt_stm._add_stream(self)
        self.stm_q = []

    @coroutine
    def _f(self):
        while True:
            mkt_up = (yield)
            for i, m in zip(self.instr_list, mkt_up):
                self.order_book[i] = m

    def run_matcing_engine(self):
        for i in self.instr_list:
            while i.orders:
                o = i.orders.pop()
                yield o.send((ORDER_STATUS.FILLED, self.order_book[i]))

    def read(self):
        yield from self.run_matcing_engine()


class SeqSrcStreamSelector:
    """
    not great for demo only ?
    if the src of a leaf stream is not registered then
    the src read method will not be called and the leaf
    will never be computed moreover only leaves for which the src has been
    added will be called as a ersult we automatically register the src
    with a None callback 
    -> this is messy I really don t like it
    """
    def __init__(self):
        self.stm_map = {}
        # self.src_q = {}
        # self.leaf_q = {}
        self.seq = []
        self.i = self.n = 0

    def is_registered(self, stm):
        # a bit more tricky than could be thought
        # if it has been registered with a none callback
        # we actually consider it as non regitered for 
        # this function see pb in intro of class
        # if (stm in self.src_q) and (self.src_q[stm] is None):
        if (stm in self.stm_map) and (self.stm_map[stm] is None):
            return False
        # return (stm in self.src_q) or (stm in self.leaf_q)
        return (stm in self.stm_map)

    def register(self, stm, cb):
        if self.is_registered(stm):
            return
        if isinstance(stm, LeafStream):
            self.stm_map[stm] = cb
            p_stm = stm
            # registering root of tree mecanism
            while not isinstance(p_stm, SrcStream):
                p_stm = p_stm.prt_stm
            self.register(p_stm, None)
        elif isinstance(stm, SrcStream):
            # self.src_q[stm] = cb
            self.stm_map[stm] = cb
            self.seq.append(stm)

    def select(self):
        if not self.seq:
            raise ValueError('SeqSrc stream must have at least one src registered')
        # evts = []
        self.n += 1
        self.i = (self.i + 1) % len(self.seq)
        stm = self.seq[self.i]
        # traverse tree
        _q = [stm]
        while _q:
            x = _q.pop()
            if isinstance(x, SrcStream):
                if self.stm_map[x] is None:
                    next(x.read()) # needs to consume the gen without doing anything please check
                else:
                    yield from map(self.stm_map[x], x.read())
            elif isinstance(x, LeafStream):
                yield from map(self.stm_map[x], x.read())
            else:
                raise ValueError()
            # if stream is leaf then stm_q = []
            for y in x.stm_q:
                if self.is_registered(y):
                    _q.append(y)

