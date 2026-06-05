import React from 'react';
import { AlignLeft, MessageSquare, FileText } from 'lucide-react';
import styles from './LDASection.module.css';

const LDASection = () => {
  return (
    <div className={`card ${styles.container}`}>
      <h2 className="section-title">Narrative Analysis (LDA)</h2>
      <p className="section-subtitle">Latent Dirichlet Allocation topic modeling on claim descriptions</p>

      <div className={styles.topicsGrid}>
        <div className={styles.topicCard}>
          <div className={styles.topicHeader}>
            <div className={styles.iconWrapper}>
              <FileText size={20} className={styles.icon} />
            </div>
            <h3 className={styles.topicTitle}>Topic A</h3>
          </div>
          <p className={styles.topicDesc}>
            Vehicle damage and repair patterns. High correlation with fabricated collision estimates.
          </p>
          <div className={styles.keywords}>
            <span>damage</span>
            <span>bumper</span>
            <span>repair</span>
            <span>mechanic</span>
          </div>
        </div>

        <div className={styles.topicCard}>
          <div className={styles.topicHeader}>
            <div className={styles.iconWrapper}>
              <MessageSquare size={20} className={styles.icon} />
            </div>
            <h3 className={styles.topicTitle}>Topic B</h3>
          </div>
          <p className={styles.topicDesc}>
            Claim amount and accident description patterns. Frequent inconsistencies detected in timelines.
          </p>
          <div className={styles.keywords}>
            <span>sudden</span>
            <span>amount</span>
            <span>pain</span>
            <span>hospital</span>
          </div>
        </div>

        <div className={styles.topicCard}>
          <div className={styles.topicHeader}>
            <div className={styles.iconWrapper}>
              <AlignLeft size={20} className={styles.icon} />
            </div>
            <h3 className={styles.topicTitle}>Topic C</h3>
          </div>
          <p className={styles.topicDesc}>
            Incident reporting and policy-related patterns. Matches profiles of recent policy inception fraud.
          </p>
          <div className={styles.keywords}>
            <span>policy</span>
            <span>police</span>
            <span>report</span>
            <span>witness</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LDASection;
