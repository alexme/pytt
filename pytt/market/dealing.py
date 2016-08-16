"""
main class dealing with order passing etc
"""
from enum import Enum

#consts
ORDER_STATUS = Enum('OrderStatus', ['FILLED'])

# STATUS_EXEC = Enum('Exec status', ['DONE', 'DENIED'])


# class Order:
#     """
#     for the time being only hit orders are used
#     """
#     def __init__(self, ticker, qty):
#         self.ticker = ticker
#         self.qty = qty
#         self.status = STATUS_ORDER.HIT

# class Exec:
#     def __init__(self, ticker, qty, price, status):
#         self.ticker = ticker
#         self.qty = qty
#         self.price = price
#         self.status = status

#     @staticmethod
#     def exec_order(order, price):
#         if order.status == STATUS_ORDER.HIT:
#             return Exec(order.ticker, order.qty, price, STATUS_EXEC.DONE)
#         return Exec(order.ticker, order.qty, None, STATUS_EXEC.DENIED)
