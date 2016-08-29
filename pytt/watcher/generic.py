"""
generic monitoring of algo and streams
"""
import threading
import queue


class EventTracker:
    """
    in main stream i.e. algo, stream and selector thread
    meant to be associated with one obj (algo, stream) only
    will be a producer for the event dispatcher which will live
    in the monitoring thread messages are passed through
    the threadsafe q and notified thanks to the condition cond
    """

    def __init__(self, q, cond):
        self.q = q
        self.cond = cond
        self.cond.acquire()

    def append(self, what):
        """
        we can imagine other append which only append when a certain number
        of events have been appended
        """
        self.cond.acquire()
        # any additional args ?
        self.q.put(what)
        self.cond.notify()
        self.cond.release()


class EventDispatcher(threading.Thread):
    """
    runs in monitoring thread
    - shares with the eventtracker the q and condition for message passing
    - ships to the handlers the event via an asyncio eventloop mecanism (good luck!)
    """

    def __init__(self, evt_tracker):
        super().__init__()
        self.daemon = True
        self.q = evt_tracker.q
        self.cond = evt_tracker.cond

    def run(self):
         while True:
            self.cond.acquire()
            print('TODO : never reaches here this is a problem')
            while True:
                if self.q:
                    data = self.q.get()
                    print('got data %s' % data)
                    # dontknow about this...
                    break
                self.cond.wait()
            self.cond.release()

