import Queue as q
import log_parser
from output_print import OutputPrinter

class Node:
    def __init__(self, dict_data):
        self.data = dict_data

    def __cmp__(self, other):
        return cmp(self.data['at'], other.data['at'])

class CircularBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self,size_max=20000):
        self.max = size_max
        self.data = q.PriorityQueue()

    class _full:
        """ class that implements a full buffer """
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data.put(x)
            #self.cur = (self.cur+1) % self.max
            item = self.data.get()
            if OutputPrinter.is_valid(item):
                OutputPrinter.print_valid_line(item)
            else:
                OutputPrinter.print_invalid_line(item)
            self.cur = (self.cur+1) % self.max
        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]

    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.put(x)

        #printer = output_print.OutputPrinter()
        if self.data.qsize() == self.max:
            #item = self.data.get()

            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self._full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

'''
import log_parser
f = open('./sample_logs/sample')
lines = f.readlines()
parser = log_parser.LogParser()
path = 'sample_logs/sample'
lis = [parser.parse(line, path) for line in lines]
cb = CircularBuffer(2)
lis_nodes = [Node(k) for k in lis]
for node in lis:
    cb.append(node)
    print cb.__class__
    print cb.data
'''
