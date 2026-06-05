import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Database } from 'lucide-react';
import styles from './MetricsSection.module.css';

const metrics = [
  { metric: "Accuracy", value: "99.67%", description: "Overall model correctness" },
  { metric: "Precision", value: "100.00%", description: "Exactness of fraud predictions" },
  { metric: "Recall", value: "98.65%", description: "Completeness of fraud detection" },
  { metric: "F1 Score", value: "99.32%", description: "Harmonic mean of precision & recall" },
  { metric: "ROC-AUC", value: "99.46%", description: "Area under the ROC curve" }
];

const MetricsSection = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={`card ${styles.container}`}>
      <div 
        className={styles.header} 
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className={styles.titleGroup}>
          <Database size={20} className={styles.icon} />
          <h2 className={styles.title}>Technical Model Metrics</h2>
        </div>
        <button className={styles.toggleBtn}>
          {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      {isOpen && (
        <div className={styles.content}>
          <table className={styles.metricsTable}>
            <thead>
              <tr>
                <th>Evaluation Metric</th>
                <th>Score</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((item, index) => (
                <tr key={index}>
                  <td className={styles.metricName}>{item.metric}</td>
                  <td className={styles.metricValue}>{item.value}</td>
                  <td className={styles.metricDesc}>{item.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default MetricsSection;
