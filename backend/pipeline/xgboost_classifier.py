import os
import pickle
import numpy as np
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

xgb_model      = None
feature_columns = None


def load_xgb_model():
    global xgb_model, feature_columns
    try:
        with open(os.path.join(MODELS_DIR, 'xgboost_fraud_model.pkl'), 'rb') as f:
            xgb_model = pickle.load(f)
        feature_columns = joblib.load(os.path.join(MODELS_DIR, 'feature_columns.pkl'))
        print(f"XGBoost model loaded. Expects {len(feature_columns)} features.")
    except Exception as e:
        print(f"Error loading XGBoost model: {e}")


load_xgb_model()

# Human-readable descriptions for the top features the model cares about most.
# Keys must match exact column names in feature_columns.pkl.
FEATURE_DESCRIPTIONS = {
    'total_claim_amount':          "Claim amount is outside normal distribution",
    'graph_degree_centrality':     "High network centrality detected for this claimant",
    'graph_clustering_coeff':      "Strong entity clustering pattern in claim network",
    'graph_pagerank':              "Elevated PageRank in fraud network graph",
    'incident_type':               "Suspicious incident type pattern",
    'incident_city':               "High-risk incident location detected",
    'incident_severity':           "Incident severity inconsistent with claim amount",
    'collision_type':              "Collision type inconsistency detected",
    'property_damage':             "Property damage claim anomaly",
    'police_report_available':     "Police report availability pattern",
    'witnesses':                   "Witness count anomaly",
    'insured_relationship':        "Insured relationship risk factor",
    'policy_state':                "Policy state risk profile",
    'months_as_customer':          "Short customer tenure detected",
    'umbrella_limit':              "Umbrella limit anomaly",
}
# Topic feature descriptions (LDA)
for i in range(20):
    FEATURE_DESCRIPTIONS[f'topic_{i}'] = f"Narrative anomaly: Topic {i + 1} pattern match"


def get_top_factors(feature_vector, top_n=3):
    """
    Generate explainability by combining model feature importances with
    the actual values in this specific prediction's feature vector.

    Returns a list of dicts: [{title, description}, ...]
    """
    factors = []

    try:
        if hasattr(xgb_model, 'feature_importances_') and xgb_model.feature_importances_ is not None:
            importances = xgb_model.feature_importances_
            col_names   = list(feature_vector.columns)

            if len(importances) != len(col_names):
                print(
                    f"Warning: Model has {len(importances)} importances but "
                    f"feature vector has {len(col_names)} columns. Skipping explainability."
                )
            else:
                # Pair each feature with its global importance score
                paired = sorted(
                    zip(col_names, importances),
                    key=lambda x: x[1],
                    reverse=True
                )

                for fname, importance in paired:
                    if len(factors) >= top_n:
                        break
                    if importance <= 0:
                        continue
                    title = fname.replace('_', ' ').title()
                    desc  = FEATURE_DESCRIPTIONS.get(
                        fname, f"Feature '{title}' strongly influenced this prediction."
                    )
                    factors.append({"title": title, "description": desc})

    except Exception as e:
        print(f"Warning: Feature importance extraction failed — {e}")

    # Fallback factors if importance extraction failed or returned fewer than top_n
    fallback = [
        {"title": "Narrative Analysis",   "description": "Claim narrative contains anomalous patterns."},
        {"title": "Amount Anomaly",        "description": "Claim amount deviates from expected distribution."},
        {"title": "Network Pattern",       "description": "Suspicious entity relationships detected in network."},
    ]
    while len(factors) < top_n and fallback:
        factors.append(fallback.pop(0))

    return factors[:top_n]


def predict_fraud(fused_vector):
    """
    Execute XGBoost prediction and return structured result with explainability.

    Args:
        fused_vector: DataFrame returned by fuse_features() — exact column
                      order matching feature_columns.pkl.

    Returns:
        dict with keys:
            prediction, fraud_probability, confidence_score,
            risk_level, top_contributing_factors
    """
    if xgb_model is None:
        raise RuntimeError("XGBoost model is not loaded. Check models/xgboost_fraud_model.pkl.")

    # --- Align columns to what the model was trained on ---
    if feature_columns:
        missing = [c for c in feature_columns if c not in fused_vector.columns]
        extra   = [c for c in fused_vector.columns if c not in feature_columns]

        if missing:
            print(f"Warning: {len(missing)} columns missing from fused vector, filling with 0.0: {missing}")
            for col in missing:
                fused_vector[col] = 0.0

        if extra:
            print(f"Warning: Dropping {len(extra)} unexpected columns: {extra}")

        # Enforce exact column order — this is critical for XGBoost tree splits
        fused_vector = fused_vector[feature_columns]

    # --- Predict ---
    try:
        proba_array = xgb_model.predict_proba(fused_vector)[0]
    except Exception as e:
        raise RuntimeError(f"XGBoost prediction failed: {e}") from e

    # proba_array[1] = P(fraud), proba_array[0] = P(genuine)
    fraud_prob = float(proba_array[1]) if len(proba_array) > 1 else float(proba_array[0])

    # --- 3-Level Risk Classification ---
    if fraud_prob >= 0.75:
        prediction_label = "Fraudulent Claim"
        risk_level        = "High"
    else:
        prediction_label = "Genuine Claim"
        risk_level        = "Low"

    # Confidence: how far the probability is from the 0.5 decision boundary, scaled to [0, 1]
    confidence = abs(fraud_prob - 0.5) * 2.0

    factors = get_top_factors(fused_vector)

    print("\n====================")
    print(f"Prediction:        {prediction_label}")
    print(f"Fraud Probability: {fraud_prob:.4f}  ({fraud_prob * 100:.2f}%)")
    print(f"Risk Level:        {risk_level}")
    print(f"Confidence:        {confidence:.4f}  ({confidence * 100:.2f}%)")
    print("====================\n")

    return {
        "prediction":               prediction_label,
        "fraud_probability":        f"{fraud_prob * 100:.2f}%",
        "confidence_score":         f"{confidence * 100:.2f}%",
        "risk_level":               risk_level,
        "top_contributing_factors": factors,
    }