"""
Useful things for streams
"""

from enum import Enum


STREAM_TYPE = Enum('StreamType', ['DATA', 'EXEC'])

class LList(list):
    # Read-only
    @property
    def max_len(self):
        return self._max_len

    def __init__(self, *args, **kwargs):
        self._max_len = kwargs.pop("max_len")
        list.__init__(self, *args, **kwargs)

    def _truncate(self):
        """Called by various methods to reinforce the maximum length."""
        dif = len(self)-self._max_len
        if dif > 0:
            self[:dif]=[]

    def append(self, x):
        list.append(self, x)
        self._truncate()

    def insert(self, *args):
        list.insert(self, *args)
        self._truncate()

    def extend(self, x):
        list.extend(self, x)
        self._truncate()

    def __setitem__(self, *args):
        list.__setitem__(self, *args)
        self._truncate()

    def __setslice__(self, *args):
        list.__setslice__(self, *args)
        self._truncate()

class QStream:
    def __init__(self, stream_id, q):
        self.sid = stream_id
        self.q = q

    def add(self, data):
        self.q.add(data)
