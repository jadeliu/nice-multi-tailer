from argparse import ArgumentParser
import os, sys
import threading
import multi_tailer
from output_print import OutputPrinter
import time, datetime
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

        if reads:
            lock.acquire()
            for record in reads:
                filepath = record[0][0]
                line = record[0][1]
                data = LogParser.parse(line, filepath)
                cb.append(Node(data))
            lock.release()

def time_monitor(cb, maxwait):
    next_call = time.time()
    while True:
        emit_logs(cb)
        time.sleep(maxwait)

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

    # threads to continuously read from files with multi tailer
    files = [args.D+k for k in os.listdir(args.D)]
    for i in range(4):
        t = threading.Thread(name='read-and-write-2-buffer', target=read_log_and_write_2_buffer(cb,files, lock))
        t.daemon = True
        t.start()

    # timer thread to trigger emit when maxwait has reached
    timerThread = threading.Thread(target=time_monitor(cb, args.T))
    timerThread.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    signal.pause()

if __name__=="__main__":
    main()