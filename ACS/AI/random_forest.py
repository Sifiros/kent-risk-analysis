#!/usr/local/bin/python3

import plac
import sys
import os
import random
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
# sys.path.append('/chemin/vers/le/dossier/parent/du/module/a/importer')
sys.path.append('/home/martin/kent/finalProject/kent-risk-analysis/ACS/AI')
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.io import arff
import pandas as pd
from AI.generate_fingerprints import generate_formatted_fingerprints
# from . import generate_fingerprints

def generate_model(fingerprints, browser_id):
    df = pd.DataFrame(fingerprints)
    yVar = df.loc[:,'browser_id']
    X_train, X_test, y_train, y_test = train_test_split(df, yVar, test_size=0.2)
    print (X_train.shape, y_train.shape)
    print (X_test.shape, y_test.shape)
    # print(df)

def get_distinct_browser_ids(fingerprints):
    browser_ids = set()
    for fingerprint in fingerprints:
        browser_ids.add(fingerprint["browser_id"])
    return list(browser_ids)

def main():
    fingerprints = generate_formatted_fingerprints(nb_browsers=2, nb_days=100)
    # split fingerprints between training / testing sets
    browser_ids = get_distinct_browser_ids(fingerprints)

    print("Running training with {} fingerprints of {} browsers.".format(len(fingerprints), len(browser_ids)))
    for browser_id in browser_ids:
        print("Processing {}".format(browser_id))
        generate_model(fingerprints, browser_id)

if __name__ == "__main__":
    plac.call(main)