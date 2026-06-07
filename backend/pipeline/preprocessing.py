import joblib
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

scaler = None

def load_preprocessing_models():
    global scaler
    try:
        scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        print("Preprocessing models loaded successfully.")
    except Exception as e:
        print(f"Error loading preprocessing models: {e}")

load_preprocessing_models()

# ----------------------------------------------------------------
# Median/default values for fields the form does NOT collect.
# These are dataset-typical values that won't skew the prediction.
# ----------------------------------------------------------------
FIELD_DEFAULTS = {
    'months_as_customer':       200,
    'age':                      35,
    'policy_csl':               1,      # encoded: "250/500"
    'policy_deductable':        500,
    'policy_annual_premium':    1200.0,
    'umbrella_limit':           0,
    'insured_sex':              0,      # encoded: MALE=0 / FEMALE=1
    'insured_education_level':  2,      # encoded: "MD"
    'insured_occupation':       4,      # encoded: "craft-repair"
    'insured_hobbies':          8,      # encoded: "reading"
    'capital-gains':            0,
    'capital-loss':             0,
    'collision_type':           0,      # encoded: "Front Collision"
    'incident_severity':        1,      # encoded: "Major Damage"
    'authorities_contacted':    1,      # encoded: "Police"
    'incident_state':           4,      # encoded: "OH"
    'incident_hour_of_the_day': 12,
    'number_of_vehicles_involved': 1,
    'property_damage':          1,      # encoded: "YES"
    'bodily_injuries':          1,
    'witnesses':                1,
    'police_report_available':  1,      # encoded: "YES"
    'injury_claim':             5000,
    'property_claim':           5000,
    'vehicle_claim':            5000,
    'auto_make':                5,      # encoded: "Honda"
    'auto_model':               10,     # encoded: "Civic"
    'auto_year':                2010,
}

# Simple lookup tables matching the notebook's LabelEncoder order
ENCODINGS = {
    'incident_type': {
        'Multi-vehicle Collision': 0,
        'Parked Car':              1,
        'Single Vehicle Collision':2,
        'Vehicle Theft':           3,
    },
    'incident_city': {
        # Cities present in the training dataset
        'Columbus':    0, 'Northbend': 1, 'Riverwood':  2,
        'Springfield': 3, 'Hillsdale': 4, 'Arlington':  5,
        'Avondale':    6, 'Hartfield': 7, 'Oakridge':   8,
        'Shelby':      9,
    },
    'policy_state': {
        'IL': 0, 'IN': 1, 'NY': 2, 'OH': 3, 'CA': 4,
    },
    'insured_relationship': {
        'husband':       0,
        'not-in-family': 1,
        'other-relative':2,
        'own-child':     3,
        'unmarried':     4,
        'wife':          5,
    },
}

def encode_field(field_name, raw_value):
    """Encode a categorical field. Falls back to 0 for unseen values."""
    mapping = ENCODINGS.get(field_name, {})
    if raw_value in mapping:
        return mapping[raw_value]
    print(f"Warning: '{raw_value}' unseen for '{field_name}', defaulting to 0.")
    return 0


def preprocess_data(claim_data):
    """
    Preprocess incoming React form data into the 33-feature vector
    the scaler and XGBoost model expect.
    """
    if scaler is None:
        raise RuntimeError("Scaler is not loaded.")

    # --- Build the full feature dict starting from defaults ---
    row = dict(FIELD_DEFAULTS)

    # --- Fill in form-supplied fields (encoded) ---
    row['incident_type']        = encode_field('incident_type',        claim_data.get('incidentType', ''))
    row['incident_city']        = encode_field('incident_city',        claim_data.get('incidentCity', ''))
    row['policy_state']         = encode_field('policy_state',         claim_data.get('policyState', ''))
    row['insured_relationship'] = encode_field('insured_relationship',  claim_data.get('insuredRelationship', ''))

    # total_claim_amount comes from the form
    try:
        amount = float(claim_data.get('claimAmount', 0))
    except (ValueError, TypeError):
        amount = 0.0
    row['total_claim_amount'] = amount
    # Split amount sensibly across sub-claims
    row['injury_claim']    = round(amount * 0.33, 2)
    row['property_claim']  = round(amount * 0.33, 2)
    row['vehicle_claim']   = round(amount * 0.34, 2)

    # Keep claim_description for LDA (not scaled)
    df = pd.DataFrame([row])
    df['claim_description'] = claim_data.get('claimDescription', '')

    # --- Scale the 33 numeric features the scaler was trained on ---
    scaler_cols = list(scaler.feature_names_in_)   # exact order from training
    try:
        df[scaler_cols] = scaler.transform(df[scaler_cols])
    except Exception as e:
        print(f"Warning: Scaling failed - {e}. Continuing with raw values.")

    return df