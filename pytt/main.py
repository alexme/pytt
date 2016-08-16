"""
main entry point dev only
- eventloop
- selector on streams :
    - stream_id is like the file descriptor
    - type of stream (data, order, exec)
    - priority queue is like the file - priority on ts
- for each stream objects which have subscribed get the event
objects are :
    - algo machine send orders according to a stream
    - cstream computations on streams
    - markets receive orders and send exec
streams are :
    - order/exec stack
    - datafeed
    - computations on streams a.k.a cstream
"""

from .streams.model import gbm_source
from .machines.trader import Algo
from .streams.utils import ZS
from .streams.abstract import SeqSrcStreamSelector, GenStream, CStream, MStream
from .market.asset import Instrument, Future
import pdb


def main():
    # a = Algo(order_q, exec_q, ['stxec1'], signal, -10000)
    z = ZS(10)
    f1 = Instrument(Future('f1', 5))
    f2 = Instrument(Future('f2', 10))
    sstream = GenStream(0, gbm_source(2))
    sstream1 = GenStream(1, gbm_source(1))
    cstream = CStream(2, sstream, z)
    mstream = MStream(3, [f1, f2], sstream)
    sel = SeqSrcStreamSelector()
    sel.register(sstream1, lambda x: x)
    sel.register(mstream, lambda x: x)
    # sel.register(sstream, lambda x: x)
    i = 0
    while True:
        print('*' * 20)
        i += 1
        if i % 2:
            f1.send_order(1)
        else:
            f2.send_order(4)
        for evts in sel.select():
            print(evts)
        # for zs in map(zs, gbm_source(2)):
        #     dstream.add(zs)

        #     a.one_loop(data)
    #     data = stream_q.pop()
    #     res = yield from a.one_loop(data)
    # z = ZS(10)
    # for i, x in enumerate(gbm_source(2)):
    #     # print(x)
    #     print(z(x))
    #     if i > 500:
    #         break



if __name__ == "__main__":
    main()