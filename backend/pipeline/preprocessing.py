import joblib
import os
import pandas as pd

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
# All values verified against sklearn LabelEncoder alphabetical order.
#
# IMPORTANT: If a field IS collected by the form, its default here
# is irrelevant — the form value always overrides it. Defaults only
# apply to features the form never sends.
# ----------------------------------------------------------------
FIELD_DEFAULTS = {
    'months_as_customer':           200,
    'age':                          35,
    'policy_csl':                   1,        # LabelEncoder alpha order: "100/300"=0, "250/500"=1, "500/1000"=2
    'policy_deductable':            500,
    'policy_annual_premium':        1200.0,
    'umbrella_limit':               0,
    'insured_sex':                  0,        # FEMALE=0, MALE=1  (alphabetical)
    'insured_education_level':      2,        # Associate=0, College=1, High School=2, JD=3, MD=4, Masters=5, PhD=6
    'insured_occupation':           4,        # alphabetical — verify against training notebook
    'insured_hobbies':              8,        # alphabetical — verify against training notebook
    'capital-gains':                0,
    'capital-loss':                 0,
    # BUG #6 FIX: collision_type default aligned to same 0-based encoding used in ENCODINGS below.
    # When form field is empty, fuse_features will apply the FIELD_DEFAULT; when form sends a value,
    # the override block applies. Both now use the same 0-based scheme.
    'collision_type':               0,        # alphabetical: "Front Collision"=0, "Rear Collision"=1, "Side Collision"=2
    # BUG #2 FIX: incident_severity default corrected. 0 = "Major Damage" (alphabetical order).
    # Original default was 1 with a comment saying "Major Damage" — that was wrong; 1 = "Minor Damage".
    'incident_severity':            0,        # Major Damage=0, Minor Damage=1, Total Loss=2, Trivial Damage=3
    'authorities_contacted':        1,        # alphabetical — verify against training notebook
    # BUG #5 NOTE: incident_state is a separate column from policy_state.
    # "OH" in the full US-state LabelEncoder is NOT guaranteed to be 4.
    # Verify the exact integer from your training notebook's le.classes_ for incident_state.
    # Placeholder kept at 4 but marked for verification.
    'incident_state':               4,        # ⚠️  VERIFY: run list(le_incident_state.classes_).index("OH") in your notebook
    'incident_hour_of_the_day':     12,
    'number_of_vehicles_involved':  1,
    # BUG #3 FIX: property_damage default changed from 1 (YES) to 0 (NO).
    # YES is a fraud correlate — defaulting to YES silently pushed every unspecified claim toward fraud.
    'property_damage':              0,        # NO=0, YES=1
    'bodily_injuries':              1,
    'witnesses':                    1,
    # BUG #3 FIX: police_report_available default changed from 1 (YES) to 0 (NO).
    # Same reason as property_damage — YES is a fraud correlate.
    'police_report_available':      0,        # NO=0, YES=1
    'injury_claim':                 5000,
    'property_claim':               5000,
    'vehicle_claim':                5000,
    # BUG #4 FIX: total_claim_amount added to FIELD_DEFAULTS so it is always present
    # in the row dict before the scaler sees it. Without this, a missing claimAmount
    # produced a 0.0 raw value which after scaling became a large negative z-score
    # (anomalously low claim), biasing the model toward fraud.
    'total_claim_amount':           15000,    # median-ish default; sub-claims sum correctly when form provides amount
    'auto_make':                    5,        # verify against training notebook
    'auto_model':                   10,       # verify against training notebook
    'auto_year':                    2010,
}

