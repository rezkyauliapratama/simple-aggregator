import threading
import time
from queue import Queue

import requests

hosts = ['https://api.ipify.org', 'https://google.com']
queue = Queue()
outqueue = Queue()


class ThreadUrl:
    """Threaded Url Grab"""

    def __init__(self, queue, outqueue):
        self.queue = queue
        self.outqueue = outqueue

    def run(self):
        while True:
            # grabs host from queue
            host = self.queue.get()
            print(f"host {host}")
            http_response = requests.get(url=host, params={"format": "json"},
                                         headers={"content-type": "application/json"})

            # place chunk into out queue
            self.outqueue.put(http_response.text)

            # signals to queue job is done
            self.queue.task_done()


class DatamineThread:
    """Threaded Url Grab"""

    def __init__(self, out_queue):
        self.out_queue = out_queue

    def run(self):
        while True:
            # grabs host from queue
            chunk = self.out_queue.get()

            print(f"chuck {chunk}")

            # signals to queue job is done
            self.out_queue.task_done()


start = time.time()


def main():
    # spawn a pool of threads, and pass them queue instance
    for i in range(5):
        threadUrl = ThreadUrl(queue, outqueue)
        t = threading.Thread(target=threadUrl.run)
        t.daemon = True
        t.start()

    for host in hosts:
        queue.put(host)

    for i in range(5):
        determineThread = DatamineThread(outqueue)
        dt = threading.Thread(target=determineThread.run)
        dt.daemon = True
        dt.start()

    # wait on the queue until everything has been processed
    queue.join()
    outqueue.join()


main()
print(f"Elapsed Time: %s" % (time.time() - start))
