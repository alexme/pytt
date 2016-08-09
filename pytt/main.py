"""
main entry point dev only
"""

def main():
    stream_q = []
    order_q = []
    exec_q = []
    a = Algo(order_q, exec_q, ['stxec1'], signal, -10000)
    while True:
        data = stream_q.pop()
        res = yield from a.one_loop(data)



if __name__ == "__main__":
    main()