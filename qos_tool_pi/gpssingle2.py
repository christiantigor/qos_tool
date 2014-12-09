#example of stoppable thread
import threading

class stoppableThread(threading.Thread):
    def __init__(self):
        super(stoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
