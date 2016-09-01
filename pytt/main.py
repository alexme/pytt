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

from functools import partial
import asyncio
import queue
from concurrent.futures import ThreadPoolExecutor

from .streams.model import gbm_source
from .machines.trader import Algo
from .streams.utils import ZS
from .streams.abstract import SeqSrcStreamSelector, GenStream, CStream, MStream
from .watcher.generic import EventDispatcher, WsHandler
from .market.asset import Instrument, Future
import pdb

# @asyncio.coroutine
def main():
    # intruments
    f1 = Instrument(Future('f1', 5))
    f2 = Instrument(Future('f2', 10))
    # monitoring
    # et = EventTracker()
    ws = WsHandler()
    w = EventDispatcher([ws])
    # streams
    sstream = GenStream(0, gbm_source(2), w)
    sstream1 = GenStream(1, gbm_source(1))
    cstream = CStream(2, sstream, ZS(10))
    mstream = MStream(3, [f1, f2], sstream)
    # algo
    a = Algo([f1, f2], cstream, -10000)
    # algo callbacks
    cb_src = partial(a.one_loop, sstream)
    cb_com = partial(a.one_loop, cstream)
    cb_mkt = partial(a.one_loop, mstream)
    # selector
    sel = SeqSrcStreamSelector()
    sel.register(sstream, cb_src)
    sel.register(cstream, cb_com)
    sel.register(mstream, cb_mkt)
    # sel.register(sstream, lambda x: x)
    # executor = ThreadPoolExecutor()
    # asyncio.ensure_future(loop.run_in_executor(executor, sel.select))
    # yield from w.run()
    asyncio.ensure_future(sel.select())
    asyncio.ensure_future(w.run())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('exit')
    finally:
        #close the handlers !
        loop.stop()
        loop.close()