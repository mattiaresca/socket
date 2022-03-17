
import time
import logging
from threading import Thread

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

def test(i):
  logging.info(f"{i} thread:iniziato")
  time.sleep(3)
  logging.info(f"{i} thread:finito")

for i in range(5):
  t=Thread(target=test, args=(i,))
  t.start()
  t.join()