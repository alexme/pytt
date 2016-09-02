"""
generic monitoring of algo and streams
"""
import asyncio
import queue
import time
import websockets
import pdb
import numpy as np

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
    def send(self, data):
        """
        ONLY APPEND IMMUTABLE DATA IN AN ASYNCIO Q
        """
        data_str = EventDispatcher.marshal(data)
        yield from self.q.put(data_str)

    @staticmethod
    def marshal(data):
        return np.array2string( data, precision=1, suppress_small=True, separator=',' )

    @asyncio.coroutine
    def run(self):
        while True:
            while not self.q.empty():
                data = yield from self.q.get()
                self.q.task_done()
                for h in self.handlers:
                    yield from h.send(data)
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
        #don t like it but can I avoid this ?
        #when calling it ?
        pass

class FileHandler(Handler):
    def __init__(self, ffn):
        super().__init__()

class WsHandler(Handler):
    def __init__(self, host='127.0.0.1', port=5678):
        super().__init__()
        asyncio.ensure_future(websockets.serve(self.ws_handler, host, port))

    @asyncio.coroutine
    def ws_handler(self, websocket, path):
        while True:
            while not self.q.empty():
                print('wait t send')
                data = yield from self.q.get()
                self.q.task_done()
                print('sending data %s' % data)
                yield from websocket.send(data)
            print('q is empty')
            yield from asyncio.sleep(1)
