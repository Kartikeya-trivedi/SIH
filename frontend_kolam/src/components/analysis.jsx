import React from 'react';
import './Analysis.css';

const Analysis = ({ analysisData, setCurrentRoute }) => {
  // If no data is passed, show a message and a way to go back.
  if (!analysisData) {
    return (
      <div className="analysis-container">
        <div className="analysis-card">
          <h2>No Analysis Data</h2>
          <p>Please go back and upload or capture an image first.</p>
          <button onClick={() => setCurrentRoute('/recognize')} className="back-btn">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const { imageSrc, header, body } = analysisData;

  return (
    <div className="analysis-container">
      <div className="analysis-card">
        <div className="analysis-image-container">
          <img src={imageSrc} alt="Analyzed Kolam" className="analysis-image" />
        </div>
        <div className="analysis-content">
          <div className="analysis-header">
            <h3>{header}</h3>
          </div>
          <div className="analysis-body">
            <p>{body}</p>
          </div>
        </div>
        <button onClick={() => setCurrentRoute('/recognize')} className="back-btn">
          Analyze Another
        </button>
      </div>
    </div>
  );
};

export default Analysis;
