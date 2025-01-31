import Queue as q
import log_parser
from output_print import OutputPrinter
import threading

class Node:
    def __init__(self, dict_data):
        self.dic_data = dict_data

    def __cmp__(self, other):
        return cmp(self.dic_data['at'], other.dic_data['at'])

def sync(func):
    def wrapper(*args, **kv):
        self = args[0]
        self.lock.acquire()
        try:
            return func(*args, **kv)
        finally:
            self.lock.release()
    return wrapper


class FixedSizePQ:
    """ class that implements a not-yet-full buffer """
    def __init__(self,size_max=20000):
        self.max = size_max
        self.data = q.PriorityQueue()
        self.lock = threading.Lock()

    class _full:
        """ class that implements a full buffer """
        @sync
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data.put(x)
            #self.cur = (self.cur+1) % self.max
            item = self.data.get().dic_data
            if OutputPrinter.is_valid(item):
                OutputPrinter.print_valid_line(item)
            else:
                OutputPrinter.print_invalid_line(item)
            self.cur = (self.cur+1) % self.max

        @sync
        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]
    @sync
    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.put(x)

        #printer = output_print.OutputPrinter()
        if self.data.qsize() == self.max:
            #item = self.data.get()

            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self._full

    @sync
    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

