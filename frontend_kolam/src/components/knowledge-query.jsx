import React, { useState, useEffect } from 'react';
import kolamService from '../services/kolamService';
import './knowledge-query.css';

const KnowledgeQuery = () => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [response, setResponse] = useState(null);
    const [imageError, setImageError] = useState(false);

    // Reset image error when response changes
    useEffect(() => {
        setImageError(false);
    }, [response]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setError('');
        setImageError(false);
        
        try {
            console.log('Sending knowledge query:', query);
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
            setError('Failed to fetch knowledge. Please try again.');
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