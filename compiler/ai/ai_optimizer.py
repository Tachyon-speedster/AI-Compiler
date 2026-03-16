import os
import pickle
import pandas as pd

from ..optimizer.optimizer import apply_parallel, optimize
from compiler.ai.feature_extractor import extract_features

MODEL_FILE = "optimizer_model.pkl"


def ai_select(ir_program):

    # -----------------------------
    # Check if ML model exists
    # -----------------------------

    if not os.path.exists(MODEL_FILE):
        print("\n⚠ AI model not found. Skipping AI optimization.")
        return ir_program

    # -----------------------------
    # Load trained model
    # -----------------------------

    try:
        with open(MODEL_FILE, "rb") as f:
            model = pickle.load(f)

    except Exception as e:
        print("\n⚠ Failed to load ML model:", e)
        return ir_program

    # -----------------------------
    # Extract features
    # -----------------------------

    features = extract_features(ir_program)

    features_df = pd.DataFrame([features])

    # -----------------------------
    # Align features with model
    # -----------------------------

    try:

        expected = model.feature_names_in_

        features_df = features_df.reindex(columns=expected, fill_value=0)

    except Exception:
        pass

    # -----------------------------
    # Predict optimization
    # -----------------------------

    try:

        prediction = model.predict(features_df)[0]

    except Exception as e:
        print("\n⚠ ML prediction failed:", e)
        return ir_program

    # -----------------------------
    # Debug prints
    # -----------------------------

    print("\nAI Optimization Decision")
    print("-----------------------")
    print("Features:", features)

    try:
        print("Model expects:", model.feature_names_in_)
        print("Features given:", list(features_df.columns))
    except:
        pass

    print("Selected optimization:", prediction)

    # -----------------------------
    # Apply optimization
    # -----------------------------

    if prediction == "parallel":

        ir_program = apply_parallel(ir_program)

    elif prediction == "formula":

        ir_program = optimize(ir_program)

    else:

        print("No optimization applied.")

    return ir_program

