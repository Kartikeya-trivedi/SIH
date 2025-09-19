import React, { useRef, useState } from 'react';
// Ensure your service file is correctly located at 'src/services/kolamService.js'
import kolamService from '../services/kolamService'; 
import './Recognize.css';

// Helper function to convert a base64 data URL to a File object for the camera capture
const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}

const Recognize = ({ onAnalysisSuccess, onNavigate }) => {
    const fileInputRef = useRef(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    const [isCameraOn, setIsCameraOn] = useState(false);
    const [stream, setStream] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const stopCamera = () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        setIsCameraOn(false);
        setStream(null);
    };

    // This function calls your service and handles the result
    const runAnalysis = async (imageFile, imagePreview) => {
        setIsLoading(true);
        setError('');
        try {
            const response = await kolamService.predictKolam(imageFile);
            // On success, pass the full result up to the App component
            onAnalysisSuccess({
                image: imagePreview,
                prediction: response.data,
            });
        } catch (err) {
            setError('Analysis failed. Please check the server connection and try again.');
            console.error("Prediction Error:", err);
        } finally {
            setIsLoading(false);
            stopCamera();
        }
    };

    // This function is triggered when the user selects a file
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                // We pass the original File object for the API and the data URL for the preview
                runAnalysis(file, reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    // This function is called when the "Upload" button is clicked
    const handleUploadClick = () => {
        stopCamera();
        // Programmatically click the hidden file input element
        fileInputRef.current.click();
    };

    const handleCaptureClick = async () => {
        setError('');
        if (isCameraOn) {
            if (videoRef.current && canvasRef.current) {
                const video = videoRef.current;
                const canvas = canvasRef.current;
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageDataUrl = canvas.toDataURL('image/png');
                const imageFile = dataURLtoFile(imageDataUrl, 'capture.png');
                runAnalysis(imageFile, imageDataUrl);
            }
        } else {
            try {
                const newStream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (videoRef.current) videoRef.current.srcObject = newStream;
                setStream(newStream);
                setIsCameraOn(true);
            } catch (err) {
                setError('Could not access the camera. Please check permissions.');
            }
        }
    };

    const handleRecreateClick = () => {
        stopCamera();
        onNavigate('/recreate');
    };

    return (
        <div className="recognize-container">
            {/* Hidden file input element, controlled by the "Upload" button */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
                accept="image/*"
            />

            <h1 className="recognize-title">Let The AI Recognize</h1>
            <p className="recognize-subtitle">Upload or capture an image for analysis.</p>

            <div className="display-area">
                {isLoading ? (
                    <div className="loading-spinner"></div>
                ) : isCameraOn ? (
                    <div className="camera-view">
                        <video ref={videoRef} autoPlay playsInline className="video-feed"></video>
                        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
                    </div>
                ) : (
                    <div className="display-placeholder"><p>Image preview will appear here</p></div>
                )}
            </div>

            {error && <p className="error-message">{error}</p>}

            <div className="recognize-controls">
                <button className="recognize-button" onClick={handleUploadClick} disabled={isLoading}>Upload</button>
                <button className="recognize-button" onClick={handleCaptureClick} disabled={isLoading}>{isCameraOn ? 'Take Photo' : 'Capture'}</button>
                <button className="recognize-button" onClick={handleRecreateClick} disabled={isLoading}>Recreate</button>
            </div>
        </div>
    );
};

export default Recognize;

