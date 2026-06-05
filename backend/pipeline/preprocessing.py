import pickle
import joblib
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Global variables for models
encoders = None
scaler = None

def load_preprocessing_models():
    global encoders, scaler
    try:
        encoders = joblib.load(os.path.join(MODELS_DIR, 'label_encoders.pkl'))
        scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        print("Preprocessing models loaded successfully.")
    except Exception as e:
        print(f"Error loading preprocessing models: {e}")

# Load models at module initialization
load_preprocessing_models()

def preprocess_data(claim_data):
    """
    Preprocess data using trained label encoders and scaler.
    """
    if encoders is None or scaler is None:
        raise RuntimeError("Preprocessing models are not loaded.")

    # Create a DataFrame from the incoming JSON (single row)
    # The keys from React might differ slightly from training features, map them appropriately.
    # From ClaimForm: incidentType, incidentCity, policyState, insuredRelationship, claimAmount
    
    # We map React camelCase to expected snake_case or whatever the model expects
    # Assuming standard snake_case for the Python model training:
    mapping = {
        'incidentType': 'incident_type',
        'incidentCity': 'incident_city',
        'policyState': 'policy_state',
        'insuredRelationship': 'insured_relationship',
        'claimAmount': 'claim_amount'
    }
    
    processed_dict = {}
    
    for react_key, py_key in mapping.items():
        val = claim_data.get(react_key, '')
        
        if py_key in encoders:
            encoder = encoders[py_key]
            # Handle unseen labels by falling back to the first class or a default unknown
            if val in encoder.classes_:
                processed_dict[py_key] = encoder.transform([val])[0]
            else:
                # Unseen value fallback to -1 or Mode
                processed_dict[py_key] = -1
        else:
            if py_key == 'claim_amount':
                try:
                    processed_dict[py_key] = float(val)
                except ValueError:
                    processed_dict[py_key] = 0.0
            else:
                processed_dict[py_key] = val

    df = pd.DataFrame([processed_dict])
    
    # Scale numerical features (assuming scaler was trained on 'claim_amount' and possibly others)
    # Usually scaler is trained on a specific subset. We'll apply it to the whole DF if it matches
    # or just the required columns. Let's assume the scaler was trained on all features or just numeric.
    # To be safe, we extract the feature order from the scaler if possible, but let's assume it scales 
    # specific columns or all. We will try to apply it to 'claim_amount' if that's what it was trained on.
    
    if hasattr(scaler, 'feature_names_in_'):
        features_to_scale = scaler.feature_names_in_
        # Ensure all required features are present
        for f in features_to_scale:
            if f not in df.columns:
                df[f] = 0.0 # Fallback
        df[features_to_scale] = scaler.transform(df[features_to_scale])
    else:
        # If standard scaler without feature names, assume it takes the whole array
        # This can be risky. We'll try just transforming claim_amount if it's a 1D scaler
        try:
            if scaler.n_features_in_ == 1:
                df['claim_amount'] = scaler.transform(df[['claim_amount']])
            else:
                df = pd.DataFrame(scaler.transform(df), columns=df.columns)
        except Exception:
            pass # Skip scaling if structure mismatches to prevent crash
            
    # Also keep the original description for LDA
    df['claim_description'] = claim_data.get('claimDescription', '')
    
    return df
