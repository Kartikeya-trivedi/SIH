import React, { useState } from 'react';
import './AiRecreate.css';

const AiRecreate = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);

  const handleCreateClick = () => {
    if (!prompt.trim()) {
      alert('Please enter a description for the Kolam pattern.');
      return;
    }
    setIsLoading(true);
    setGeneratedImage(null); // Clear previous image while generating a new one

    // Simulate an API call to generate an image
    setTimeout(() => {
      // In a real app, you would get the image URL from your AI service
      const newImage = 'https://i.imgur.com/gK2R4Xp.png';
      setGeneratedImage(newImage);
      setIsLoading(false);
    }, 1500); // 1.5-second delay to simulate generation
  };

  return (
    <div className="ai-recreate-container">
      <h1 className="recreate-title">Let The AI Recreate</h1>
      <p className="recreate-subtitle">
        "Simply describe your idea, and let AI craft the design for you."
      </p>

      <textarea
        className="prompt-textarea"
        placeholder="A simple Kolam with four intersecting lines, creating a diamond shape in the center..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        disabled={isLoading}
      />

      {/* The generated image will now appear here */}
      {generatedImage && !isLoading && (
        <div className="recreate-output-container">
          <img src={generatedImage} alt="Generated Kolam Pattern" className="generated-image" />
        </div>
      )}

      {/* Loading indicator appears in the same spot */}
      {isLoading && (
        <div className="recreate-output-container">
          <div className="recreate-loader"></div>
        </div>
      )}

      {/* The button is now always at the bottom */}
      <button
        className="recreate-button"
        onClick={handleCreateClick}
        disabled={isLoading}
      >
        {isLoading ? 'Creating...' : (generatedImage ? 'Recreate' : 'Create')}
      </button>
    </div>
  );
};

export default AiRecreate;

