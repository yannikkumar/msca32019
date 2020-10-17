import unittest
import random
import time
import logging

logger = logging.getLogger('BANK')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())



#YOUR IMPORTS HERE
import queue
import threading
import time

# YOUR CODE HERE
class WriteError(Exception):
    pass


class BankClosedException(Exception):
    pass


class Bank():
    def __init__(self, name, teller_count=4):
        self.name = name
        self._Bank__teller_count = teller_count
        self.is_open = False
        self._lock = threading.Lock()
        self._Bank__ledger = {}
        self._Bank__queue = queue.Queue()
        self._Bank__tellers = [threading.Thread(target=self._teller_task,
                                                name="thread_" + str(i))
                               for i in range(1, self.teller_count + 1)]
    
    @property
    def teller_count(self):
        return self._Bank__teller_count
    
    @teller_count.setter
    def teller_count(self, teller_count):
        if teller_count < 1:
            raise ValueError ("Teller count must be >1")
        self._Bank__teller_count = teller_count
    
    @property
    def ledger(self):
        return self._Bank__ledger

    @ledger.setter
    def ledger(self, *args, **kwargs):
        raise WriteError ("You cannot write directly to the ledger")
    
    def open_for_business(self):
        self.is_open = True
        for teller in self._Bank__tellers:
            teller.start()
    
    def close(self):
        self.is_open = False
        for teller in self._Bank__tellers:
            teller.join()
    
    def receive_customer(self, customer):
        if self.is_open:
            self._Bank__queue.put(customer)
        else:
            raise BankClosedException ("Bank is not open to receive customers")
    
    def _teller_task(self):
        time.sleep(2)
        while not self._Bank__queue.empty():
            current_customer = self._Bank__queue.get()
            self._lock.acquire()
            if current_customer[0] in self._Bank__ledger:
                current_balance = self._Bank__ledger[current_customer[0]]
                transaction = current_customer[1]
                if current_balance + transaction >= 0:
                    self._Bank__ledger[current_customer[0]] += current_customer[1]
            else:
                transaction = current_customer[1]
                if 0 + transaction >= 0:
                    self._Bank__ledger[current_customer[0]] = current_customer[1]
            self._lock.release()
    
    


######################################
##    DON'T CODE AFTER THIS LINE   ###
######################################


