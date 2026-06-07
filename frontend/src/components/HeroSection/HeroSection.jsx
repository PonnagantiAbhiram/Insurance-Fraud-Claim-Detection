import React from 'react';
import { Activity, ShieldCheck, CheckCircle2, AlertTriangle } from 'lucide-react';
import styles from './HeroSection.module.css';

const StatCard = ({ title, value, icon: Icon, color }) => (
  <div className={styles.statCard}>
    <div className={styles.statIcon} style={{ color }}>
      <Icon size={24} />
    </div>
    <div className={styles.statInfo}>
      <p className={styles.statTitle}>{title}</p>
      <h3 className={styles.statValue}>{value}</h3>
    </div>
  </div>
);

const HeroSection = () => {
  return (
    <section className={styles.heroSection}>
      <div className={`container ${styles.heroContainer}`}>
        <div className={styles.heroContent}>
          <h1 className={styles.title}>Insurance Fraud Detection System</h1>
          <p className={styles.subtitle}>
            AI-powered fraud detection using Narrative Analysis, Relationship Analysis, and XGBoost Classification
          </p>
        </div>
        
        <div className={styles.statsGrid}>
          <StatCard title="Accuracy" value="98.33%" icon={CheckCircle2} color="var(--success)" />
          <StatCard title="Precision" value="94.81%" icon={ShieldCheck} color="var(--primary-action)" />
          <StatCard title="Recall" value="98.65%" icon={AlertTriangle} color="var(--warning)" />
          <StatCard title="ROC-AUC" value="99.91%" icon={Activity} color="#8B5CF6" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
