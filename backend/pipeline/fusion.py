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
        print(f"Feature columns loaded successfully. Total: {len(feature_columns)} columns.")
    except Exception as e:
        print(f"Error loading feature columns: {e}")


load_fusion_models()


def fuse_features(processed_df, lda_features, graph_features):
    """
    Combines preprocessed tabular features, LDA topic features, and
    graph-based features into the exact training feature structure.

    Args:
        processed_df:   DataFrame returned by preprocess_data().
                        Contains scaled tabular features + 'claim_description'.
        lda_features:   Dict of {topic_0: float, topic_1: float, ...}
        graph_features: Dict of {graph_degree_centrality: float,
                                  graph_clustering_coeff: float,
                                  graph_pagerank: float}

    Returns:
        DataFrame with exactly the columns in feature_columns.pkl,
        in the exact order XGBoost was trained on.
    """
    if feature_columns is None:
        raise RuntimeError(
            "Feature columns are not loaded. Check models/feature_columns.pkl path."
        )

    # --- Validate inputs ---
    if not isinstance(lda_features, dict) or not lda_features:
        raise ValueError(
            f"lda_features must be a non-empty dict. Got: {type(lda_features)}"
        )
    if not isinstance(graph_features, dict) or not graph_features:
        raise ValueError(
            f"graph_features must be a non-empty dict. Got: {type(graph_features)}"
        )

    # --- Convert auxiliary feature dicts to single-row DataFrames ---
    lda_df   = pd.DataFrame([lda_features])
    graph_df = pd.DataFrame([graph_features])

    # --- Concatenate all feature blocks side by side ---
    # Reset indices to ensure correct axis=1 alignment
    processed_df = processed_df.reset_index(drop=True)
    lda_df       = lda_df.reset_index(drop=True)
    graph_df     = graph_df.reset_index(drop=True)

    fused_df = pd.concat([processed_df, lda_df, graph_df], axis=1)

    # --- Drop the raw text column (consumed by LDA; not a model feature) ---
    if 'claim_description' in fused_df.columns:
        fused_df = fused_df.drop('claim_description', axis=1)

    # --- Reconstruct the exact training feature structure ---
    # Any column in feature_columns that is missing gets filled with 0.0.
    # Any extra column in fused_df that is not in feature_columns is discarded.
    final_features = {}
    missing_in_fused = []
    for col in feature_columns:
        if col in fused_df.columns:
            final_features[col] = fused_df[col].iloc[0]
        else:
            final_features[col] = 0.0
            missing_in_fused.append(col)

    if missing_in_fused:
        print(
            f"Warning: {len(missing_in_fused)} feature(s) expected by the model were not "
            f"found in the fused DataFrame and were filled with 0.0: {missing_in_fused}"
        )

    final_df = pd.DataFrame([final_features])

    # --- Enforce exact column order matching training ---
    final_df = final_df[feature_columns]

    print("\n=========== FINAL FUSED FEATURES ===========")
    print(final_df.T.to_string())
    print(f"Total features: {len(final_df.columns)}")
    print("=============================================")
    return final_df