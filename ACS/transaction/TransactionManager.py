from .TransactionTask import TransactionTask

# Manage each requests part of the transaction until its entire completion
# run() is the main loop blocking until reaching state VALIDATED or ABORTED
class TransactionManager():

    def __init__(self, transaction_id, completion_callback):
        self.transaction = TransactionTask(transaction_id)
        self.completion_callback = completion_callback

        self.request_callbacks = {
            TransactionTask.WAITING_USER_PROFILE: self.check_user_profile,
            TransactionTask.WAITING_AUTH_REQUEST: self.check_auth_request,
            TransactionTask.WAITING_CHALLENGE_SOLUTION: self.check_challenge_solution,
        }

    @property
    def is_running(self):
        return self.transaction.state != TransactionTask.VALIDATED and self.transaction.state != TransactionTask.ABORTED

    def abort(self):
        self.transaction.state = TransactionTask.ABORTED
        self.feed_data(None)

    def run(self):
        while self.is_running:
            # Wait for data
            last_data = self.transaction.get_data()
            cur_state = self.transaction.state
            if not self.is_running:
                break
            self.request_callbacks[cur_state](last_data)

        print("Transaction {} finished.".format(self.transaction.id))

    # Feed data to be processed in this transaction
    def feed_data(self, body):
        self.transaction.feed_data(body)

    def on_step_completion(self, next_state, step_result=None):
        if step_result != None:
            self.completion_callback(self, self.transaction.state, step_result)
        # If current step has been successfully completed
        if next_state != TransactionTask.ERROR:
            self.transaction.validate_current_step()
            self.transaction.state = next_state

    ########### Requests handlers ###########

    # 1. WAITING_USER_PROFILE -> WAITING_AUTH_REQUEST
    def check_user_profile(self, user_profile):
        print("RECEIVED USER PROFILE ...")
        print(user_profile)
        self.transaction.user_profile = user_profile
        self.on_step_completion(TransactionTask.WAITING_AUTH_REQUEST)

    # 2. WAITING_AUTH_REQUEST -> (WAITING_CHALLENGE_SOLUTION OR VALIDATED)
    def check_auth_request(self, purchase_info):
        print("Received auth request")
        print(purchase_info)
        print("Running AI")
        print("A chal is needed")
        checking_result = None # is a challenge needed ? 
        self.on_step_completion(TransactionTask.WAITING_CHALLENGE_SOLUTION, checking_result)

    # 3. WAITING_CHALLENGE_SOLUTION  -> VALIDATED
    def check_challenge_solution(self, response):
        print("Handling CHALLENGE RESPONSE")
        print(response)
        # if invalid response, reply an error
        # otherwise, store http request in order to reply after final validation
        self.on_step_completion(TransactionTask.VALIDATED, {})