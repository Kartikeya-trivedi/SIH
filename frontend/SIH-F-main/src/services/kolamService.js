import apiClient from './api';

const kolamService = {
    /**
     * Predict the type of Kolam from an uploaded image
     * @param {File} imageFile - The image file to upload
     * @returns {Promise} - Promise with prediction response
     */
    predictKolam: async (imageFile) => {
        try {
            console.log('Uploading image for prediction:', imageFile.name, 'Size:', imageFile.size);
            const formData = new FormData();
            formData.append('file', imageFile);
            
            // Log what's being sent in the form data
            for (let [key, value] of formData.entries()) {
                console.log(`FormData: ${key} = ${value instanceof File ? value.name : value}`);
            }
            
            const response = await apiClient.post('/api/v1/kolam/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            console.log('Prediction response:', response);
            
            // Ensure the confidence value is a number
            if (response.data && response.data.confidence) {
                // Convert from percentage back to decimal if needed (backend sends as percentage)
                const confidence = parseFloat(response.data.confidence);
                if (!isNaN(confidence)) {
                    // If backend is sending as percentage (e.g., 95.5), convert to decimal (0.955)
                    response.data.confidence = confidence > 1 ? confidence / 100 : confidence;
                } else {
                    // Fallback if conversion fails
                    response.data.confidence = 0;
                }
            }
            
            return response;
        } catch (error) {
            console.error('Error in prediction:', error.response?.status, error.response?.data || error.message);
            throw error;
        }
    },

    /**
     * Query the knowledge base about Kolam and optionally generate an image
     * @param {string} query - The query about Kolam
     * @param {boolean} generateImage - Whether to generate an image
     * @returns {Promise} - Promise with knowledge response
     */
    getKolamKnowledge: async (query, generateImage = false) => {
        try {
            console.log('Knowledge query:', query, 'Generate image:', generateImage);
            
            const response = await apiClient.post('/api/v1/kolam/knowledge', {
                query,
                generate_image: generateImage,
            });
            
            console.log('Knowledge response received with status:', response.status);
            
            // Validate image_base64 if it exists
            if (response.data && response.data.image_base64) {
                const base64Length = response.data.image_base64.length;
                console.log(`Base64 image received (${base64Length} characters)`);
                
                // Check if the base64 string looks valid
                if (base64Length < 100) {
                    console.warn('Warning: Base64 image data appears too short');
                }
            } else if (response.data) {
                console.log('Response received without image data');
            }
            
            return response;
        } catch (error) {
            console.error('Error fetching knowledge:', error.response?.status, error.response?.data || error.message);
            throw error;
        }
    },
};

export default kolamService;