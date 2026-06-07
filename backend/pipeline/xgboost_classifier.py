import os
import pickle
import numpy as np
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

xgb_model = None
feature_columns = None

def load_xgb_model():
    global xgb_model, feature_columns
    try:
        with open(os.path.join(MODELS_DIR, 'xgboost_fraud_model.pkl'), 'rb') as f:
            xgb_model = pickle.load(f)
        feature_columns = joblib.load(os.path.join(MODELS_DIR, 'feature_columns.pkl'))
        print("XGBoost model and feature columns loaded successfully.")
    except Exception as e:
        print(f"Error loading XGBoost model: {e}")

load_xgb_model()

def get_top_factors(feature_vector):
    """
    Generate explainability based on the model's feature importance.
    """
    factors = []
    
    feature_mapping = {
        'claim_amount': "Claim amount is anomalous",
        'graph_degree_centrality': "High network centrality detected",
        'graph_clustering_coeff': "Strong clustering in entities",
        'graph_pagerank': "High PageRank in network",
        'incident_type': "Suspicious incident type pattern",
        'incident_city': "High-risk location detected",
    }
    
    for i in range(10):
        feature_mapping[f'topic_{i}'] = f"Narrative pattern match: Topic {i+1}"
    
    try:
        if hasattr(xgb_model, 'feature_importances_') and xgb_model.feature_importances_ is not None:
            importances = xgb_model.feature_importances_
            col_names = list(feature_vector.columns)
            
            feature_imp = list(zip(col_names, importances))
            feature_imp.sort(key=lambda x: x[1], reverse=True)
            
            for fname, importance in feature_imp[:3]:
                if importance > 0:
                    title = fname.replace('_', ' ').title()
                    desc = feature_mapping.get(fname, f"Feature '{title}' influenced prediction.")
                    factors.append({
                        "title": title,
                        "description": desc
                    })
    except Exception as e:
        print(f"Warning: Feature importance extraction failed - {e}")
    
    if len(factors) < 3:
        fallback = [
            {"title": "Narrative Analysis", "description": "Claim contains anomalies"},
            {"title": "Amount Anomaly", "description": "Unusual claim amount"},
            {"title": "Network Pattern", "description": "Suspicious entity relationships"},
        ]
        while len(factors) < 3 and fallback:
            factors.append(fallback.pop(0))
    
    return factors[:3]

def predict_fraud(fused_vector):
    """
    Execute XGBoost prediction with explainability.
    """
    if xgb_model is None:
        raise RuntimeError("XGBoost model is not loaded.")

    try:
        if feature_columns:
            for col in feature_columns:
                if col not in fused_vector.columns:
                    fused_vector[col] = 0.0
            fused_vector = fused_vector[feature_columns]
        
        proba = xgb_model.predict_proba(fused_vector)[0]
        fraud_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        
        is_fraud = fraud_prob >= 0.5
        prediction_label = "Fraudulent Claim" if is_fraud else "Genuine Claim"
        
        if fraud_prob > 0.7:
            risk_level = "High"
        elif fraud_prob > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        confidence = abs(fraud_prob - 0.5) * 2
        factors = get_top_factors(fused_vector)

        return {
            "prediction": prediction_label,
            "fraud_probability": f"{fraud_prob * 100:.2f}%",
            "confidence_score": f"{confidence * 100:.2f}%",
            "risk_level": risk_level,
            "top_contributing_factors": factors
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        raise e
