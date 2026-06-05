import React from 'react';
import { Lightbulb, TrendingUp, AlertOctagon, Link2, FileWarning } from 'lucide-react';
import styles from './ContributingFactors.module.css';

const factors = [
  {
    id: 1,
    title: "Unusual narrative pattern",
    description: "The claim description contains anomalies commonly associated with fabricated events.",
    icon: FileWarning,
    color: "var(--fraud-alert)"
  },
  {
    id: 2,
    title: "Elevated claim amount",
    description: "The requested amount is significantly higher than historical averages for this incident type.",
    icon: TrendingUp,
    color: "var(--warning)"
  },
  {
    id: 3,
    title: "Strong relationship connections",
    description: "Network analysis reveals suspicious links between the insured and involved parties.",
    icon: Link2,
    color: "var(--fraud-alert)"
  },
  {
    id: 4,
    title: "High-risk claim characteristics",
    description: "Combination of incident city and policy state flags a known high-risk geographical pattern.",
    icon: AlertOctagon,
    color: "var(--warning)"
  },
  {
    id: 5,
    title: "Similarity with previous patterns",
    description: "High cosine similarity with previously confirmed fraudulent claims in the database.",
    icon: Lightbulb,
    color: "var(--primary-action)"
  }
];

const ContributingFactors = () => {
  return (
    <div className={`card ${styles.container}`}>
      <h2 className="section-title">Top Contributing Factors</h2>
      <p className="section-subtitle">Key variables influencing the model's prediction</p>

      <div className={styles.factorsList}>
        {factors.map((factor) => {
          const Icon = factor.icon;
          return (
            <div key={factor.id} className={styles.factorItem}>
              <div className={styles.iconWrapper} style={{ backgroundColor: `${factor.color}15` }}>
                <Icon size={20} style={{ color: factor.color }} />
              </div>
              <div className={styles.factorContent}>
                <h4 className={styles.factorTitle}>{factor.title}</h4>
                <p className={styles.factorDescription}>{factor.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ContributingFactors;
