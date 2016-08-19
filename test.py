from enum import Enum

import functools

def coroutine(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        cr = f(*args, **kwargs)
        next(cr)
        return cr
    return wrapper

import pdb

ORDER_STATUS = Enum('OrderStatus', ['HIT', 'CANCEL'])
EXEC_STATUS = Enum('ExecStatus', ['FILLED', 'CANCELLED', 'PENDING'])
DONE_STATUS = ( EXEC_STATUS.FILLED, EXEC_STATUS.CANCELLED )

class Instrument:
    def __init__(self, asset):
        self.asset = asset
        self.orders = []

    def send_order(self, qty, client):
        cr = self._o(qty, client)
        self.orders.append(cr)
        client.orders[self].append(cr)
        return cr

    # @coroutine
    # def _o(self, qty):
    #     """
    #     very simple here the market gives us a status
    #     which is always done and a price
    #     we could imagine a much more complicated logic
    #     this method would then probably comprise a couple of yield
    #     statements instead of only 2
    #     """
    #     status, pce = (yield)
    #     yield (self, qty, pce)

    @coroutine
    def _o(self, qty, client):
        status = EXEC_STATUS.PENDING
        print('bef while')
        yield
        while not (status in DONE_STATUS):
            print('bef status')
            yield status, qty
            print('bet')
            status, pce = (yield)
            print('after status ', status, pce)
        print('done')
        return (status, qty, pce)

class A:
    def __init__(self, i):
        self.i = i
        self.orders = {i: []}

    def pr(self):
        return self.i.send_order(10, self)

i = Instrument('f')
a = A(i)
o = a.pr()

#cote algo
for x in a.orders[i]:
    print(id(x))
    print(id(o))
    status, qty = x.send(None)
    print(status)
    print(qty)
    print('*' * 3)
    g = x.send(('ff', 10))
    print('g is ', g)
#cote marche
print(o)
ret = next(o)
print('firt ret')
print(ret)
try:
    o.send((EXEC_STATUS.FILLED, 1045))
except StopIteration as ex:
    ret = ex
    ind = i.orders.index(o)
    del i.orders[ind]
print('ret is ', ret)
print(i.orders)
print(a.orders)

