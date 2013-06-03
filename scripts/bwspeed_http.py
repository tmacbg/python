#!/usr/bin/env python

import sys
import time
import socket
from threading import Thread

host = '184.173.198.48'
port = 80

thread_count = 10  

class Controller:
    def __init__(self):
        self.count_ref = []
    def start(self):
        for i in range(thread_count):
            agent = Agent(self.count_ref)
            agent.setDaemon(True)
            agent.start()
        print 'started %d threads' % (i + 1)
        while True:
            time.sleep(1)
            line = 'connects/sec: %s' % len(self.count_ref)
            self.count_ref[:] = []
            sys.stdout.write(chr(0x08) * len(line))
            sys.stdout.write(line)
            
class Agent(Thread):
    def __init__(self, count_ref):
        Thread.__init__(self)
        self.count_ref = count_ref
    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, port))
                s.shutdown(2)
                s.close()
                self.count_ref.append(1)
            except:
                print 'SOCKET ERROR\n'
                
if __name__ == '__main__':
    controller = Controller()
    controller.start()

