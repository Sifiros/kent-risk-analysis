#!/usr/local/bin/python3

import json
import pickle
import sys

import pandas as pd
import plac
from DataEncoder import DataEncoder


def validate_identity(user_id: "UserId to test input fingerprint with"):
    try:
        model = pickle.load(open("models/{}/model_{}.dat".format(user_id, user_id), 'rb'))
    except:
        print("No user '{}' found".format(user_id))
        return
    try:
        fingerprint = json.loads(sys.stdin.read())
        if type(fingerprint) != list:
            fingerprint = [fingerprint]
        fingerprint = [DataEncoder(cur).m_formated_data for cur in fingerprint]
    except:
        print("Invalid input fingerprint JSON")
        return
    fingerprint = pd.DataFrame(fingerprint)
    result = model.predict(fingerprint)
    print(result)

if __name__ == "__main__":
    plac.call(validate_identity)