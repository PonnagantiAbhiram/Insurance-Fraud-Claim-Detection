import React, { useState } from 'react';
import { FileText, Send, AlertCircle } from 'lucide-react';
import styles from './ClaimForm.module.css';

// Technical Parameters - Insurance Claim Constraints
const TECHNICAL_PARAMS = {
  CLAIM_AMOUNT_MIN: 100,
  CLAIM_AMOUNT_MAX: 1000000,
  DESCRIPTION_MIN_LENGTH: 20,
  DESCRIPTION_MAX_LENGTH: 5000,
  CITY_MAX_LENGTH: 50,
  INCIDENT_TYPES: ['Multi-vehicle Collision', 'Single Vehicle Collision', 'Vehicle Theft', 'Parked Car'],
  POLICY_STATES: ['OH', 'IL', 'IN', 'NY', 'CA'],
  INSURED_RELATIONSHIPS: ['own-child', 'other-relative', 'not-in-family', 'husband', 'wife', 'unmarried']
};

const ClaimForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    incidentType: '',
    incidentCity: '',
    policyState: '',
    insuredRelationship: '',
    claimAmount: '',
    claimDescription: ''
  });

  const [validationErrors, setValidationErrors] = useState({});

  const validateForm = () => {
    const errors = {};

    if (!formData.incidentType) {
      errors.incidentType = 'Incident type is required';
    }

    if (!formData.incidentCity || formData.incidentCity.trim().length === 0) {
      errors.incidentCity = 'City is required';
    } else if (formData.incidentCity.length > TECHNICAL_PARAMS.CITY_MAX_LENGTH) {
      errors.incidentCity = `City must be less than ${TECHNICAL_PARAMS.CITY_MAX_LENGTH} characters`;
    }

    if (!formData.policyState) {
      errors.policyState = 'State is required';
    }

    if (!formData.insuredRelationship) {
      errors.insuredRelationship = 'Relationship is required';
    }

    if (!formData.claimAmount) {
      errors.claimAmount = 'Claim amount is required';
    } else if (isNaN(parseFloat(formData.claimAmount))) {
      errors.claimAmount = 'Claim amount must be a valid number';
    } else if (parseFloat(formData.claimAmount) < TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN) {
      errors.claimAmount = `Minimum claim amount is $${TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN}`;
    } else if (parseFloat(formData.claimAmount) > TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX) {
      errors.claimAmount = `Maximum claim amount is $${TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX}`;
    }

    if (!formData.claimDescription) {
      errors.claimDescription = 'Claim description is required';
    } else if (formData.claimDescription.length < TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH) {
      errors.claimDescription = `Description must be at least ${TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH} characters`;
    } else if (formData.claimDescription.length > TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH) {
      errors.claimDescription = `Description must be less than ${TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH} characters`;
    }

    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error for this field when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errors = validateForm();
    
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }

    onSubmit(formData);
  };

  return (
    <div className="card" id="analyze">
      <div className={styles.formHeader}>
        <FileText className={styles.headerIcon} size={24} />
        <div>
          <h2 className="section-title">Analyze New Claim</h2>
          <p className="text-secondary">Enter the claim details to run fraud detection analysis.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGrid}>
          <div className={styles.formGroup}>
            <label htmlFor="incidentType">Incident Type *</label>
            <select
              id="incidentType"
              name="incidentType"
              value={formData.incidentType}
              onChange={handleChange}
              style={{ borderColor: validationErrors.incidentType ? '#dc2626' : '' }}
            >
              <option value="">Select type...</option>
              <option value="Multi-vehicle Collision">Multi-vehicle Collision</option>
              <option value="Single Vehicle Collision">Single Vehicle Collision</option>
              <option value="Vehicle Theft">Vehicle Theft</option>
              <option value="Parked Car">Parked Car</option>
            </select>
            {validationErrors.incidentType && (
              <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <AlertCircle size={14} />
                {validationErrors.incidentType}
              </div>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="incidentCity">Incident City * (Max {TECHNICAL_PARAMS.CITY_MAX_LENGTH} chars)</label>
            <input
              type="text"
              id="incidentCity"
              name="incidentCity"
              placeholder="e.g. Columbus"
              value={formData.incidentCity}
              onChange={handleChange}
              maxLength={TECHNICAL_PARAMS.CITY_MAX_LENGTH}
              style={{ borderColor: validationErrors.incidentCity ? '#dc2626' : '' }}
            />
            {validationErrors.incidentCity && (
              <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <AlertCircle size={14} />
                {validationErrors.incidentCity}
              </div>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="policyState">Policy State *</label>
            <select
              id="policyState"
              name="policyState"
              value={formData.policyState}
              onChange={handleChange}
              style={{ borderColor: validationErrors.policyState ? '#dc2626' : '' }}
            >
              <option value="">Select state...</option>
              <option value="OH">Ohio</option>
              <option value="IL">Illinois</option>
              <option value="IN">Indiana</option>
              <option value="NY">New York</option>
              <option value="CA">California</option>
            </select>
            {validationErrors.policyState && (
              <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <AlertCircle size={14} />
                {validationErrors.policyState}
              </div>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="insuredRelationship">Insured Relationship *</label>
            <select
              id="insuredRelationship"
              name="insuredRelationship"
              value={formData.insuredRelationship}
              onChange={handleChange}
              style={{ borderColor: validationErrors.insuredRelationship ? '#dc2626' : '' }}
            >
              <option value="">Select relationship...</option>
              <option value="own-child">Own Child</option>
              <option value="other-relative">Other Relative</option>
              <option value="not-in-family">Not in Family</option>
              <option value="husband">Husband</option>
              <option value="wife">Wife</option>
              <option value="unmarried">Unmarried</option>
            </select>
            {validationErrors.insuredRelationship && (
              <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <AlertCircle size={14} />
                {validationErrors.insuredRelationship}
              </div>
            )}
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="claimAmount">Claim Amount ($) * (${TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN} - ${TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX})</label>
            <input
              type="number"
              id="claimAmount"
              name="claimAmount"
              placeholder="e.g. 50000"
              value={formData.claimAmount}
              onChange={handleChange}
              min={TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN}
              max={TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX}
              style={{ borderColor: validationErrors.claimAmount ? '#dc2626' : '' }}
            />
            {validationErrors.claimAmount && (
              <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <AlertCircle size={14} />
                {validationErrors.claimAmount}
              </div>
            )}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="claimDescription">Claim Description (Narrative) * ({TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH}-{TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH} chars)</label>
          <textarea
            id="claimDescription"
            name="claimDescription"
            rows="5"
            placeholder="Provide a detailed description of the incident..."
            value={formData.claimDescription}
            onChange={handleChange}
            maxLength={TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH}
            style={{ borderColor: validationErrors.claimDescription ? '#dc2626' : '', resize: 'vertical' }}
          ></textarea>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            {formData.claimDescription.length}/{TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH} characters
          </p>
          {validationErrors.claimDescription && (
            <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertCircle size={14} />
              {validationErrors.claimDescription}
            </div>
          )}
        </div>

        <div className={styles.formActions}>
          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? (
              <>Processing...</>
            ) : (
              <>
                <Send size={18} />
                Analyze Claim
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClaimForm;
