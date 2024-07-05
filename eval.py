import os

import numpy as np
import pandas as pd


def load_user_study_data(directory_path):
    raw = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            raw += [(filename[:-len(".csv")], f"{directory_path}/{filename}")]

    long, short, ai = {}, {}, {}
    for fn, fp in raw:
        participant, mode, uid = tuple(fn.split("_"))

        resp = pd.read_csv(fp)

        if mode == "long":
            long[participant] = resp
        elif mode == "ai":
            ai[participant] = resp
        else:
            short[participant] = resp

    return long, short, ai


def accuracy(dir_path):
    long, short, ai = load_user_study_data(dir_path)

    accuracy_of_short, accuracy_of_ai = [], []
    for pi in long:
        l, s, a = long[pi], short[pi], a[pi]

        for ix, long_responses in enumerate(l.iterrows()):
            short_responses = s.iloc[ix]
            ai_responses = ai.iloc[ix]

            if short_responses["response"] == long_responses["response"]:
                accuracy_of_short += [1]
            else:
                accuracy_of_short += [0]

            if ai_responses["response"] == long_responses["response"]:
                accuracy_of_ai += [1]
            else:
                accuracy_of_ai += [0]

    accuracy_of_short = np.sum(accuracy_of_short) / len(accuracy_of_short)
    accuracy_of_ai = np.sum(accuracy_of_ai) / len(accuracy_of_ai)

    print("SHORT ACCURACY = ", accuracy_of_short)
    print("AI ACCURACY = ", accuracy_of_ai)

accuracy("./responses")