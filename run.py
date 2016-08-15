from argparse import ArgumentParser
import sys
import threading
import multi_tailer
import output_print
import time

class TimerThread(threading.Thread):
    def __init__(self):
        self.stopped = False
        threading.Thread.__init__(self)

    def run(self, wait_time, func, *args):
        while not self.stopped:
            func(args)
            time.sleep(wait_time)

def write_2_buffer(directory):
    pass

def emit_log():
    pass

def main():
    parser = ArgumentParser(description="usage: %prog [arguments]")
    parser.add_argument('-D',metavar="directory",required = True, help="path to the directory")
    parser.add_argument('-T', metavar='maxwait',type = int, default=1000, help='value in milliseconds to delay processing events')
    parser.add_argument('-B',action='store_true')
    args = parser.parse_args()
    print "parser"
    print args
    lock = threading.Lock()

    mt = multi_tailer.MultiTail(args.D, skip_to_end=False)
    print list(mt.poll())


    # thread to read from files with multi tailer
    #t2 = TimerThread()
    #t2.start()

    # timer thread to


    # output thread to monitor queue, sort and emit
    #t3 = threading.Thread(name='non-daemon', target=non_daemon)



if __name__=="__main__":
    main()