# ----------------------------------------------------------------
# Categorical encodings — ALL must match sklearn LabelEncoder
# alphabetical order used during training exactly.
# ----------------------------------------------------------------
ENCODINGS = {
    'incident_type': {
        # Alphabetical: Multi-vehicle Collision < Parked Car < Single Vehicle Collision < Vehicle Theft
        'Multi-vehicle Collision':  0,
        'Parked Car':               1,
        'Single Vehicle Collision': 2,
        'Vehicle Theft':            3,
    },
    'incident_city': {
        # Alphabetical: Arlington < Columbus < Hillsdale < Northbend < Northbrook < Riverwood < Springfield
        'Arlington':   0,
        'Columbus':    1,
        'Hillsdale':   2,
        'Northbend':   3,
        'Northbrook':  4,
        'Riverwood':   5,
        'Springfield': 6,
    },
    'policy_state': {
        # Alphabetical: IL < IN < OH
        'IL': 0,
        'IN': 1,
        'OH': 2,
    },
    'insured_relationship': {
        # Alphabetical: husband < not-in-family < other-relative < own-child < unmarried < wife
        'husband':        0,
        'not-in-family':  1,
        'other-relative': 2,
        'own-child':      3,
        'unmarried':      4,
        'wife':           5,
    },
    # BUG #1 FIX: collision_type now starts at 0 (alphabetical).
    # Original code used 1/2/3 instead of 0/1/2 — every value was one category off,
    # and "Side Collision" mapped to 3 which is out-of-distribution for XGBoost.
    'collision_type': {
        # Alphabetical: Front Collision < Rear Collision < Side Collision
        'Front Collision': 0,
        'Rear Collision':  1,
        'Side Collision':  2,
    },
    'incident_severity': {
        # Alphabetical: Major Damage < Minor Damage < Total Loss < Trivial Damage
        'Major Damage':   0,
        'Minor Damage':   1,
        'Total Loss':     2,
        'Trivial Damage': 3,
    },
    'property_damage': {
        'NO':  0,
        'YES': 1,
    },
    'police_report_available': {
        'NO':  0,
        'YES': 1,
    },
}


def encode_field(field_name, raw_value, fallback=None):
    """
    Encode a categorical field using training-aligned LabelEncoder mappings.

    Args:
        field_name:  Key in ENCODINGS dict.
        raw_value:   String value from the form.
        fallback:    Value to use when raw_value is empty/unknown.
                     If None, uses 0. Pass the field's FIELD_DEFAULTS value
                     to get median-safe fallback for optional fields.
    Returns:
        Integer encoded value.
    """
    if not raw_value:
        # Empty string = field was not filled in; use the explicit fallback
        return fallback if fallback is not None else 0

    mapping = ENCODINGS.get(field_name, {})
    if raw_value in mapping:
        return mapping[raw_value]

    print(f"Warning: '{raw_value}' unseen for '{field_name}', using fallback={fallback}.")
    return fallback if fallback is not None else 0


