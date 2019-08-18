#!/usr/local/bin/python3

import copy
import json
import os
import pickle
import random
import sys
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

import numpy as np
import pandas as pd
import plac
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from AI.DataEncoder import DataEncoder
from AI.generate_fingerprints import generate
from Database import database

models_dir = DOSSIER_COURRANT + '/models/'

def generate_model(fingerprints, browser_id, validation_stage=False, add_to_database=False, debug=False):
    print("Training {} model ...".format(browser_id))
    encoded_fingerprints = []
    browser_fingerprints = []
    for fingerprint in fingerprints:
        authenticity = 1 if fingerprint["browser_id"] == browser_id else 0
        if authenticity == 1:
            browser_fingerprints.append(fingerprint.copy())
        encoded = DataEncoder(fingerprint).m_formated_data
        encoded["authenticity"] = authenticity
        encoded_fingerprints.append(encoded)

    df = pd.DataFrame(encoded_fingerprints)
    yVar = df.loc[:,'authenticity']
    xVar = [col for col in df.head() if col != 'authenticity']
    df = df[xVar]
    if validation_stage:
        X_train, X_test, y_train, y_test = train_test_split(df, yVar, test_size=0.7)
    else:
        X_train, y_train = df, yVar

    model = RandomForestClassifier(n_jobs=2, random_state=0)
    model.fit(X_train, y_train)
    if add_to_database:
        database.append_user_fingerprint(browser_id, browser_fingerprints)

    if validation_stage:
        preds = model.predict(X_test)
        print("Confusion matrix : ")
        print(pd.crosstab(y_test, preds, rownames=['Actual Result'], colnames=['Predicted Result']))
    feature_importances = list(zip(X_train, model.feature_importances_))
    if debug:
        print("Features importance : ")
        print(feature_importances)
        print("Saving model ...")
    if not os.path.exists(models_dir + browser_id):
        os.mkdir(models_dir + browser_id)
    pickle.dump(model, open(models_dir + "{}/model_{}.dat".format(browser_id, browser_id), 'wb'))
    with open(models_dir + "{}/fingerprints.json".format(browser_id), "w") as f:
        browser_fingerprints = sorted(browser_fingerprints, key=lambda cur: cur['day'])
        f.write(json.dumps(browser_fingerprints))
    with open(models_dir + "{}/feature_importances.json".format(browser_id), "w") as f:            
        feature_importances = sorted(feature_importances, key=lambda cur: cur[1])
        f.write(json.dumps(feature_importances))
    print("{} training done and persisted.".format(browser_id))

def get_distinct_browser_ids(fingerprints):
    browser_ids = set()
    for fingerprint in fingerprints:
        browser_ids.add(fingerprint["browser_id"])
    return list(browser_ids)

def main():
    if not os.path.exists("models"):
        os.mkdir("models")
    fingerprints = generate(nb_browsers=60, nb_days=300)
    # split fingerprints between training / testing sets
    browser_ids = get_distinct_browser_ids(fingerprints)

    print("Running training with {} fingerprints of {} browsers.".format(len(fingerprints), len(browser_ids)))
    for browser_id in browser_ids:
        generate_model(
            fingerprints,
            browser_id,
            validation_stage=True,
            add_to_database=True,
            debug=True
        )

if __name__ == "__main__":
    plac.call(main)
