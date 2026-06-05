import React from 'react';
import { FileInput, Database, FileText, Network, Combine, Cpu, ShieldAlert, ArrowRight } from 'lucide-react';
import styles from './ArchitectureSection.module.css';

const steps = [
  { name: "Input Claim", icon: FileInput },
  { name: "Preprocessing", icon: Database },
  { name: "LDA Analysis", icon: FileText },
  { name: "Graph Features", icon: Network },
  { name: "Feature Fusion", icon: Combine },
  { name: "XGBoost", icon: Cpu },
  { name: "Fraud Prediction", icon: ShieldAlert }
];

const ArchitectureSection = () => {
  return (
    <div className={`card ${styles.container}`}>
      <h2 className="section-title">System Architecture</h2>
      <p className="section-subtitle">End-to-end data processing pipeline</p>

      <div className={styles.workflowContainer}>
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <React.Fragment key={index}>
              <div className={styles.stepCard}>
                <div className={styles.iconWrapper}>
                  <Icon size={24} className={styles.icon} />
                </div>
                <span className={styles.stepName}>{step.name}</span>
              </div>
              
              {index < steps.length - 1 && (
                <div className={styles.arrowWrapper}>
                  <ArrowRight size={20} className={styles.arrow} />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default ArchitectureSection;
