import React, { useState, useRef } from 'react';
import kolamService from '../services/kolamService';
import './AiRecreate.css';

const AiRecreate = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [error, setError] = useState('');
  const [explanation, setExplanation] = useState('');
  
  // Animation state
  const [isPromptActive, setIsPromptActive] = useState(false);
  const [isButtonVisible, setIsButtonVisible] = useState(true);
  const promptRef = useRef(null);
  
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

  // Handle the animation sequence when button is clicked
  const handleButtonClick = () => {
    if (!prompt.trim()) {
      alert('Please enter a description for the Kolam pattern.');
      return;
    }
    
    // Step 1: Start title fade-out animation immediately
    setIsPromptActive(true);
    
    // Step 2: Wait just a moment before fading button
    setTimeout(() => {
      setIsButtonVisible(false);
      
      // Step 3: Wait for animations to complete before starting API call
      setTimeout(() => {
        handleCreateRequest();
      }, 800); // Shorter wait time for faster animations
    }, 800); // Shorter wait time for faster animations
  };
  
  // Reset the UI when user wants to create a new design
  const handleResetUI = () => {
    setGeneratedImage(null);
    setExplanation('');
    setError('');
    setIsPromptActive(false);
    setIsButtonVisible(true);
  };

  // Actual API request function
  const handleCreateRequest = async () => {
    setIsLoading(true);
    setGeneratedImage(null);
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
      <div className={`title-container ${isPromptActive ? 'title-hidden' : ''}`}>
        <h1 className="recreate-title">Let The AI Recreate</h1>
        <p className="recreate-subtitle">
          "Simply describe your idea, and let AI craft the design for you."
        </p>
      </div>

      {/* Prompt textarea with animation class */}
      <div 
        className={`prompt-container ${isPromptActive ? 'prompt-active' : ''}`}
        ref={promptRef}
      >
        <textarea
          className="prompt-textarea"
          placeholder="A simple Kolam with four intersecting lines, creating a diamond shape in the center..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={isLoading || isPromptActive}
        />
      </div>

      {/* Display error if any */}
      {error && (
        <div className="recreate-error">
          <p>{error}</p>
        </div>
      )}

      {/* The generated image will appear here */}
      {generatedImage && !isLoading && (
        <div className="recreate-output-container">
          <div className="image-wrapper">
            <img 
              src={generatedImage} 
              alt="Generated Kolam Pattern" 
              className="generated-image"
              onError={() => setError('Failed to load the generated image')} 
            />
          </div>
          {explanation && (
            <div className="recreate-explanation">
              <h3>Design Insight</h3>
              <p>{explanation}</p>
            </div>
          )}
          
          {/* Reset button to create a new design */}
          <button
            className="recreate-reset-button"
            onClick={handleResetUI}
          >
            Create New Design
          </button>
        </div>
      )}

      {/* Loading indicator */}
      {isLoading && (
        <div className="recreate-output-container">
          <div className="recreate-loader"></div>
          <p>Generating your Kolam design. This may take a moment...</p>
        </div>
      )}

      {/* Main action button with animation class */}
      <button
        className={`recreate-button ${isButtonVisible ? '' : 'button-hidden'}`}
        onClick={handleButtonClick}
        disabled={isLoading || isPromptActive}
      >
        Let the AI Recreate
      </button>
    </div>
  );
};

export default AiRecreate;