def preprocess_data(claim_data):
    """
    Preprocess incoming React form data into the feature vector
    the scaler and XGBoost model expect.

    Pipeline:
      1. Start from FIELD_DEFAULTS (all keys present, safe median values).
      2. Override with form-supplied values (encoded where categorical).
      3. Compute total_claim_amount and sub-claims from form claimAmount.
      4. Attach claim_description (not scaled; consumed by LDA module).
      5. Scale numeric features via the loaded StandardScaler.
    """
    if scaler is None:
        raise RuntimeError("Scaler is not loaded. Check models/scaler.pkl path.")

    # --- 1. Start from safe defaults (all columns guaranteed present) ---
    row = dict(FIELD_DEFAULTS)

    # --- 2. Override with encoded form values ---
    # Required fields — form always sends these
    row['incident_type'] = encode_field(
        'incident_type', claim_data.get('incidentType', ''), fallback=0)
    row['incident_city'] = encode_field(
        'incident_city', claim_data.get('incidentCity', ''), fallback=0)
    row['policy_state'] = encode_field(
        'policy_state', claim_data.get('policyState', ''), fallback=0)
    row['insured_relationship'] = encode_field(
        'insured_relationship', claim_data.get('insuredRelationship', ''), fallback=0)

    # Optional fields — use FIELD_DEFAULTS value as fallback (not 0) so
    # missing values stay at the neutral median rather than a possibly
    # high-fraud-signal extreme.

    # BUG #1 FIX: collision_type now uses 0-based alphabetical encoding via ENCODINGS dict.
    # BUG #6 FIX: fallback uses FIELD_DEFAULTS['collision_type'] (0 = Front Collision),
    #             so default path and override path are now consistent.
    raw_collision = claim_data.get('collisionType', '')
    row['collision_type'] = encode_field(
        'collision_type', raw_collision, fallback=FIELD_DEFAULTS['collision_type'])

    # BUG #2 FIX: incident_severity fallback is now FIELD_DEFAULTS['incident_severity'] = 0 (Major Damage).
    raw_severity = claim_data.get('incidentSeverity', '')
    row['incident_severity'] = encode_field(
        'incident_severity', raw_severity, fallback=FIELD_DEFAULTS['incident_severity'])

    # BUG #3 FIX: property_damage fallback changed to 0 (NO) — not 1 (YES).
    # YES is a fraud signal; defaulting to YES when not provided biased every claim.
    raw_prop_damage = claim_data.get('propertyDamage', '')
    row['property_damage'] = encode_field(
        'property_damage', raw_prop_damage, fallback=FIELD_DEFAULTS['property_damage'])

    # BUG #3 FIX: police_report_available fallback changed to 0 (NO) — not 1 (YES).
    raw_police = claim_data.get('policeReportAvailable', '')
    row['police_report_available'] = encode_field(
        'police_report_available', raw_police, fallback=FIELD_DEFAULTS['police_report_available'])

    # witnesses — numeric, optional
    try:
        witnesses_val = claim_data.get('witnesses', '')
        row['witnesses'] = int(witnesses_val) if witnesses_val != '' else FIELD_DEFAULTS['witnesses']
    except (ValueError, TypeError):
        row['witnesses'] = FIELD_DEFAULTS['witnesses']

    # --- 3. Claim amount + sub-claims ---
    # BUG #4 FIX: total_claim_amount is now guaranteed in FIELD_DEFAULTS above.
    # When the form provides a value we overwrite correctly; when it doesn't,
    # the default (15000) is used and sub-claims stay at their own defaults (5000 each).
    raw_amount = claim_data.get('claimAmount', '')
    if raw_amount != '' and raw_amount is not None:
        try:
            amount = float(raw_amount)
        except (ValueError, TypeError):
            amount = float(FIELD_DEFAULTS['total_claim_amount'])
    else:
        amount = float(FIELD_DEFAULTS['total_claim_amount'])

    row['total_claim_amount'] = amount
    # Sub-claims derived consistently from the same amount
    row['injury_claim']   = round(amount * 0.33, 2)
    row['property_claim'] = round(amount * 0.33, 2)
    row['vehicle_claim']  = round(amount * 0.34, 2)

    # --- 4. Attach claim_description for the LDA module (not scaled) ---
    df = pd.DataFrame([row])
    df['claim_description'] = claim_data.get('claimDescription', '')

    # --- 5. Scale numeric features using the fitted StandardScaler ---
    scaler_cols = list(scaler.feature_names_in_)   # exact order from training

    # Verify all expected columns are present before scaling
    missing_cols = [c for c in scaler_cols if c not in df.columns]
    if missing_cols:
        raise RuntimeError(
            f"Scaler expects columns missing from feature dict: {missing_cols}. "
            f"Check FIELD_DEFAULTS and form field mappings."
        )

    # BUG #7 FIX: scaling failure now raises an exception instead of silently
    # continuing with raw unscaled values (which would be wildly out-of-distribution).
    try:
        df[scaler_cols] = scaler.transform(df[scaler_cols])
    except Exception as e:
        raise RuntimeError(
            f"Scaling failed: {e}. "
            f"This likely means a column dtype is wrong or a new unseen value was introduced."
        ) from e

    print("\n=========== PREPROCESSED FEATURES ===========")
    print(df[[c for c in scaler_cols if c in df.columns]].T)
    print("=============================================")
    return df