import threading
import time
from .TransactionTask import TransactionTask
from config import HTTP_PORT, PUBLIC_IP
from acs import AcsPacketFactory
from Database import database
from AI.random_forest import generate_model
from AI.validate_user import validate_identity

# Manage each requests part of the transaction until its entire completion
# run() is the main loop blocking until reaching state VALIDATED or ABORTED
class TransactionManager():

    def __init__(self, transaction_id, completion_callback):
        self.transaction = TransactionTask(transaction_id)
        self.completion_callback = completion_callback

        self.request_callbacks = {
            TransactionTask.WAITING_USER_PROFILE: self.preparing_ai,
            TransactionTask.WAITING_AUTH_REQUEST: self.preparing_ai,
            TransactionTask.WAITING_CHALLENGE_SOLUTION: self.check_challenge_solution,
        }

    @property
    def is_running(self):
        return self.transaction.state != TransactionTask.VALIDATED and self.transaction.state != TransactionTask.ABORTED

    def process(self, packet):
        cur_state = self.transaction.state
        if not self.is_running:
            return
        self.request_callbacks[cur_state](packet)

    def on_step_completion(self, next_state, step_result=None):
        if step_result != None:
            self.completion_callback(self, self.transaction.state, step_result)
        # If current step has been successfully completed
        if next_state != TransactionTask.ERROR:
            self.transaction.validate_current_step()
            self.transaction.state = next_state

    ########### Requests handlers ###########

    # 1. WAITING_USER_PROFILE -> WAITING_AUTH_REQUEST
    # or WAITING_AUTH_REQUEST -> WAITING_USER_PROFILE
    # then second state -> (WAITING_CHALLENGE_SOLUTION OR VALIDATED)
    def preparing_ai(self, packet):
        if "messageType" in packet and packet["messageType"] == "AReq":
            self.transaction.state = TransactionTask.WAITING_AUTH_REQUEST
            self.check_auth_request(packet)
        else:
            self.transaction.state = TransactionTask.WAITING_USER_PROFILE
            self.check_user_profile(packet)

        if self.transaction.user_profile is not None and self.transaction.purchase is not None:
            self.run_ai()

    def check_user_profile(self, user_profile):
        print("Storing fingerprint ...")
        self.transaction.user_profile = user_profile
        self.on_step_completion(TransactionTask.WAITING_AUTH_REQUEST)

    def check_auth_request(self, purchase_info):
        print("Handling auth request ...")
        self.transaction.purchase = purchase_info
        self.transaction.notification_url = purchase_info["notificationURL"]
        self.on_step_completion(TransactionTask.WAITING_USER_PROFILE)

    def run_ai(self):
        purchase, user_profile = (self.transaction.purchase, self.transaction.user_profile)
        user_id = purchase["acctNumber"]
        user_profile["browser_id"] = user_id # for AI needs
        user_profile["day"] = int(time.time()) # for AI needs
        database.append_user_fingerprint(user_id, user_profile)
        fingerprints = database.get_user_fingerprints(user_id)
        print("Running AI ...")
        # TODO: ensure same input formats than generate_fingerprint output
        try:
            if int(purchase['purchaseAmount']) > 500:
                raise Exception("High purchase amount, trigger a challenge")
            validated = validate_identity(user_id, user_profile)[0] == 1
        except:
            validated = False

        if validated:
            print("User {} authentified !".format(user_id))
        else:
            print("User {} looks suspicious, asking for a challenge !".format(user_id))

        checking_result = AcsPacketFactory.get_aResp_packet(
            threeDSServerTransID=self.transaction.id,
            transStatus="Y" if validated else "C",
            acsChallengeMandated="N" if validated else "Y",
            acsURL='http://{}:{}/challrequest'.format(PUBLIC_IP, HTTP_PORT)
        )
        # Re train user model
        usermodel_training = threading.Thread(target=generate_model, args=(database.get_all_fingerprints(), user_id))
        usermodel_training.start()
        self.on_step_completion(TransactionTask.WAITING_CHALLENGE_SOLUTION, checking_result)

    # 3. WAITING_CHALLENGE_SOLUTION  -> VALIDATED
    def check_challenge_solution(self, response):
        print("Handling challenge response ...")
        # if invalid response, reply an error
        # otherwise, store http request in order to reply after final validation
        self.on_step_completion(TransactionTask.VALIDATED, AcsPacketFactory.get_cResp_packet(
            threeDSServerTransID=self.transaction.id,
            challengeCompletionInd="Y"
        ))