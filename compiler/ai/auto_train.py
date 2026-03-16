import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

DATASET = "training_data.csv"
MODEL = "optimizer_model.pkl"


def retrain():

    if not os.path.exists(DATASET):
        return

    try:
        data = pd.read_csv(DATASET)
    except Exception:
        print("Dataset corrupted. Resetting training data.")
        os.remove(DATASET)
        return

    # Need minimum data
    if len(data) < 10:
        return

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10
    )

    model.fit(X, y)

    with open(MODEL, "wb") as f:
        pickle.dump(model, f)

    print("ML model retrained with", len(data), "samples")
