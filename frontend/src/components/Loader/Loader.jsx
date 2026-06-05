import React from 'react';
import { Loader2, CheckCircle2, Circle } from 'lucide-react';
import styles from './Loader.module.css';

const steps = [
  "Data Preprocessing",
  "Narrative Analysis (LDA)",
  "Graph Feature Extraction",
  "Feature Fusion",
  "XGBoost Classification",
  "Generating Prediction"
];

const Loader = ({ currentStep }) => {
  return (
    <div className={`card ${styles.loaderCard}`}>
      <div className={styles.loaderHeader}>
        <Loader2 className={styles.spinner} size={32} />
        <h2 className={styles.title}>Processing Claim Data</h2>
        <p className="text-secondary">Running multi-modal fraud detection models</p>
      </div>

      <div className={styles.stepsContainer}>
        {steps.map((step, index) => {
          const isCompleted = currentStep > index;
          const isCurrent = currentStep === index;
          const isPending = currentStep < index;

          return (
            <div 
              key={index} 
              className={`${styles.stepItem} ${
                isCompleted ? styles.completed : isCurrent ? styles.current : styles.pending
              }`}
            >
              <div className={styles.stepIcon}>
                {isCompleted ? (
                  <CheckCircle2 size={20} className={styles.completedIcon} />
                ) : isCurrent ? (
                  <Loader2 size={20} className={styles.currentIcon} />
                ) : (
                  <Circle size={20} className={styles.pendingIcon} />
                )}
              </div>
              <span className={styles.stepText}>{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Loader;
