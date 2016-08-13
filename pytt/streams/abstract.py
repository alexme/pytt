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
        return self.m
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
        self.m = None

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
        return self.m

class SeqSrcStreamSelector:
    """
    not great for demo only
    need to register to call read register src only
    """
    def __init__(self):
        self.src_q = {}
        self.leaf_q = {}
        self.seq = []
        self.i = self.n = 0

    def is_registered(self, stm):
        return (stm in self.src_q) or (stm in self.leaf_q)

    def register(self, stm, cb):
        if self.is_registered(stm):
            return
        if isinstance(stm, LeafStream):
            self.leaf_q[stm] = cb
            # prt_stm = stm.prt_stm
            # self.register(prt_stm, None)
        elif isinstance(stm, SrcStream):
            self.src_q[stm] = cb
            self.seq.append(stm)

    def select(self):
        evts = []
        self.n += 1
        self.i = (self.i + 1) % len(self.src_q)
        stm = self.seq[self.i]
        # traverse tree
        _q = [stm]
        while _q:
            x = _q.pop()
            if isinstance(x, SrcStream):
                evts.append(self.src_q[stm](stm.read()))
            elif isinstance(x, LeafStream):
                evts.append(self.leaf_q[stm](stm.read()))
            else:
                raise ValueError()
            for y in x.q:
                if self.is_registered(y):
                    _q.append(y)
        return evts

