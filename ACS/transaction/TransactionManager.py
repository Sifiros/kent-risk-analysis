from .TransactionTask import TransactionTask

# Manage each requests part of the transaction until its entire completion
# run() is the main loop blocking until reaching state VALIDATED or ABORTED
class TransactionManager():

    def __init__(self, transaction_id, completion_callback):
        self.transaction = TransactionTask(transaction_id)
        self.completion_callback = completion_callback

        self.request_callbacks = {
            TransactionTask.WAITING_USER_PROFILE: self.check_user_profile,
            TransactionTask.WAITING_LONGPOLL_REQUEST: self.handle_challenge_request,
            TransactionTask.WAITING_CHALLENGE_REQUEST: self.handle_challenge_request,
            TransactionTask.WAITING_CHALLENGE_RESPONSE: self.check_challenge_response,
            TransactionTask.WAITING_FINAL_VALIDATION: self.handle_final_validation,
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

            self.request_callbacks[cur_state](self, last_data)

    # Feed data to be processed in this transaction
    def feed_data(self, body):
        self.transaction.feed_data(body)

    def on_step_completion(self, next_state, step_result=None):
        if step_result != None:
            self.completion_callback(self, self.transaction.step, step_result)
        # If current step has been successfully completed
        if next_state != TransactionTask.ERROR:
            self.transaction.validate_current_step()
            self.transaction.state = next_state

    ########### Requests handlers ###########

    # WAITING_USER_PROFILE -> PROFILE_CHECKING -> (WAITING_CHALLENGE_REQUEST OR VALIDATED)
    def check_user_profile(self, user_profile):
        self.on_step_completion(TransactionTask.PROFILE_CHECKING)
        print("AI checking user profile ...")
        result = {}
        self.on_step_completion(TransactionTask.WAITING_LONGPOLL_REQUEST, result)
        print("Checked : a chal is needed")
        return True

    # WAITING_LONGPOLL_REQUEST -> WAITING_CHALLENGE_REQUEST
    # WAITING_CHALLENGE_REQUEST -> WAITING_CHALENGE_RESPONSE
    # dispatch to the right handler (it is a longpoll or challenge request ?)
    def handle_challenge_request(self, request):
        print("Handling challenge request")
        # Detect request type (2 different types handled by this function)
        # assume the request type given what we still need or detect the type if we haven't received anything yet
        remaining_steps = step([TransactionTask.WAITING_LONGPOLL_REQUEST, TransactionTask.WAITING_CHALLENGE_REQUEST]) - self.transaction.steps_done
        if len(remaining_steps) > 1:
            request_type = TransactionTask.WAITING_LONGPOLL_REQUEST if 'longpoll' in request else TransactionTask.WAITING_CHALLENGE_REQUEST
        else:
            request_type = list(remaining_steps)[0]

        # force current state with detected type & process request
        self.transition.state = request_type
        if request_type == TransactionTask.WAITING_LONGPOLL_REQUEST:
            result = self.handle_longpoll_request(request)
        else:            
            result = self.handle_challenge_request(request)

        # Transition on next state
        if result is not False: # TODO error handling via different result classes
            remaining_steps -= set([request_type])
            next_state = list(remaining_steps)[0] if len(remaining_steps) > 0 else TransactionTask.WAITING_CHALENGE_RESPONSE
            self.on_step_completion(next_state, result)
    
    def handle_longpoll_request(self, request):
        print("Handling longpoll request")
        return True

    def handle_challenge_request(self, request):
        print("Handling challenge front html request")
        return True        

    # WAITING_CHALLENGE_RESPONSE  -> WAITING_FINAL_VALIDATION
    def check_challenge_response(self, response):
        print("Handling CHALLENGE RESPONSE")
        self.on_step_completion(TransactionTask.WAITING_FINAL_VALIDATION, {})

    # WAITING_FINAL_VALIDATION -> VALIDATED
    def handle_final_validation(self, validation):
        print("Finally validated by 3DS server")
        self.on_step_completion(TransactionTask.VALIDATED, {})


    
