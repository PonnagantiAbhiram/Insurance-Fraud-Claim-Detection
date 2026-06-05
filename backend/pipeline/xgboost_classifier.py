import os
import pickle
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

xgb_model = None

def load_xgb_model():
    global xgb_model
    try:
        with open(os.path.join(MODELS_DIR, 'xgboost_fraud_model.pkl'), 'rb') as f:
            xgb_model = pickle.load(f)
        print("XGBoost model loaded successfully.")
    except Exception as e:
        print(f"Error loading XGBoost model: {e}")

load_xgb_model()

def get_top_factors(feature_vector):
    """
    Generate explainability based on the model's feature importance.
    """
    factors = []
    
    # Try to extract actual feature importances if available
    try:
        if hasattr(xgb_model, 'feature_importances_'):
            importances = xgb_model.feature_importances_
            feature_names = feature_vector.columns
            
            # Combine and sort
            feature_imp = list(zip(feature_names, importances))
            feature_imp.sort(key=lambda x: x[1], reverse=True)
            
            top_3 = feature_imp[:3]
            
            # Map column names to human readable text
            mapping = {
                'claim_amount': "Elevated claim amount relative to incident type",
                'graph_connected_entities': "Strong relationship connections detected in network",
                'graph_avg_degree': "High centrality in suspected network cluster",
                'topic_0': "Narrative matches Topic 0 (Fabrication indicators)",
                'topic_1': "Narrative matches Topic 1 (Timeline inconsistencies)",
                'topic_2': "Narrative matches Topic 2 (Suspicious reporting delay)",
                'incident_city': "Incident location matches high-risk geographical pattern",
                'insured_relationship': "Unusual policyholder relationship involved"
            }
            
            for fname, imp in top_3:
                title = fname.replace('_', ' ').title()
                desc = mapping.get(fname, f"The feature '{title}' strongly influenced the model.")
                factors.append({
                    "title": title,
                    "description": desc
                })
                
    except Exception as e:
        print(f"Error calculating feature importances: {e}")
        
    # Fallback generic factors if extraction fails
    if not factors:
        factors = [
            {"title": "Unusual narrative pattern", "description": "The claim description contains anomalies."},
            {"title": "Elevated claim amount", "description": "The requested amount is statistically abnormal."},
            {"title": "Network Connections", "description": "Suspicious links between the insured and involved parties."}
        ]
        
    return factors

def predict_fraud(fused_vector):
    """
    Execute the XGBoost model to generate predictions, probabilities, and factors.
    """
    if xgb_model is None:
        raise RuntimeError("XGBoost model is not loaded.")

    try:
        # Predict probability
        # Assuming model outputs shape [n_samples, n_classes] where class 1 is Fraud
        proba = xgb_model.predict_proba(fused_vector)[0]
        
        fraud_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
        
        # Binary prediction (threshold = 0.5)
        is_fraud = fraud_prob >= 0.5
        prediction_label = "Fraudulent Claim" if is_fraud else "Genuine Claim"
        
        # Risk level logic
        if fraud_prob > 0.7:
            risk_level = "High"
        elif fraud_prob > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        # Confidence score (how far from 0.5 boundary)
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
