import queue

class TransactionTask():
    # 1. a transaction task is created as soon as a USER_PROFILE request (coming from the harvester) initiates the transaction
    WAITING_USER_PROFILE = 1 # browser fingerprint
    # 2. Wait for auth request
    WAITING_AUTH_REQUEST = 2 # purchase info
    # AI processing gathered data from last steps
    #   --> if OK : transaction validated. We stop here.
    #   --> otherwise : tells back a challenge is needed
    # 3. If a challenge was needed & sent, wait for challenge result
    WAITING_CHALLENGE_SOLUTION = 3
    # If challenge is not validated ; reply back an http error making reloop on another WAITING_CHALLENGE_SOLUTION
    # If validated ; keep transaction alive to answer it after final validatio
    VALIDATED = 4 # challenge validated 
    ABORTED = 5 # Aborted
    ERROR = 6
    
    def __init__(self, transaction_id):
        self.state = TransactionTask.WAITING_USER_PROFILE
        self.id = transaction_id
        self.data_queue = queue.Queue()
        self.steps_done = set()
        self.user_profile = None
        self.purchase = None

    # Append data to be processed in the queue
    def feed_data(self, data):
        self.data_queue.put(data)

    # Get data to be processed
    def get_data(self):
        return self.data_queue.get(block=True)

    # Assigns current step to steps_done
    def validate_current_step(self):
        self.steps_done.add(self.state)


    