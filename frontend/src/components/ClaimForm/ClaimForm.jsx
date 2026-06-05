import React, { useState } from 'react';
import { FileText, Send } from 'lucide-react';
import styles from './ClaimForm.module.css';

const ClaimForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    incidentType: '',
    incidentCity: '',
    policyState: '',
    insuredRelationship: '',
    claimAmount: '',
    claimDescription: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
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
            <label htmlFor="incidentType">Incident Type</label>
            <select
              id="incidentType"
              name="incidentType"
              value={formData.incidentType}
              onChange={handleChange}
              required
            >
              <option value="">Select type...</option>
              <option value="Multi-vehicle Collision">Multi-vehicle Collision</option>
              <option value="Single Vehicle Collision">Single Vehicle Collision</option>
              <option value="Vehicle Theft">Vehicle Theft</option>
              <option value="Parked Car">Parked Car</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="incidentCity">Incident City</label>
            <input
              type="text"
              id="incidentCity"
              name="incidentCity"
              placeholder="e.g. Columbus"
              value={formData.incidentCity}
              onChange={handleChange}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="policyState">Policy State</label>
            <select
              id="policyState"
              name="policyState"
              value={formData.policyState}
              onChange={handleChange}
              required
            >
              <option value="">Select state...</option>
              <option value="OH">Ohio</option>
              <option value="IL">Illinois</option>
              <option value="IN">Indiana</option>
              <option value="NY">New York</option>
              <option value="CA">California</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="insuredRelationship">Insured Relationship</label>
            <select
              id="insuredRelationship"
              name="insuredRelationship"
              value={formData.insuredRelationship}
              onChange={handleChange}
              required
            >
              <option value="">Select relationship...</option>
              <option value="own-child">Own Child</option>
              <option value="other-relative">Other Relative</option>
              <option value="not-in-family">Not in Family</option>
              <option value="husband">Husband</option>
              <option value="wife">Wife</option>
              <option value="unmarried">Unmarried</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="claimAmount">Claim Amount ($)</label>
            <input
              type="number"
              id="claimAmount"
              name="claimAmount"
              placeholder="e.g. 50000"
              value={formData.claimAmount}
              onChange={handleChange}
              min="0"
              required
            />
          </div>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="claimDescription">Claim Description (Narrative)</label>
          <textarea
            id="claimDescription"
            name="claimDescription"
            rows="5"
            placeholder="Provide a detailed description of the incident..."
            value={formData.claimDescription}
            onChange={handleChange}
            required
          ></textarea>
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
