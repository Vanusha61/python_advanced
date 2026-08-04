
from typing import Callable
from threading import Thread
from queue import PriorityQueue

import random
import time

queue = PriorityQueue()


class Producer(Thread):
    def __init__(self, priority: int, func: Callable, queue_list: PriorityQueue, args, kwargs=None):
        super().__init__()
        self.priority = priority
        self.queue_list = queue_list
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        task = Task(
            priority=self.priority,
            func=self.func,
            args=self.args,
        )
        self.queue_list.put((self.priority, task))



class Consumer(Thread):
    def __init__(self, queue_list: PriorityQueue):
        super().__init__()
        self.queue_list = queue_list

    def run(self):
        while not self.queue_list.empty():
            priority, task =  self.queue_list.get()
            print(f"Running Task(priority={priority}), args={task.args}")
            task.func(*task.args)

class Task:
    def __init__(self, priority: int, func: Callable, args, kwargs = None):
        self.priority = priority
        self.func = func
        self.args = args
        self.kwargs = kwargs


if __name__ == "__main__":
    start = time.time()
    thread = []
    for i in range(10):
        thread_1 = Producer(priority=i,func=time.sleep, queue_list=queue, args=(random.random(), ), kwargs={})
        thread_1.start()
        thread.append(thread_1)
    for thr in thread:
        thr.join()

    thread = []
    for i in range(10):
        thread_1 = Consumer(queue_list=queue)
        thread_1.start()
        thread.append(thread_1)
    for thr in thread:
        thr.join()


    print(f"Total time: {time.time() - start}")
