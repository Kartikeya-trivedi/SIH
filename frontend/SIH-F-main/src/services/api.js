import axios from 'axios';

// Create an instance of axios with default settings
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 seconds
});

// Add a request interceptor for authentication if needed later
apiClient.interceptors.request.use(
    (config) => {
        // Log all API requests during development
        console.log(`API Request: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`, config.data || config.params);
        
        // You can add auth tokens here if needed
        // const token = localStorage.getItem('token');
        // if (token) {
        //     config.headers.Authorization = `Bearer ${token}`;
        // }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log(`API Response: ${response.status} from ${response.config.url}`, response.data);
        return response;
    },
    (error) => {
        // Handle different error statuses here
        console.error('API Error:', error);
        
        const { response } = error;
        if (response && response.status === 401) {
            // Handle unauthorized error
            console.error('Unauthorized access');
            // Maybe redirect to login
        } else if (response && response.status === 500) {
            // Handle server error
            console.error('Server error:', response.data);
        } else if (!response) {
            // Handle network error
            console.error('Network error - no response from server');
        }
        return Promise.reject(error);
    }
);

export default apiClient;