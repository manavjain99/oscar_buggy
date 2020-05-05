import concurrent.futures
import logging
import queue
import random
import threading
import time

def producer(queue, event):
    """Pretend we're getting a number from the network."""
    while (event.is_set() == False):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        queue.put(message)

    logging.info("Producer received event. Exiting")

def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    while (event.is_set() == False) or not queue.empty():
        message = queue.get()
        logging.info(
            "Consumer storing message: %s (size=%d)", message, queue.qsize()
        )

    logging.info("Consumer received event. Exiting")

    

def f1():
    while(event.is_set()):
        print("event set")

def f2():
    while (not event.is_set()):
        print("event not set")
    
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    event = threading.Event()
    #event.set()
    pipeline = queue.Queue(maxsize=10)
    while (1):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(f1)
            executor.submit(f2)
            event.set()
            #event.clear()
            time.sleep(0.001)
            logging.info("Main: about to set event")
            #event.set()

            event.clear()
