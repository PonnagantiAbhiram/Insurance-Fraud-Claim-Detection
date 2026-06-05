import React from 'react';
import styles from './Footer.module.css';

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.footerContainer}`}>
        <div className={styles.footerInfo}>
          <h3 className={styles.projectName}>Insurance Fraud Detection System</h3>
          <p className={styles.projectType}>Academic Mini Project</p>
        </div>
        <div className={styles.footerTech}>
          <p>Technologies Used:</p>
          <div className={styles.techTags}>
            <span>React.js</span>
            <span>NetworkX (Mock)</span>
            <span>XGBoost (Mock)</span>
            <span>Flask (Pending)</span>
          </div>
        </div>
      </div>
      <div className={styles.copyright}>
        <p>&copy; {new Date().getFullYear()} Insurance Fraud Detection Project. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
