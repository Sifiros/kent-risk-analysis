from threading import Thread
from .TransactionTask import TransactionTask
from .TransactionManager import TransactionManager

# This class handles a list of TransactionManager threads, each responsible of 1 current transaction
# Receive each transaction step result & give them back to the ACS (on_step_completion)
class TransactionController():

    def __init__(self):
        self.managers = {}

    # Called for each transaction request (whatever its type is)
    # Dispatch the request handling to the right thread
    # Create a new manager thread if the transaction just begins
    def handle_transaction_request(self, transaction_id, body):
        if transaction_id not in self.managers:
            # First request, body must be the auth request (with user profile)
            manager = TransactionManager(transaction_id, self.on_step_completion)
            self.managers[transaction_id] = manager
            # Run manager main loop inside a new thread
            thread = Thread(target=manager.run, args=[])
            thread.start()
        
        # Feed this request in the transaction
        self.managers[transaction_id].feed_data(body)
        
    # Callback called by a manager each time a step is completed, requiring its HTTP response
    def on_step_completion(self, manager, completed_step, result):
        if completed_step == TransactionTask.END:
            del self.managers[manager.transaction.id]
            return

        print("{} has finished step {} with result {}! ".format(
            manager.transaction.id, completed_step, result
        ))
        