"""
Streams are a forest each SrcStream being the root of one tree
this is a strong limitation as you can t have a leaf stream depending on
more than one signal
"""

from enum import Enum
from .utils import coroutine
import asyncio
import time

from ..market.dealing import ORDER_STATUS, EXEC_STATUS

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
    def __init__(self, sid, g, dispatcher = None):
        self.sid = sid
        self.g = g
        self.q = []
        self.m = None
        self.stm_q = []
        self.dispatcher = dispatcher

    def read(self):
        self.m = next(self.g)
        if self.dispatcher:
            print("->", self.m)
            asyncio.ensure_future(self.dispatcher.send(self.m))
            print(self.m)
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
        self.price_book = {x: None for x in instr_list}
        self.instr_list = instr_list
        for i in instr_list:
            i._bind_market(self)
        self.prt_stm = prt_stm
        self.prt_stm._add_stream(self)
        self.stm_q = []

    @coroutine
    def _f(self):
        while True:
            mkt_up = (yield)
            for i, m in zip(self.instr_list, mkt_up):
                self.price_book[i] = m

    def run_matching_engine(self):
        for i in self.instr_list:
            orders_push_back = []
            while i.orders:
                o = i.orders.pop()
                status, qty = next(o)
                try:
                    if status == ORDER_STATUS.HIT:
                        o.send((EXEC_STATUS.FILLED, self.price_book[i]))
                    elif status == ORDER_STATUS.CANCEL:
                        o.send((EXEC_STATUS.CANCELLED, self.price_book[i]))
                    else:
                        orders_push_back.append(o)
                        raise ValueError("order status unknown")
                except StopIteration as e:
                    status, pce, qty, cli = e.value
                    index = cli.orders[i].index(o)
                    del cli.orders[i][index]
                    yield (i, status, pce, qty, cli)
            i.orders = orders_push_back

    def read(self):
        # do 2 things :
        # - run the ;atching engine
        # - send the execs and cancelled
        yield from self.run_matching_engine()


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
        self.i = 0

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

    @asyncio.coroutine
    def select(self):
        while True:
            print('another loop')
            if not self.seq:
                raise ValueError('SeqSrc stream must have at least one src registered')
            # evts = []
            self.i = (self.i + 1) % len(self.seq)
            # 
            stm = self.seq[self.i]
            # traverse tree
            _q = [stm]
            while _q:
                x = _q.pop()
                if isinstance(x, SrcStream):
                    if self.stm_map[x] is None:
                        next(x.read()) # needs to consume the gen without doing anything please check
                    else:
                        # yield from map(self.stm_map[x], x.read())
                        for data in x.read():
                            self.stm_map[x](data)
                elif isinstance(x, LeafStream):
                    for data in x.read():
                        # print(data)s
                        # data = yield from x.read()
                        self.stm_map[x](data)
                else:
                    raise ValueError()
                # if stream is leaf then stm_q = []
                for y in x.stm_q:
                    if self.is_registered(y):
                        _q.append(y)
            yield from asyncio.sleep(0.25)

