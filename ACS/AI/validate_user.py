#!/usr/local/bin/python3

import json
import pickle
import sys
import os

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
import pandas as pd
import plac
from AI.DataEncoder import DataEncoder


def validate_identity(user_id: "UserId to test input fingerprint with", fingerprint=None):
    try:
        model = pickle.load(open("models/{}/model_{}.dat".format(user_id, user_id), 'rb'))
    except:
        print("No user '{}' found".format(user_id))
        return
    try:
        if fingerprint is None:
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
    return result

if __name__ == "__main__":
    plac.call(validate_identity)
