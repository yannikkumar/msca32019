from threading_MSCA2020Q4 import Bank
import time
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')

console.setFormatter(formatter)

logger.addHandler(console)



if __name__ == '__main__':
    logger.info("starting")
    b = Bank("Scrooge Trust")
    logger.info("Bank constructed")
    b.open_for_business()
    cust = ('Huey', 20)
    b.receive_customer(cust)
    b.close()
    logger.info(f"Bank LEDGER: {b.ledger}")