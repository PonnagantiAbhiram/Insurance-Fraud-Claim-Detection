import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';
import styles from './Navbar.module.css';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={`container ${styles.navContainer}`}>
        <Link to="/" className={styles.logo}>
          <ShieldCheck size={28} className={styles.logoIcon} />
          <span className={styles.logoText}>Insurance Fraud Detection System</span>
        </Link>
        <div className={styles.navLinks}>
          <Link to="/" className={styles.navLink}>Home</Link>
          <a href="#analyze" className={styles.navLink}>Analyze Claim</a>
          <a href="#about" className={styles.navLink}>About Project</a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
