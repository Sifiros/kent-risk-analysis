
# A transaction task is created as soon as an auth request is received with a new transaction id
# auth request contains profile data, fed into our AI : 
# 1. PROFILE_CHECKING
#   --> 2. If OK, VALIDATED --> transaction finished. We stop here.

#   ---> otherwise, if any doubt raised by our ai:
# 2. a challenge is required : WAITING_LONGPOLL_REQUEST -> WAITING_CHALLENGE_REQUEST
# When LONGPOLL + CHALLENGE_REQUEST received : 
# 3. WAITING_CHALLENGE_RESPONSE
# If received response is not valid; reply an http error 
# If validated ; reply 200 + send a "validated challenge" request to the 3DS server
# 4. WAITING_FINAL_VALIDATION
# When 3DS server finally answered to our last validation request ; 
# 5. VALIDATED 

class TransactionTask():
    # Waiting for the first request data : user profile
    WAITING_USER_PROFILE = 1
    # AI processing received transaction id / profile datas
    PROFILE_CHECKING = 2
    # After we replied back AI results, if not validated, wait for challenge beginning
    WAITING_LONGPOLL_REQUEST = 3 # Wait for challenge longpoll request
    WAITING_CHALLENGE_REQUEST = 4 # Wait for challenge html request
    # After we replied back challenge html, wait for challenge result
    WAITING_CHALLENGE_RESPONSE = 5 # challenge html + longpoll challenge request
    # If challenge is not validated ; reply back an http error making reloop on another CHALLENGE_RESPONSE
    # If validated ; also send a "validated challenge" req to 3DS server and :
    WAITING_FINAL_VALIDATION = 6
    # after receiving "result res" from 3DS server, reply the longpoll request (opened on CHALLENGE_REQUEST)
    VALIDATED = 7 # challenge validated 
    ABORTED = 8 # Aborted
    ERROR = 9
    
    def __init__(self, transaction_id):
        self.state = WAITING_USER_PROFILE
        self.id = transaction_id
        self.data_queue = Queue()
        self.steps_done = set()

    # Append data to be processed in the queue
    def feed_data(self, data):
        self.data_queue.put(data)

    # Get data to be processed
    def get_data(self):
        return self.data_queue.get(block=True)

    # Assigns current step to steps_done
    def validate_current_step(self):
        self.steps_done.add(self.state)


    