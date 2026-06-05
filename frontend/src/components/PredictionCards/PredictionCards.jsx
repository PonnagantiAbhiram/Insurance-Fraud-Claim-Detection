import React from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  BarChart3
} from 'lucide-react';

import styles from './PredictionCards.module.css';

const PredictionCards = ({ data }) => {
  if (!data) return null;

  console.log("Prediction Data:", data);

  // Backend sends snake_case
  const prediction =
    data.prediction || "Unknown";

  const fraudProbability =
    data.fraud_probability || "0%";

  const riskLevel =
    data.risk_level || "Low";

  const confidenceScore =
    data.confidence_score || "0%";

  const isFraud =
    prediction === "Fraudulent Claim" ||
    prediction === "Fraudulent";

  const getRiskColor = (risk) => {
    if (!risk) return "var(--text-secondary)";

    switch (String(risk).toLowerCase()) {
      case "high":
        return "var(--fraud-alert)";

      case "medium":
        return "var(--warning)";

      case "low":
        return "var(--success)";

      default:
        return "var(--text-secondary)";
    }
  };

  return (
    <div className={styles.grid}>

      {/* Prediction Card */}
      <div
        className={`card ${styles.resultCard} ${isFraud
            ? styles.dangerBorder
            : styles.successBorder
          }`}
      >
        <div className={styles.cardHeader}>
          <h3 className={styles.cardTitle}>
            Prediction
          </h3>

          {isFraud ? (
            <ShieldAlert
              className={styles.iconDanger}
              size={24}
            />
          ) : (
            <CheckCircle2
              className={styles.iconSuccess}
              size={24}
            />
          )}
        </div>

        <div
          className={styles.cardValue}
          style={{
            color: isFraud
              ? "var(--fraud-alert)"
              : "var(--success)"
          }}
        >
          {prediction}
        </div>

        <p className="text-secondary">
          AI Model Classification
        </p>
      </div>

      {/* Fraud Probability */}
      <div className="card">
        <div className={styles.cardHeader}>
          <h3 className={styles.cardTitle}>
            Fraud Probability
          </h3>

          <BarChart3
            className={styles.iconNeutral}
            size={24}
          />
        </div>

        <div className={styles.cardValue}>
          {fraudProbability}
        </div>

        <div className={styles.progressBarBg}>
          <div
            className={styles.progressBarFill}
            style={{
              width:
                typeof fraudProbability === "string"
                  ? fraudProbability
                  : `${fraudProbability}%`,

              backgroundColor: isFraud
                ? "var(--fraud-alert)"
                : "var(--success)"
            }}
          />
        </div>
      </div>

      {/* Risk Level */}
      <div className="card">
        <div className={styles.cardHeader}>
          <h3 className={styles.cardTitle}>
            Risk Level
          </h3>

          <AlertTriangle
            className={styles.iconRisk}
            size={24}
            style={{
              color: getRiskColor(riskLevel)
            }}
          />
        </div>

        <div
          className={styles.cardValue}
          style={{
            color: getRiskColor(riskLevel)
          }}
        >
          {riskLevel} Risk
        </div>

        <p className="text-secondary">
          Based on historical patterns
        </p>
      </div>

      {/* Confidence */}
      <div className="card">
        <div className={styles.cardHeader}>
          <h3 className={styles.cardTitle}>
            Confidence Score
          </h3>

          <CheckCircle2
            className={styles.iconNeutral}
            size={24}
          />
        </div>

        <div className={styles.cardValue}>
          {confidenceScore}
        </div>

        <p className="text-secondary">
          Model certainty metric
        </p>
      </div>

    </div>
  );
};

export default PredictionCards;