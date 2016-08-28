"""
unitests for order passing
"""

import unittest
from unittest.mock import MagicMock

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
        a = MagicMock(orders={f1:[], f2:[]})
        PRICE = 110
        QTY = 5
        # streams need a mkt stream to be tradable
        # sstream = GenStream(0, self.cst_pce([27.10, 45.10]))
        # mstream = MStream(3, [f1, f2], sstream)
        o = f1.send_order(ORDER_STATUS.HIT, QTY, a)
        s, q = next(o)
        with self.assertRaises(StopIteration) as e:
            o.send((EXEC_STATUS.FILLED, PRICE))
        self.assertEqual(e.exception.value[0], EXEC_STATUS.FILLED)
        self.assertEqual(e.exception.value[1], PRICE)
        self.assertEqual(e.exception.value[2], QTY)
        self.assertEqual(e.exception.value[3], a)
        o = f2.send_order(ORDER_STATUS.HIT, QTY, a)
        s, q = next(o)
        self.assertEqual(s, ORDER_STATUS.HIT)
        self.assertEqual(q, QTY)
        o.send((ORDER_STATUS.CANCEL, 110))
        s, q = next(o)
        self.assertEqual(s, ORDER_STATUS.CANCEL)
        self.assertEqual(q, QTY)
        with self.assertRaises(StopIteration) as e:
            o.send((EXEC_STATUS.CANCELLED, None))
        self.assertEqual(e.exception.value[0], EXEC_STATUS.CANCELLED)
        self.assertIsNone(e.exception.value[1])
        self.assertEqual(e.exception.value[2], QTY)
        self.assertEqual(e.exception.value[3], a)


    def test_market_order(self):
        # TODO check properly a.orders
        f1 = Instrument(Future('f1', 5))
        f2 = Instrument(Future('f2', 10))
        # streams
        sstream = GenStream(0, self.cst_pce([27.10, 45.10]))
        mstream = MStream(3, [f1, f2], sstream)
        # # algo
        a = Algo([f1, f2], sstream, -10000)
        # ici un premier test
        o = f1.send_order(ORDER_STATUS.HIT, 10, a)
        oc = f2.send_order(ORDER_STATUS.HIT, 100, a)
        next(oc)
        oc.send((ORDER_STATUS.CANCEL, None))
        # send one update
        next(sstream.read())
        # check exec/cancel
        x = list(mstream.read())
        self.assertEqual(x[0][0], EXEC_STATUS.FILLED)
        self.assertEqual(x[0][1], 27.10)
        self.assertEqual(x[0][2], 10)
        self.assertEqual(x[1][0], EXEC_STATUS.CANCELLED)
        self.assertEqual(x[1][1], 45.1)
        self.assertEqual(x[1][2], 100)

if __name__ == "__main__":
    unittest.main()