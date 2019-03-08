import threading
import requests
from _datetime import datetime
import random
import queue


class StressTester():

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
    tester = StressTester()
    tester.stress_test()
    a = []
    while not tester.q.empty():
        a.append(tester.q.get())

    for i in a:
        print (i)


main()