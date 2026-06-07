from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import traceback
import numpy as np

# Import pipeline modules
from pipeline.preprocessing import preprocess_data
from pipeline.lda_analysis import run_lda
from pipeline.graph_features import extract_graph_features
from pipeline.fusion import fuse_features
from pipeline.xgboost_classifier import predict_fraud

app = Flask(__name__)
CORS(app)


# ---------------------------------------------------
# Convert NumPy types to Python native types
# ---------------------------------------------------
def convert_numpy(obj):
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)

    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [convert_numpy(v) for v in obj]

    return obj


@app.route('/api/analyze', methods=['POST'])
def analyze_claim():
    try:
        claim_data = request.json

        if not claim_data:
            return jsonify({
                "error": "No claim data provided"
            }), 400

        print("\n" + "=" * 60)
        print("STARTING FRAUD ANALYSIS PIPELINE")
        print("=" * 60)

        # ---------------------------------------------------
        # STEP 1 - PREPROCESSING
        # ---------------------------------------------------
        print("STEP 1: Preprocessing...")
        processed_data = preprocess_data(claim_data)

        # ---------------------------------------------------
        # STEP 2 - LDA ANALYSIS
        # ---------------------------------------------------
        print("STEP 2: LDA Analysis...")
        lda_features, lda_frontend_data = run_lda(processed_data)

        # ---------------------------------------------------
        # STEP 3 - GRAPH FEATURES
        # ---------------------------------------------------
        print("STEP 3: Graph Feature Extraction...")
        graph_features, graph_frontend_data = extract_graph_features(
            claim_data
        )

        # ---------------------------------------------------
        # STEP 4 - FEATURE FUSION
        # ---------------------------------------------------
        print("STEP 4: Feature Fusion...")
        fused_vector = fuse_features(
            processed_data,
            lda_features,
            graph_features
        )

        # ---------------------------------------------------
        # STEP 5 - MODEL PREDICTION
        # ---------------------------------------------------
        print("STEP 5: XGBoost Prediction...")
        prediction_results = predict_fraud(
            fused_vector
        )

        # Optional animation delay
        time.sleep(2)

        # ---------------------------------------------------
        # RESPONSE
        # ---------------------------------------------------
        response = {
            "prediction":
                prediction_results["prediction"],

            "fraud_probability":
                prediction_results["fraud_probability"],

            "confidence_score":
                prediction_results["confidence_score"],

            "risk_level":
                prediction_results["risk_level"],

            "top_contributing_factors":
                prediction_results["top_contributing_factors"],

            "lda_analysis":
                lda_frontend_data,

            "graph_analysis":
                graph_frontend_data
        }

        # Convert all NumPy values
        response = convert_numpy(response)

        print("=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

        return jsonify(response), 200

    except Exception as e:
        print("\nERROR IN PIPELINE")
        print(str(e))
        traceback.print_exc()

        # Check if this is a model loading error
        error_msg = str(e)
        if "is not loaded" in error_msg or "No such file or directory" in error_msg:
            return jsonify({
                "error": "ML models are not loaded. Please run the Insurance_model_fixed.ipynb notebook to generate the required model files.",
                "details": error_msg
            }), 503  # Service Unavailable
        
        return jsonify({
            "error": "An error occurred during fraud analysis. Please check the claim data and try again.",
            "details": error_msg
        }), 500


if __name__ == '__main__':
    app.run(
        debug=False,
        port=5000
    )