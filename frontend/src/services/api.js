import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Calls the Flask backend to analyze a claim.
 * @param {Object} claimData - The form data submitted by the user.
 * @returns {Promise} - Resolves with prediction results from the backend.
 */
export const analyzeClaim = async (claimData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, claimData);
    return response.data;
  } catch (error) {
    console.error("Error calling the backend API:", error);
    // Return a fallback or throw error based on your error handling preference
    throw new Error('Failed to analyze claim. Ensure the Flask backend is running on port 5000.');
  }
};
