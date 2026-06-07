import React, { useState } from 'react';
import { FileText, Send, AlertCircle } from 'lucide-react';
import styles from './ClaimForm.module.css';

const TECHNICAL_PARAMS = {
  CLAIM_AMOUNT_MIN: 100,
  CLAIM_AMOUNT_MAX: 1000000,
  DESCRIPTION_MIN_LENGTH: 20,
  DESCRIPTION_MAX_LENGTH: 5000,
  CITY_MAX_LENGTH: 50,
  // These arrays must stay in sync with preprocessing.py ENCODINGS.
  // The alphabetical order here is for display only; encoding happens in the backend.
  INCIDENT_TYPES: [
    'Multi-vehicle Collision',
    'Single Vehicle Collision',
    'Vehicle Theft',
    'Parked Car',
  ],
  POLICY_STATES: ['IL', 'IN', 'OH'],
  INCIDENT_CITIES: [
    'Arlington',
    'Columbus',
    'Hillsdale',
    'Northbend',
    'Northbrook',
    'Riverwood',
    'Springfield',
  ],
  INSURED_RELATIONSHIPS: [
    'husband',
    'not-in-family',
    'other-relative',
    'own-child',
    'unmarried',
    'wife',
  ],
  // FIX: Sorted alphabetically to match LabelEncoder order — makes it easier to
  // spot encoding mismatches during debugging.
  INCIDENT_SEVERITY: ['Major Damage', 'Minor Damage', 'Total Loss', 'Trivial Damage'],
  COLLISION_TYPES: ['Front Collision', 'Rear Collision', 'Side Collision'],
  BOOLEAN_OPTIONS: ['NO', 'YES'],  // FIX: NO listed first so "Select" default doesn't silently mean YES
};

// Fields that are required — must match validateForm() below.
// All fields that meaningfully affect the prediction are required to prevent
// silent bad defaults (especially fraud-correlated YES/NO fields).
const REQUIRED_FIELDS = [
  'incidentType',
  'incidentCity',
  'policyState',
  'insuredRelationship',
  'claimAmount',
  'claimDescription',
  // FIX: incidentSeverity, collisionType, propertyDamage, policeReportAvailable
  // are now required. These fields directly affect the prediction — leaving them
  // blank caused the backend to use fraud-biased defaults (e.g. propertyDamage=YES).
  'incidentSeverity',
  'collisionType',
  'propertyDamage',
  'policeReportAvailable',
];

const FIELD_LABELS = {
  incidentType:          'Incident Type',
  incidentCity:          'Incident City',
  policyState:           'Policy State',
  insuredRelationship:   'Insured Relationship',
  claimAmount:           'Claim Amount',
  claimDescription:      'Claim Description',
  incidentSeverity:      'Incident Severity',
  collisionType:         'Collision Type',
  propertyDamage:        'Property Damage',
  policeReportAvailable: 'Police Report Available',
  witnesses:             'Witnesses',
};

