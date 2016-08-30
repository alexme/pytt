"""
generic monitoring of algo and streams
"""
import asyncio
import queue
import time


class EventTracker:
    """
    in main stream i.e. algo, stream and selector thread
    meant to be associated with one obj (algo, stream) only
    will be a producer for the event dispatcher which will live
    in the monitoring thread messages are passed through
    the threadsafe q and notified thanks to the condition cond
    """

    def __init__(self):
        self.q = queue.Queue()

    def send(self, what):
        """
        we can imagine other append which only append when a certain number
        of events have been appended
        """
        self.q.put(what)


class EventDispatcher:
    """
    runs in monitoring thread
    - shares with the eventtracker the q and condition for message passing
    - ships to the handlers the event via an asyncio eventloop mecanism (good luck!)
    """

    def __init__(self, evt_tracker):
        self.q = evt_tracker.q

    # @asyncio.coroutine
    # def _r(self):
    #     yield from iter(self.q.get, None)

    @asyncio.coroutine
    def run(self):
        print('gros prouti')
        while True:
            print('ff')
            while not self.q.empty():
                data = self.q.get()
                print('got data %s' % data)
            print(self.q.qsize())
            yield from asyncio.sleep(1)


