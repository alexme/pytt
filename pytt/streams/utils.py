"""
various utils
for online stats
https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
"""

from collections import deque
import numpy as np
import functools

def coroutine(f):
    @functools.wrap(f)
    def wrapper(*args, **kwargs):
        cr = f(*args, **kwargs)
        next(cr)
        return cr
    return wrapper


class Avg:
    """
    zs
    """
    def __init__(self, l):
        self.q = deque()
        self.max_len = l
        self.m = 0.0
        self.v = 0.0

    def __call__(self, value):
        #not great demo only
        if len(self.q) < self.max_len:
            self.q.append(value)
            self.m += value
            if len(self.q) == self.max_len:
                return value - self.m / self.max_len
            return 0.0
        old_val = self.q.popleft()
        self.m += value - old_val
        self.q.append(value)
        return value - self.m / self.max_len

class ZS:
    """ note that data has to be in R**n
    """
    def __init__(self, min_l):
        self.l = min_l
        self.n = 0
        self.mean = None
        self.v = None

    def __call__(self, data):
        if not self.n:
            self.mean = np.zeros(data.size)
            self.v = np.zeros(data.size)
        self.n += 1
        delta = data - self.mean
        self.mean += delta / self.n
        self.v += delta * (data - self.mean)
        if self.n < self.l:
            zs = np.zeros(data.size)
        else:
            zs = (self.n-1) * (data - self.mean) / self.v
        return zs

