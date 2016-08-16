from argparse import ArgumentParser
import os, sys
import threading
import multi_tailer
from output_print import OutputPrinter
import time
import signal
from circular_buffer import *
from log_parser import LogParser

def signal_handler(signal, frame):
    print('You pressed Ctrl+C! Exit the program')
    sys.exit(0)

def read_log_and_write_2_buffer(cb, files, lock):
    mt = multi_tailer.MultiTail(files, skip_to_end=False)
    while True:
        reads = list(mt.poll(files))
        print reads
        '''
        if reads:
            lock.acquire()
            for line in reads:
        '''

def emit_logs(cb):
    # function to emit everything in the circular buffer
    while not cb.data.empty():
        item = cb.data.get()
        if OutputPrinter.is_valid(item):
            OutputPrinter.print_valid_line(item)
        else:
            OutputPrinter.print_invalid_line(item)

def main():
    parser = ArgumentParser(description="usage: %prog [arguments]")
    parser.add_argument('-D',metavar="directory",required = True, help="path to the directory")
    parser.add_argument('-T', metavar='maxwait',type = int, default=1000, help='value in milliseconds to delay processing events')
    parser.add_argument('-B',action='store_true')
    args = parser.parse_args()

    lock = threading.Lock()
    cb = CircularBuffer(args.T)

    # thread to continuously read from files with multi tailer
    files = [args.D+k for k in os.listdir(args.D)]
    t1 = threading.Thread(name='read-and-write-2-buffer', target=read_log_and_write_2_buffer(cb,files, lock))

    # timer thread to trigger emit
    #t2 = TimerThread()
    #t2.start()

    # timer thread to


    # output thread to monitor queue, sort and emit
    #t3 = threading.Thread(name='non-daemon', target=non_daemon)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()

if __name__=="__main__":
    main()