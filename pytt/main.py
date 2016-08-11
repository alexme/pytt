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
from .streams.cstream import ZS
from .streams.abstract import LList

def main():
    stream_q = []
    order_q = []
    exec_q = []
    # a = Algo(order_q, exec_q, ['stxec1'], signal, -10000)
    z = ZS(10)
    dstream = Stream(sid=0, LList(max_len=3))
    ostream = Stream(sid=1, [])
    estream = Stream(sid=2, [])
    while True:
        #events = sel.select
        for zs in map(zs, gbm_source(2)):
            dstream.add(zs)

            a.one_loop(data)
    #     data = stream_q.pop()
    #     res = yield from a.one_loop(data)
    z = ZS(10)
    for i, x in enumerate(gbm_source(2)):
        # print(x)
        print(z(x))
        if i > 500:
            break



if __name__ == "__main__":
    main()