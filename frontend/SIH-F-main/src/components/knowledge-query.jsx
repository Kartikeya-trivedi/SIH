import React, { useState, useEffect } from 'react';
import kolamService from '../services/kolamService';
import MOCK_KNOWLEDGE_DATA from '../data/mockKnowledgeData';
import './knowledge-query.css';

const KnowledgeQuery = () => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [response, setResponse] = useState(null);
    const [imageError, setImageError] = useState(false);
    const [apiStatus, setApiStatus] = useState({ checked: false, available: false, message: '' });

    // Check if we're in development mode or if we need to use mock data
    const useMockData = import.meta.env.DEV || import.meta.env.VITE_USE_MOCK_DATA === 'true';
    
    // Mock data for fallback if the API is unavailable
    const mockKnowledgeResponse = {
        explanation: "Kolam is a traditional form of art practiced in South India. It involves drawing geometric patterns using rice flour, chalk, or rock powder. Kolams are typically drawn at the entrance of homes and are believed to bring prosperity and ward off evil spirits.",
        image_base64: null // No image in fallback mode
    };
    
    // Find a relevant mock answer based on the query
    const findMockAnswer = (userQuery) => {
        if (!userQuery) return mockKnowledgeResponse;
        
        // Convert query to lowercase for case-insensitive matching
        const lowercaseQuery = userQuery.toLowerCase();
        
        // Find the most relevant mock answer based on keyword matching
        const relevantData = MOCK_KNOWLEDGE_DATA.find(item => 
            item.question.toLowerCase().includes(lowercaseQuery) || 
            lowercaseQuery.includes(item.question.toLowerCase().split(' ')[1]) ||
            lowercaseQuery.includes('kolam')
        );
        
        return relevantData 
            ? { explanation: relevantData.answer, image_base64: relevantData.image }
            : mockKnowledgeResponse;
    };
    
    // Reset image error when response changes
    useEffect(() => {
        setImageError(false);
    }, [response]);

    // Check API availability on component mount
    useEffect(() => {
        const checkApiAvailability = async () => {
            if (useMockData) {
                setApiStatus({ checked: true, available: false, message: 'Using mock data (configured)' });
                return;
            }

            try {
                const healthCheck = await kolamService.checkApiHealth();
                setApiStatus({ 
                    checked: true, 
                    available: true, 
                    message: `API available (${healthCheck.data?.status || 'OK'})`
                });
            } catch (err) {
                console.error('API health check failed:', err);
                setApiStatus({ 
                    checked: true, 
                    available: false, 
                    message: `API unavailable: ${err.message || 'Unknown error'}`
                });
            }
        };

        checkApiAvailability();
    }, [useMockData]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setError('');
        setImageError(false);
        
        try {
            console.log('Sending knowledge query:', query);
            
            // Use mock data if configured or if we're in development mode and want to test without API
            if (useMockData) {
                console.log('Using mock data for knowledge response');
                setTimeout(() => {
                    const mockResponse = findMockAnswer(query);
                    setResponse(mockResponse);
                    setLoading(false);
                }, 1000); // Simulate network delay
                return;
            }
            
            const result = await kolamService.getKolamKnowledge(query, true);
            console.log('Knowledge response received:', result.data);
            
            // Validate the response has expected fields
            if (!result.data || typeof result.data.explanation !== 'string') {
                console.error('Invalid response format:', result.data);
                throw new Error('Invalid response format from server');
            }
            
            // Check if image_base64 exists and is valid
            if (result.data.image_base64) {
                console.log('Response includes base64 image of length:', result.data.image_base64.length);
            } else {
                console.log('No image was generated in the response');
            }
            
            setResponse(result.data);
        } catch (err) {
            console.error('Error fetching knowledge:', err);
            let errorMessage = 'Failed to fetch knowledge. Please try again.';
            
            // More detailed error messages based on the type of error
            if (err.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.error('Server responded with error:', err.response.status, err.response.data);
                if (err.response.status === 404) {
                    errorMessage = 'Knowledge API endpoint not found. Please check server configuration.';
                } else if (err.response.status === 500) {
                    errorMessage = 'Server error occurred. Please try again later.';
                } else if (err.response.status === 401 || err.response.status === 403) {
                    errorMessage = 'Authorization error. Please check your credentials.';
                }
            } else if (err.request) {
                // The request was made but no response was received
                console.error('No response received from server:', err.request);
                errorMessage = 'No response from server. Please check your internet connection.';
            }
            
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleImageError = () => {
        console.error('Failed to load image from base64 data');
        setImageError(true);
    };

    return (
        <div className="knowledge-query-container">
            <h2>Ask About Kolam</h2>
            <p>Query our knowledge base to learn more about different kolam styles and traditions.</p>
            
            <div className="api-status" style={{ 
                fontSize: '12px', 
                padding: '5px 10px', 
                borderRadius: '4px', 
                marginBottom: '10px',
                backgroundColor: apiStatus.checked 
                    ? (apiStatus.available ? '#d4edda' : '#f8d7da')
                    : '#e2e3e5',
                color: apiStatus.checked 
                    ? (apiStatus.available ? '#155724' : '#721c24')
                    : '#383d41'
            }}>
                {apiStatus.checked 
                    ? (apiStatus.available 
                        ? '✅ API Connected: ' + apiStatus.message
                        : '⚠️ API Unavailable: ' + apiStatus.message + ' (using fallback data)') 
                    : '⏳ Checking API availability...'}
            </div>
            
            <form onSubmit={handleSubmit} className="query-form">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask something about kolam..."
                    className="query-input"
                />
                <button 
                    type="submit" 
                    className="query-button"
                    disabled={loading || !query.trim()}
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>
            
            {error && <div className="query-error">{error}</div>}
            
            {response && (
                <div className="knowledge-response">
                    <h3>Results</h3>
                    <div className="response-content">
                        <p>{response.explanation}</p>
                    </div>
                    {response.image_base64 && !imageError ? (
                        <div className="response-image">
                            <h4>Generated Image</h4>
                            <img 
                                src={`data:image/jpeg;base64,${response.image_base64}`} 
                                alt="Generated Kolam" 
                                onError={handleImageError}
                            />
                        </div>
                    ) : response.image_base64 && imageError ? (
                        <div className="response-image-error">
                            <h4>Image Generation</h4>
                            <p>An image was generated but could not be displayed.</p>
                        </div>
                    ) : (
                        <div className="response-no-image">
                            <h4>No Image Generated</h4>
                            <p>No image was generated for this query.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default KnowledgeQuery;