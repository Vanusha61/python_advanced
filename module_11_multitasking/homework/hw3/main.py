import logging
import random
import threading
import time
from typing import List

from threading import Lock

TOTAL_TICKETS: int = 10
MAX_TICKETS = 100
lock = Lock()

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                with lock:
                    if TOTAL_TICKETS <= 0:
                        break
                    self.tickets_sold += 1
                    TOTAL_TICKETS -= 1
                    logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
                    if TOTAL_TICKETS <= 3:
                        self.director()
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))

    def director(self):
        global TOTAL_TICKETS
        global MAX_TICKETS
        if MAX_TICKETS <= 0:
            return f"Билеты закончились"
        counts = min(9, MAX_TICKETS)
        TOTAL_TICKETS += counts
        MAX_TICKETS -= counts


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore(3)
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
