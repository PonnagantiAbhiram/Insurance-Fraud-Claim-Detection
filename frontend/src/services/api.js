import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Calls the Flask backend to analyze a claim.
 * @param {Object} claimData - The form data submitted by the user.
 * @returns {Promise} - Resolves with prediction results from the backend.
 */
export const analyzeClaim = async (claimData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, claimData, {
      timeout: 60000, // 60 second timeout
    });
    return response.data;
  } catch (error) {
    console.error("Error calling the backend API:", error);
    
    if (error.response) {
      // Backend returned an error response
      const status = error.response.status;
      const data = error.response.data;
      
      if (status === 503) {
        // Models not loaded
        throw new Error(data.error || 'Models are not loaded. Please run the Jupyter notebook first.');
      } else if (status === 500) {
        // General server error
        throw new Error(data.error || 'Server error. Please ensure the backend is running correctly.');
      } else {
        throw new Error(data.error || `Backend error (${status})`);
      }
    } else if (error.request) {
      // No response from backend
      throw new Error('Cannot connect to backend. Ensure Flask is running on http://localhost:5000');
    } else {
      // Other error
      throw new Error('Failed to analyze claim: ' + error.message);
    }
  }
};
