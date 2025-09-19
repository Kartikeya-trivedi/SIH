import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import kolamService from '../services/kolamService';
import './Recognize.css';
import './analyze-button.css';

const Recognize = ({ onAnalysisSuccess }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [error, setError] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  // Hidden file input for the upload button
  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImageSrc(e.target.result);
        setIsCameraOpen(false); // Close camera if it was open
      };
      reader.readAsDataURL(file);
    }
  };

  // Function to start the camera
  const startCamera = async () => {
    // Check if mediaDevices is supported
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        setIsCameraOpen(true);
        setImageSrc(null); // Clear previous image
        setError('');
      } catch (err) {
        console.error("Error accessing camera: ", err);
        setError('Could not access the camera. Please check permissions and try again.');
        setIsCameraOpen(false);
      }
    } else {
      setError('Your browser does not support camera access.');
    }
  };

  // Function to take a picture
  const takePicture = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      // Set canvas dimensions to match the video stream
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
      
      const dataUrl = canvas.toDataURL('image/png');
      setImageSrc(dataUrl);
      
      // Convert dataURL to File object
      canvas.toBlob((blob) => {
        const file = new File([blob], "captured-image.png", { type: "image/png" });
        setImageFile(file);
      });
      
      stopCamera();
    }
  };

  // Function to analyze the image using backend API
  const analyzeImage = async () => {
    if (!imageFile) {
      setError('No image to analyze. Please upload or capture an image first.');
      return;
    }
    
    try {
      setIsAnalyzing(true);
      setError('');
      
      console.log('Sending image file for analysis:', imageFile);
      const response = await kolamService.predictKolam(imageFile);
      
      console.log('Raw API response:', response);
      
      // If successful, call the onAnalysisSuccess callback with the response data
      if (response && response.data) {
        console.log('Processing response data:', response.data);
        // Make sure confidence is a valid number
        const processedData = {
          ...response.data,
          confidence: typeof response.data.confidence === 'number' ? response.data.confidence : 0,
          imageUrl: imageSrc,
        };
        console.log('Processed data for UI:', processedData);
        onAnalysisSuccess(processedData);
      }
    } catch (err) {
      console.error('Error analyzing image:', err);
      console.error('Error details:', err.response?.data || err.message);
      setError('Failed to analyze the image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Function to stop the camera stream
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsCameraOpen(false);
  };

  return (
    <div className="recognize-container">
      <h1 className="recognize-title">Let The AI Recognize</h1>
      <p className="recognize-subtitle">
        Upload images and get AI-powered analysis of Kolam patterns
      </p>

      {/* Display the captured or uploaded image */}
      {imageSrc && !isCameraOpen && (
        <div className="image-preview-container">
          <img src={imageSrc} alt="Kolam Preview" className="image-preview" />
          <button 
            onClick={analyzeImage} 
            className="analyze-btn"
            disabled={isAnalyzing}
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze Image'}
          </button>
        </div>
      )}

      {/* Display the camera view if active */}
      {isCameraOpen && (
        <div className="camera-view-container">
          <video ref={videoRef} autoPlay playsInline className="camera-stream"></video>
          <button onClick={takePicture} className="capture-snapshot-btn">
            Take Picture
          </button>
        </div>
      )}
      
      {/* Hidden canvas for capturing the image frame */}
      <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
      
      {/* Display error message if any */}
      {error && <p className="error-message">{error}</p>}

      <div className="recognize-actions">
        {!isCameraOpen ? (
          <>
            <button onClick={handleUploadClick} className="action-btn">
              <span>&#x2191;</span> Upload
            </button>
            <button onClick={startCamera} className="action-btn">
              <span>&#x1F4F7;</span> Capture
            </button>
          </>
        ) : (
           <button onClick={stopCamera} className="action-btn stop-btn">
              Cancel
            </button>
        )}
      </div>

      <button
        className="action-btn small-btn"
        onClick={() => navigate('/recreate')}
      >
        <span>&#x2699;&#xFE0F;</span>Recreate or complete patterns
      </button>

      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        accept="image/*"
      />
    </div>
  );
};

export default Recognize;

