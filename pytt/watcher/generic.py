"""
generic monitoring of algo and streams
"""
import asyncio
import queue
import time
import websockets
import aiofiles
import pdb
import numpy as np
from enum import Enum

# class EventTracker:
#     """
#     in main stream i.e. algo, stream and selector thread
#     meant to be associated with one obj (algo, stream) only
#     will be a producer for the event dispatcher which will live
#     in the monitoring thread messages are passed through
#     the threadsafe q and notified thanks to the condition cond
#     """

#     def __init__(self):
#         self.q = queue.Queue()
PLD_CAT = Enum('CatPayload', ('PL', 'STREAM', 'POSITIONS'))

class EventDispatcher:
    """
    runs in monitoring thread
    - shares with the eventtracker the q and condition for message passing
    - ships to the handlers the event via an asyncio eventloop mecanism (good luck!)
    """

    def __init__(self, handlers):
        self.q = asyncio.Queue()
        self.handlers = handlers

    @asyncio.coroutine
    def send(self, sid, cat, data):
        """
        ONLY APPEND IMMUTABLE DATA IN AN ASYNCIO Q
        """
        pld_str = EventDispatcher.marshal(sid, cat, data)
        yield from self.q.put(pld_str)

    @staticmethod
    def marshal(aid, cat, data):
        if isinstance(data, np.ndarray):
            data_str = np.array2string( data, precision=1, suppress_small=True, separator=',' )
        else:
            data_str = "%s" % data
        id_str = "%s" % aid
        cat_str = "%s" % cat
        return "|".join((id_str, cat_str, data_str))

    @asyncio.coroutine
    def run(self):
        while True:
            while not self.q.empty():
                pld = yield from self.q.get()
                self.q.task_done()
                for h in self.handlers:
                    yield from h.send(pld)
            yield from asyncio.sleep(1)


class Handler:
    def __init__(self):
        self.q = asyncio.Queue()

    # @asyncio.coroutine
    # def send(self, data):
    #     data = "%s" % data
    #     print('putting in q %s' % data)
    #     self.q.put(data)
    @asyncio.coroutine
    def send(self, data_str):
        yield from self.q.put(data_str)

    def close():
        # call it in the finally of main loop
        # closed with the asyncio loop
        pass

class FileHandler(Handler):
    def __init__(self, ffn):
        super().__init__()
        self.ffn = ffn
        self.fh = None
        asyncio.ensure_future(self.run(ffn))

    @asyncio.coroutine
    def run(self, ffn):
        self.fh = yield from aiofiles.open(ffn, mode='w')
        while True:
            while not self.q.empty():
                pld_str = yield from self.q.get()
                self.q.task_done()
                yield from fh.write(pld_str)
            yield from asyncio.sleep(1)

    @asyncio.coroutine
    def close(self):
        print("closing file %s" % self.ffn)
        yield from self.fh.close()
        print("file closed")


class WsHandler(Handler):
    def __init__(self, host='127.0.0.1', port=5678):
        super().__init__()
        asyncio.ensure_future(websockets.serve(self.ws_handler, host, port))

    @asyncio.coroutine
    def ws_handler(self, websocket, path):
        while True:
            while not self.q.empty():
                pld_str = yield from self.q.get()
                self.q.task_done()
                print('sending data %s' % pld_str)
                yield from websocket.send(pld_str)
            print('q is empty')
            yield from asyncio.sleep(1)