const ClaimForm = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    incidentType:          '',
    incidentCity:          '',
    policyState:           '',
    insuredRelationship:   '',
    claimAmount:           '',
    claimDescription:      '',
    incidentSeverity:      '',
    collisionType:         '',
    propertyDamage:        '',
    policeReportAvailable: '',
    witnesses:             '',
  });

  const [validationErrors, setValidationErrors] = useState({});

  const validateForm = () => {
    const errors = {};

    // --- Required field presence check ---
    REQUIRED_FIELDS.forEach((field) => {
      const val = formData[field];
      if (!val || (typeof val === 'string' && val.trim() === '')) {
        errors[field] = `${FIELD_LABELS[field] || field} is required`;
      }
    });

    // --- Claim amount range check ---
    const amount = parseFloat(formData.claimAmount);
    if (
      formData.claimAmount &&
      (isNaN(amount) ||
        amount < TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN ||
        amount > TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX)
    ) {
      errors.claimAmount = `Amount must be between $${TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN.toLocaleString()} and $${TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX.toLocaleString()}`;
    }

    // --- Description length check ---
    const desc = formData.claimDescription;
    if (
      desc &&
      (desc.length < TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH ||
        desc.length > TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH)
    ) {
      errors.claimDescription = `Description must be between ${TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH} and ${TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH} characters`;
    }

    // --- Witnesses range check (optional field) ---
    if (formData.witnesses !== '') {
      const w = parseInt(formData.witnesses, 10);
      if (isNaN(w) || w < 0 || w > 10) {
        errors.witnesses = 'Witnesses must be a number between 0 and 10';
      }
    }

    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field as soon as user changes it
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      // Scroll to first error
      const firstErrorField = document.querySelector(`.${styles.errorText}`);
      if (firstErrorField) firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    setValidationErrors({});
    onSubmit(formData);
  };

  const renderError = (field) =>
    validationErrors[field] ? (
      <div className={styles.errorText}>
        <AlertCircle size={14} />
        {' '}
        {validationErrors[field]}
      </div>
    ) : null;

  const isRequired = (field) => REQUIRED_FIELDS.includes(field);

  return (
    <div className="card" id="analyze">
      <div className={styles.formHeader}>
        <FileText className={styles.headerIcon} size={24} />
        <div>
          <h2 className="section-title">Analyze New Claim</h2>
          <p className="text-secondary">
            Enter claim details for fraud detection analysis. Fields marked * are required.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className={styles.form} noValidate>
        <div className={styles.formGrid}>

          {/* ---- Incident Type ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="incidentType">
              Incident Type{isRequired('incidentType') ? ' *' : ''}
            </label>
            <select
              id="incidentType"
              name="incidentType"
              value={formData.incidentType}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select type...</option>
              {TECHNICAL_PARAMS.INCIDENT_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            {renderError('incidentType')}
          </div>

          {/* ---- Incident City ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="incidentCity">
              Incident City{isRequired('incidentCity') ? ' *' : ''}
            </label>
            <select
              id="incidentCity"
              name="incidentCity"
              value={formData.incidentCity}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select city...</option>
              {TECHNICAL_PARAMS.INCIDENT_CITIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            {renderError('incidentCity')}
          </div>

          {/* ---- Policy State ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="policyState">
              Policy State{isRequired('policyState') ? ' *' : ''}
            </label>
            <select
              id="policyState"
              name="policyState"
              value={formData.policyState}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select state...</option>
              {TECHNICAL_PARAMS.POLICY_STATES.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
            {renderError('policyState')}
          </div>

          {/* ---- Insured Relationship ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="insuredRelationship">
              Insured Relationship{isRequired('insuredRelationship') ? ' *' : ''}
            </label>
            <select
              id="insuredRelationship"
              name="insuredRelationship"
              value={formData.insuredRelationship}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select relationship...</option>
              {TECHNICAL_PARAMS.INSURED_RELATIONSHIPS.map((r) => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
            {renderError('insuredRelationship')}
          </div>

          {/* ---- Incident Severity (now required) ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="incidentSeverity">
              Incident Severity{isRequired('incidentSeverity') ? ' *' : ''}
            </label>
            <select
              id="incidentSeverity"
              name="incidentSeverity"
              value={formData.incidentSeverity}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select severity...</option>
              {TECHNICAL_PARAMS.INCIDENT_SEVERITY.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
            {renderError('incidentSeverity')}
          </div>

          {/* ---- Collision Type (now required) ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="collisionType">
              Collision Type{isRequired('collisionType') ? ' *' : ''}
            </label>
            <select
              id="collisionType"
              name="collisionType"
              value={formData.collisionType}
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select type...</option>
              {TECHNICAL_PARAMS.COLLISION_TYPES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            {renderError('collisionType')}
          </div>

          {/* ---- Property Damage (now required) ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="propertyDamage">
              Property Damage{isRequired('propertyDamage') ? ' *' : ''}
            </label>
            <select
              id="propertyDamage"
              name="propertyDamage"
              value={formData.propertyDamage}
              onChange={handleChange}
              aria-required="true"
            >
              {/* FIX: "Select" placeholder forces an explicit choice — no silent YES default */}
              <option value="">Select...</option>
              {TECHNICAL_PARAMS.BOOLEAN_OPTIONS.map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
            {renderError('propertyDamage')}
          </div>

          {/* ---- Police Report Available (now required) ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="policeReportAvailable">
              Police Report Available{isRequired('policeReportAvailable') ? ' *' : ''}
            </label>
            <select
              id="policeReportAvailable"
              name="policeReportAvailable"
              value={formData.policeReportAvailable}
              onChange={handleChange}
              aria-required="true"
            >
              {/* FIX: "Select" placeholder forces an explicit choice — no silent YES default */}
              <option value="">Select...</option>
              {TECHNICAL_PARAMS.BOOLEAN_OPTIONS.map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
            {renderError('policeReportAvailable')}
          </div>

          {/* ---- Witnesses (optional) ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="witnesses">Witnesses (0–10)</label>
            <input
              id="witnesses"
              type="number"
              name="witnesses"
              min="0"
              max="10"
              value={formData.witnesses}
              onChange={handleChange}
              placeholder="e.g. 1"
            />
            {renderError('witnesses')}
          </div>

          {/* ---- Claim Amount ---- */}
          <div className={styles.formGroup}>
            <label htmlFor="claimAmount">
              Claim Amount ($){isRequired('claimAmount') ? ' *' : ''}
            </label>
            <input
              id="claimAmount"
              type="number"
              name="claimAmount"
              value={formData.claimAmount}
              onChange={handleChange}
              placeholder="e.g. 50000"
              min={TECHNICAL_PARAMS.CLAIM_AMOUNT_MIN}
              max={TECHNICAL_PARAMS.CLAIM_AMOUNT_MAX}
            />
            {renderError('claimAmount')}
          </div>

        </div>{/* end formGrid */}

        {/* ---- Claim Description (full width) ---- */}
        <div className={styles.formGroup}>
          <label htmlFor="claimDescription">
            Claim Description{isRequired('claimDescription') ? ' *' : ''}
          </label>
          <textarea
            id="claimDescription"
            name="claimDescription"
            rows="4"
            value={formData.claimDescription}
            onChange={handleChange}
            placeholder="Detailed incident description (min 20 characters)..."
          />
          <small>
            {formData.claimDescription.length} / {TECHNICAL_PARAMS.DESCRIPTION_MAX_LENGTH} chars
            {formData.claimDescription.length < TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH &&
              formData.claimDescription.length > 0 && (
                <span style={{ color: 'var(--color-warning, orange)', marginLeft: '8px' }}>
                  (min {TECHNICAL_PARAMS.DESCRIPTION_MIN_LENGTH} chars required)
                </span>
              )}
          </small>
          {renderError('claimDescription')}
        </div>

        <button type="submit" className="btn-primary" disabled={isLoading}>
          {isLoading ? 'Processing...' : (
            <>
              <Send size={18} />
              {' '}
              Analyze Claim
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default ClaimForm;
