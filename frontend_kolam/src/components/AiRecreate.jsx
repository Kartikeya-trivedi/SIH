import React, { useState } from 'react';
import kolamService from '../services/kolamService';
import './AiRecreate.css';

const AiRecreate = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [error, setError] = useState('');
  const [explanation, setExplanation] = useState('');

  // Function to clean up the explanation text
  const cleanExplanationText = (text) => {
    if (!text) return '';
    
    // Extract only the relevant part by removing query, context, and system prompt
    let cleaned = text;
    
    // Remove "Query: {query}\nContext: [Document..." part
    if (cleaned.includes('Query:') && cleaned.includes('Context:')) {
      cleaned = cleaned.split('Context:')[1] || cleaned;
      // Find the end of the context section
      const contextEndIndex = cleaned.indexOf('You are an AI assistant');
      if (contextEndIndex !== -1) {
        cleaned = cleaned.substring(contextEndIndex);
      }
    }
    
    // Remove system prompt part
    const systemPromptStart = cleaned.indexOf('You are an AI assistant');
    if (systemPromptStart !== -1) {
      cleaned = cleaned.substring(0, systemPromptStart).trim();
    }
    
    // Remove any Document mentions
    cleaned = cleaned.replace(/Document\(content=['"][^'"]*['"]/, '');
    
    // Clean up special characters and formatting
    cleaned = cleaned.replace(/\\n/g, ' ') // Replace newline characters with spaces
                    .replace(/\s+/g, ' ')  // Replace multiple spaces with a single space
                    .replace(/\[.*?\]/g, '') // Remove anything in square brackets
                    .trim();
    
    // If we've removed too much, provide a fallback
    if (cleaned.length < 20) {
      return "This Kolam design is inspired by traditional patterns. The generated image represents the essence of your prompt.";
    }
    
    return cleaned;
  };

  const handleCreateClick = async () => {
    if (!prompt.trim()) {
      alert('Please enter a description for the Kolam pattern.');
      return;
    }
    setIsLoading(true);
    setGeneratedImage(null); // Clear previous image while generating a new one
    setError('');
    setExplanation('');

    try {
      console.log('Sending generation request with prompt:', prompt);
      // Use the knowledge endpoint with generate_image=true
      const result = await kolamService.getKolamKnowledge(prompt, true);
      console.log('Generation response:', result.data);
      
      if (result.data) {
        // Process and set the explanation
        const cleanedExplanation = cleanExplanationText(result.data.explanation);
        setExplanation(cleanedExplanation);
        
        // Check if an image was generated
        if (result.data.image_base64) {
          setGeneratedImage(`data:image/jpeg;base64,${result.data.image_base64}`);
        } else {
          setError('No image was generated. Please try a different prompt.');
        }
      } else {
        setError('Received invalid response from server');
      }
    } catch (err) {
      console.error('Error generating image:', err);
      setError('Failed to generate image. Please try again later.');
    } finally {
      setIsLoading(false);
    }
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

      {/* Display error if any */}
      {error && (
        <div className="recreate-error">
          <p>{error}</p>
        </div>
      )}

      {/* The generated image will now appear here */}
      {generatedImage && !isLoading && (
        <div className="recreate-output-container">
          <img 
            src={generatedImage} 
            alt="Generated Kolam Pattern" 
            className="generated-image"
            onError={() => setError('Failed to load the generated image')} 
          />
          {explanation && (
            <div className="recreate-explanation">
              <h3>Design Insight</h3>
              <p>{explanation}</p>
            </div>
          )}
        </div>
      )}

      {/* Loading indicator appears in the same spot */}
      {isLoading && (
        <div className="recreate-output-container">
          <div className="recreate-loader"></div>
          <p>Generating your Kolam design. This may take a moment...</p>
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

