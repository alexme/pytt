"""
main entry point dev only
"""

from .streams.model import gbm_source
from .machines.trader import Algo
from .signals.dummy import AvgSignal

def main():
    stream_q = []
    order_q = []
    exec_q = []
    signal = AvgSignal(10)
    a = Algo(order_q, exec_q, ['stxec1'], signal, -10000)
    # while True:
    #     data = stream_q.pop()
    #     res = yield from a.one_loop(data)
    # for i, x in enumerate(gbm_source(2)):
    #     print(x)
    #     if i > 50:
    #         break



if __name__ == "__main__":
    main()