class ThreadingTests(unittest.TestCase):

    def test_bank_class_defined(self):
        self.assertIn('Bank', globals())

    def test_bank_constructor_sets_public_name(self):
        b = Bank("Scrooge Trust")
        self.assertEqual(b.name, "Scrooge Trust")

    def test_bank_constructor_sets_private_number_of_tellers(self):
        b = Bank("Scrooge Trust", 4)
        self.assertEqual(b._Bank__teller_count, 4)

    def test_bank_allows_changing_teller_count(self):
        # you'll need to use the @property and @property.setter decorators
        b = Bank("Scrooge Trust")
        b.teller_count = 6
        self.assertEqual(b.teller_count, 6)
        self.assertEqual(b.teller_count, b._Bank__teller_count)

    def test_setting_teller_count_less_than_1_throws_error(self):
        b = Bank("Scrooge Trust")
        with self.assertRaises(ValueError):
            b.teller_count = -4

    def test_bank_contructor_initializes_private_ledger(self):
        b = Bank("Scrooge Trust")
        self.assertTrue(isinstance(b._Bank__ledger, dict))

    def test_can_read_but_not_overwrite_to_ledger(self):
        b = Bank("Scrooge Trust")
        self.assertEqual(b.ledger, {})
        # You will need to define your own Exception, WriteError
        with self.assertRaises(WriteError):
            b.ledger = {'sneaky': -10000000}

    def test_bank_has_open_for_business_method(self):
        self.assertTrue(hasattr(Bank, "open_for_business"))

    def test_makes_import_queue(self):
        self.assertIn('queue',globals())

    def test_bank_constructor_initializes_a_private_queue(self):
        b = Bank("Scrooge Trust")
        self.assertTrue(isinstance(b._Bank__queue, queue.Queue))

    def test_bank_is_initialized_to_be_closed(self):
        b = Bank("Scrooge Test")
        self.assertFalse(b.is_open)

    def test_open_for_business_sets_bank_to_open(self):
        b = Bank("Scrooge Trust")
        b.open_for_business()
        self.assertTrue(b.is_open)

    def test_bank_has_close_method_which_closes_bank(self):
        b = Bank("Scrooge Test")
        b.open_for_business()
        self.assertTrue(b.is_open)
        b.close()
        self.assertFalse(b.is_open)

    def test_bank_has_receive_customer_method(self):
        self.assertTrue(hasattr(Bank, "receive_customer"))

    def test_receive_customer_puts_passed_cust_in_queue(self):
        b = Bank("Scrooge Trust")
        b.is_open = True
        b.receive_customer("new cust")
        self.assertFalse(b._Bank__queue.empty())
        self.assertEqual(b._Bank__queue.get(), "new cust")

    def test_receive_customer_only_puts_cust_in_queue_if_bank_is_open(self):
        b = Bank("Scrooge Trust")
        with self.assertRaises(BankClosedException):
            b.receive_customer("new cust")
        self.assertTrue(b._Bank__queue.empty())

    def test_bank_has_protected_teller_task_method(self):
        b = Bank("Scrooge Test")
        self.assertTrue(hasattr(Bank, "_teller_task"))

    def test_makes_import_threading(self):
        self.assertIn('threading',globals())

    def test_bank_constructor_initializes_private_list_of_threads(self):
        b = Bank("Scrooge Trust")
        self.assertTrue(isinstance(b._Bank__tellers, list))
        self.assertEqual(len(b._Bank__tellers), 4)
        self.assertTrue(isinstance(b._Bank__tellers[0], threading.Thread))
        self.assertFalse(b._Bank__tellers[0].is_alive())
        self.assertEqual(len(threading.enumerate()), 1)

    def test_bank_constructor_initializes_threads_to_target_teller_task(self):
        b = Bank("Scrooge Trust")
        self.assertEqual(b._Bank__tellers[0]._target.__name__, "_teller_task")

    def test_teller_task_runs_while_bank_is_open(self):
        b = Bank("Scrooge Trust")
        b.open_for_business()
        t = threading.Thread(target=b._teller_task)
        t.start()
        self.assertTrue(t.is_alive())
        b.close()
        t.join()
        self.assertFalse(t.is_alive())

    def test_when_bank_opens_tellers_are_started(self):
        b = Bank("Scrooge Trust")
        b.open_for_business()
        self.assertTrue(b._Bank__tellers[0].is_alive())
        self.assertTrue(all([teller.is_alive() for teller in b._Bank__tellers]))
        b.close()
        self.assertFalse(any([teller.is_alive() for teller in b._Bank__tellers]))

    def test_bank_constructor_initializes_a_protected_lock(self):
        b = Bank("Scrooge Trust")
        self.assertTrue(hasattr(b, "_lock"))

    def test_teller_accepts_customer_and_updates_ledger(self):
        b = Bank("Scrooge Test")
        cust = ('Huey', 20)
        b.open_for_business()
        b.receive_customer(cust)
        b.close()
        self.assertEqual(b.ledger, {cust[0]: cust[1]})

    def test_one_teller_accepts_many_customers_and_updates_ledger(self):
        b = Bank("Scrooge Trust", 1)
        b.open_for_business()
        random.seed(0)
        for _ in range(100):
            cust = random.choice(['Huey', 'Dewey', 'Lewey'])
            amount = random.randint(1, 100)
            b.receive_customer((cust, amount))
        time.sleep(1)
        b.close()
        self.assertEqual(b.ledger['Dewey'], 1927)
        self.assertEqual(b.ledger['Huey'], 2456)
        self.assertEqual(b.ledger['Lewey'], 1164)

    def test_teller_wont_allow_negative_balance(self):
        b = Bank("Scrooge Trust", 1)
        b.open_for_business()
        random.seed(0)
        for _ in range(100):
            cust = random.choice(['Huey', 'Dewey', 'Lewey'])
            amount = random.randint(-100, 100)
            b.receive_customer((cust, amount))
        time.sleep(1)
        b.close()
        self.assertEqual(b.ledger['Dewey'], 174)
        self.assertEqual(b.ledger['Huey'], 133)
        self.assertEqual(b.ledger['Lewey'], 31)

    def test_many_tellers_accept_many_customers(self):
        b = Bank("Scrooge Trust", 4)
        b.open_for_business()
        random.seed(0)
        for _ in range(100):
            cust = random.choice(['Huey', 'Dewey', 'Lewey'])
            amount = random.randint(-100, 100)
            b.receive_customer((cust, amount))
        time.sleep(1)
        b.close()
        self.assertEqual(b.ledger['Dewey'], 174)
        self.assertEqual(b.ledger['Huey'], 133)
        self.assertEqual(b.ledger['Lewey'], 31)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)