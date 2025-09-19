import React from 'react';
import './Analysis.css';

const Analysis = ({ analysisData, onNavigate }) => {
  // Guard clause in case the user navigates here directly without data
  if (!analysisData) {
    return (
      <div className="analysis-container">
        <div className="analysis-card">
          <p>No analysis data available. Please upload an image first.</p>
          <button className="analyze-another-btn" onClick={() => onNavigate('/recognize')}>
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const { image, prediction } = analysisData;

  // Safely access prediction data with fallbacks
  const kolamClass = prediction?.label || 'Unknown';
  const confidence = prediction?.confidence; // already a percentage from backend
  const designPrinciple = prediction?.design_principle || 'No design principle information available.';

  return (
    <div className="analysis-container">
      <div className="analysis-card">
        <div className="image-display">
            {image && <img src={image} alt="Analyzed Kolam" />}
        </div>
        <div className="result-box">
            <p><strong>Identified as:</strong> {kolamClass}</p>
            <p><strong>Confidence:</strong> {typeof confidence === 'number' ? `${(confidence * 100).toFixed(1)}%` : 'Unavailable'}</p>
        </div>
        <div className="result-box">
            <p><strong>Design Principle:</strong></p>
            <p>{designPrinciple}</p>
        </div>
        <button className="analyze-another-btn" onClick={() => onNavigate('/recognize')}>
            Analyze Another
        </button>
      </div>
    </div>
  );
};

export default Analysis;

