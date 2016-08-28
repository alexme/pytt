"""
unitests for order passing
"""

import unittest

from ..market.asset import Instrument, Future
from ..machines.trader import Algo
from ..streams.abstract import MStream, GenStream
from ..market.dealing import ORDER_STATUS, EXEC_STATUS


class TestOrderMgt(unittest.TestCase):

    @staticmethod
    def cst_pce(pce):
        while True:
            yield pce

    def test_order(self):
        # instruments
        f1 = Instrument(Future('f1', 5))
        f2 = Instrument(Future('f2', 10))
        # streams need a mkt stream to be tradable
        # sstream = GenStream(0, self.cst_pce([27.10, 45.10]))
        # mstream = MStream(3, [f1, f2], sstream)
        o = f1.send_order(ORDER_STATUS.HIT, 10)
        s, q = next(o)
        with self.assertRaises(StopIteration) as e:
            resp = o.send((EXEC_STATUS.FILLED, 110))
        print(e.exception)
        # resp = o.send((EXEC_STATUS.CANCELLED, 110))
        # s, q = next(o)
        # next(o)


    def test_market_order(self):
        f1 = Instrument(Future('f1', 5))
        f2 = Instrument(Future('f2', 10))
        # streams
        sstream = GenStream(0, self.cst_pce([27.10, 45.10]))
        mstream = MStream(3, [f1, f2], sstream)
        # # algo
        a = Algo([f1, f2], sstream, -10000)
        # ici un premier test
        o = f1.send_order(ORDER_STATUS.HIT, 10)
        next(sstream.read())
        with self.assertRaises(StopIteration) as e:
            mstream.run_matching_engine()
        print(e.exception)

if __name__ == "__main__":
    unittest.main()