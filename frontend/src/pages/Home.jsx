import React, { useState, useEffect, useRef } from 'react';
import HeroSection from '../components/HeroSection/HeroSection';
import ClaimForm from '../components/ClaimForm/ClaimForm';
import Loader from '../components/Loader/Loader';
import PredictionCards from '../components/PredictionCards/PredictionCards';
import ContributingFactors from '../components/ContributingFactors/ContributingFactors';
import LDASection from '../components/LDASection/LDASection';
import GraphSection from '../components/GraphSection/GraphSection';
import MetricsSection from '../components/MetricsSection/MetricsSection';
import ArchitectureSection from '../components/ArchitectureSection/ArchitectureSection';
import { analyzeClaim } from '../services/api';
import styles from './Home.module.css';

const Home = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState(null);

  const dashboardRef = useRef(null);
  const loaderRef = useRef(null);

  const handleClaimSubmit = async (formData) => {
    setIsProcessing(true);
    setCurrentStep(0);
    setPredictionResult(null);
    setError(null);

    // Scroll to loader
    setTimeout(() => {
      loaderRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);

    // Start API call in background
    const apiPromise = analyzeClaim(formData);

    // Manage sequential loader steps
    for (let i = 0; i <= 6; i++) {
      setCurrentStep(i);
      // Wait for 1 second per step to simulate complex processing visually
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Wait for API to resolve (it should be done by now, but just in case)
    try {
      const result = await apiPromise;
      setPredictionResult(result);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing the claim. Please ensure the Flask backend is running on port 5000 and models are properly loaded.');
    } finally {
      setIsProcessing(false);
    }

    // Scroll to results
    setTimeout(() => {
      if (predictionResult || error) {
        dashboardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  };

  return (
    <div className={styles.homeContainer}>
      <HeroSection />

      <div className="container">
        {!isProcessing && !predictionResult && !error && (
          <div className={styles.sectionMargin}>
            <ClaimForm onSubmit={handleClaimSubmit} isLoading={isProcessing} />
          </div>
        )}

        {isProcessing && (
          <div className={styles.sectionMargin} ref={loaderRef}>
            <Loader currentStep={currentStep} />
          </div>
        )}

        {error && !isProcessing && (
          <div ref={dashboardRef} className={styles.sectionMargin}>
            <div className="card" style={{ borderLeft: '4px solid #dc2626', backgroundColor: '#fee2e2' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                <div style={{ fontSize: '1.5rem' }}>⚠️</div>
                <h3 style={{ margin: 0, color: '#7f1d1d' }}>Analysis Failed</h3>
              </div>
              <p style={{ color: '#7f1d1d', marginBottom: '1.5rem' }}>{error}</p>
              <button
                className="btn-primary"
                onClick={() => {
                  setError(null);
                  setPredictionResult(null);
                }}
              >
                Try Again
              </button>
            </div>
          </div>
        )}

        {predictionResult && !isProcessing && (
          <div ref={dashboardRef} className={styles.dashboardSection}>
            <div className={styles.resultsHeader}>
              <h2 className="section-title" style={{ fontSize: '2rem' }}>Analysis Results</h2>
              <p className="text-secondary">Comprehensive fraud detection report for the submitted claim</p>

              <button
                className="btn-primary"
                style={{ marginTop: '1.5rem' }}
                onClick={() => setPredictionResult(null)}
              >
                Analyze Another Claim
              </button>
            </div>

            <PredictionCards data={predictionResult} />

            <ContributingFactors
              factors={predictionResult.top_contributing_factors}
            />

            <LDASection
              data={predictionResult.lda_analysis}
            />

            <GraphSection
              data={predictionResult.graph_analysis}
            />

            <MetricsSection />
          </div>
        )}

        <div className={styles.sectionMargin} id="about">
          <ArchitectureSection />
        </div>
      </div>
    </div>
  );
};

export default Home;
