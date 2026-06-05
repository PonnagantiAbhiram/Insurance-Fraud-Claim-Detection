import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

feature_columns = None

def load_fusion_models():
    global feature_columns
    try:
        with open(os.path.join(MODELS_DIR, 'feature_columns.pkl'), 'rb') as f:
            feature_columns = pickle.load(f)
        print("Feature columns loaded successfully.")
    except Exception as e:
        print(f"Error loading feature columns: {e}")

load_fusion_models()

def fuse_features(processed_df, lda_features, graph_features):
    """
    Combines text, graph, and numerical/categorical features.
    Recreates the exact training feature structure.
    """
    if feature_columns is None:
        raise RuntimeError("Feature columns are not loaded.")

    # Convert lda and graph features to DataFrame
    lda_df = pd.DataFrame([lda_features])
    graph_df = pd.DataFrame([graph_features])
    
    # Concatenate all features
    fused_df = pd.concat([processed_df, lda_df, graph_df], axis=1)
    
    # Drop columns not needed (like original description)
    if 'claim_description' in fused_df.columns:
        fused_df = fused_df.drop('claim_description', axis=1)
        
    # Recreate the exact training feature structure
    final_features = {}
    for col in feature_columns:
        if col in fused_df.columns:
            final_features[col] = fused_df[col].iloc[0]
        else:
            final_features[col] = 0.0 # Handle missing columns safely
            
    final_df = pd.DataFrame([final_features])
    
    # Ensure column order matches training exactly
    final_df = final_df[feature_columns]
    
    return final_df
