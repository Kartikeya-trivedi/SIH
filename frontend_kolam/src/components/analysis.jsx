import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Analysis.css';

const Analysis = ({ analysisData }) => {
  const navigate = useNavigate();

  useEffect(() => {
    // Log received data for debugging
    console.log('Analysis component received data:', analysisData);
  }, [analysisData]);

  // If no data is passed, show a message and a way to go back.
  if (!analysisData) {
    return (
      <div className="analysis-container">
        <div className="analysis-card">
          <h2>No Analysis Data</h2>
          <p>Please go back and upload or capture an image first.</p>
          <button onClick={() => navigate('/recognize')} className="back-btn">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  // Extract data from the API response
  const { label, confidence, design_principle, imageUrl } = analysisData;
  
  // Convert confidence to a valid number
  const confidenceValue = parseFloat(confidence);
  const displayConfidence = !isNaN(confidenceValue) 
    ? `${(confidenceValue * 100).toFixed(2)}%` 
    : 'Unavailable';

  return (
    <div className="analysis-container">
      <div className="analysis-card">
        <div className="analysis-image-container">
          <img src={imageUrl} alt="Analyzed Kolam" className="analysis-image" />
        </div>
        <div className="analysis-content">
          <div className="analysis-header">
            <h3>Identified as: {label || 'Unknown'}</h3>
            <p className="confidence">Confidence: {displayConfidence}</p>
          </div>
          <div className="analysis-body">
            <h4>Design Principle:</h4>
            <p>{design_principle || 'No design principle information available.'}</p>
          </div>
        </div>
        <button onClick={() => navigate('/recognize')} className="back-btn">
          Analyze Another
        </button>
      </div>
    </div>
  );
};

export default Analysis;
