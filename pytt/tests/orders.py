"""
unitests for order passing
"""

from ..market.asset import Instrument, Future
from ..machines.trader import Algo
from ..streams.abstract import MStream, GenStream
from ..market.dealing import ORDER_STATUS, EXEC_STATUS

def cst_pce(pce):
    while True:
        yield pce

f1 = Instrument(Future('f1', 5))
f2 = Instrument(Future('f2', 10))
# streams
sstream = GenStream(0, cst_pce([27.10, 45.10]))
mstream = MStream(3, [f1, f2], sstream)
# # algo
a = Algo([f1, f2], sstream, -10000)
# ici un premier test
o = f1.send_order(ORDER_STATUS.HIT, 10, a)
# s, q = next(o)
# print('cici')
# resp = o.send((EXEC_STATUS.FILLED, 110))
# print('cacia')
# s, q = next(o)
# print('coucou')
# resp = o.send((EXEC_STATUS.CANCELLED, 110))
# print(resp)
# s, q = next(o)
# next(o)
next(sstream.read())
mstream.run_matching_engine()