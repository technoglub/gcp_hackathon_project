#!./../env/bin/python3

import threading
import requests
from _datetime import datetime
import random
import queue
import sys


class StressTester():

    ''' Class that tests the servers. If no command line input, it hits localhost,
        if there's an IP passed in, it will use that instead '''

    def __init__(self, url="http://LOCALHOST:5000/"):
        self.url = url
        self.port = 5000
        self.threads = []
        self.q = queue.Queue()


    def stress_test(self):
        '''Creates a bunch of threads to spam the servers'''

        for i in range(128):
            t = threading.Thread(target=self.make_request)
            t.start()


    def make_request(self):
        ''' Picks a random known coordinate '''
        start = datetime.now()
        indx = random.randint(0,5)
        print (indx)
        locs = ["34.13,-117.27", "34.07,-117.28", "34.52,-117.43", "34.52,-117.43", "34.08,-117.24", "34.10,-117.28"]
        print(locs[indx])
        r = requests.get(self.url + locs[indx])
        time = datetime.now() - start
        self.q.put(item=time, block=True)


def main():
    try:
        sys.argv[1]
        print(sys.argv[1])
        ip = sys.argv[1]
        dot_count = 0
        for i, v in enumerate(ip):
            if v == '.':
                dot_count += 1

        if dot_count != 3:
            print("Invalid format")
            return

        # initialize the testing class if the input is valid
        tester = StressTester(ip)
    except IndexError:
        tester = StressTester()
        pass
    try:
        tester.stress_test()
    except Exception as e:
        print(e)
        return

    timings = []
    while not tester.q.empty():
        timings.append(tester.q.get())

    for i in timings:
        print (i)


main()