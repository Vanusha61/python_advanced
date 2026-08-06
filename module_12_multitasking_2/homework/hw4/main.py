from queue import Queue

import requests
import time
import threading


queue = Queue()


def requst_get():
    for _ in range(20):
        current_timestamp = int(time.time())
        res = requests.get(f"http://127.0.0.1:8080/timestamp/{current_timestamp}")
        queue.put((current_timestamp, res.text))
        time.sleep(1)


if __name__ == '__main__':
    threads = []
    for i in range(10):
        thread = threading.Thread(target=requst_get)
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for thread in threads:
        thread.join()

    with open("log.txt", "a") as f:
        for i in sorted(queue.queue):
            current_timestamp, res = i
            f.write(f'{current_timestamp} {res}' + "\n")