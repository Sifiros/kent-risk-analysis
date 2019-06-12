from threading import Thread
from .TransactionManager import TransactionManager

# This class handles a list of TransactionManager threads, each responsible of 1 current transaction
# Receive each transaction step result & give them back to the ACS (on_step_completion)
class TransactionController():

    def __init__(self, acs_callback):
        self.managers = {}
        self.acs_callback = acs_callback

    # Called for each transaction request (whatever its type is)
    # Dispatch the request handling to the right thread
    # Create a new manager thread if the transaction just begins
    def handle_transaction_request(self, transaction_id, body):
        if transaction_id not in self.managers:
            # First request, body must be the auth request (with user profile)
            manager = TransactionManager(transaction_id, self.on_step_completion)
            self.managers[transaction_id] = manager
        
        # Feed this request in the transaction
        self.managers[transaction_id].process(body)
        
    # Callback called by a manager each time a step is completed, requiring its HTTP response
    def on_step_completion(self, manager, completed_step, result):
        print("{} has finished step {} with result {}! ".format(
            manager.transaction.id, completed_step, result
        ))
        self.acs_callback(manager.transaction.id, result)
        