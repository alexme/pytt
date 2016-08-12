"""
Streams are a forest each SrcStream being the root of one tree
this is a strong limitation as you can t have a leaf stream depending on
more than one signal
"""

from enum import Enum
from .utils import coroutine


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
        self.q.append(stm._f())

    def read(self):
        for x in self.q:
            x.send(self.m)
        return self.m


class GenStream(SrcStream, ParentStream):
    def __init__(self, sid, g):
        self.sid = sid
        self.g = g
        ParentStream.__init__(self)

    def read(self):
        self.m = next(g)
        return ParentStream.read(self)


class CStream(LeafStream, ParentStream):
    def __init__(self, sid, prt_stm, fun):
        self.sid = sid
        self.x = None
        self.f = fun
        self.prt_stm = prt_stm
        self.prt_stm._add_stream(self)
        ParentStream.__init__(self)

    @coroutine
    def _f(self):
        while True:
            self.x = (yield)

    def read(self):
        self.m = self.f(self.x)
        return ParentStream.read(self)


class SeqStreamSelector:
    def __init__(self):
        self.src_q = []
        self.leaf_q = []
        self.i = self.n = 0

    def is_registered(self, stm):
        return (stm in src_q) or (stm in leaf_q)

    def register(self, stm, cb):
        if self.is_registered(stm):
            return
        if isinstance(stm, LeafStream):
            self.src_q.append((stm, cb))
            prt_stm = stm.prt_stm
            self.register((prt_stm, None))
        elif isinstance(stm, SrcStream):
            self.src_q.append((stm, cb))

    def select(self):
        evts = []
        self.n += 1
        self.i = (self.i + 1) % len(self.src_q)
        stm, cb = self.src_q[self.i]
        if cb:
            evts.append(cb(stm.read()))
        return evts

