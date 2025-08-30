import axios from 'axios';

const apiRequest = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}${process.env.REACT_APP_DOMAIN_NAME}:8002`,
  timeout: 5000,
});

apiRequest.interceptors.request.use(
  (config) => {
    // Perform actions before the request is sent here
    return config;
  },
  (error) => {
    // Handle request errors here
    return Promise.reject(error);
  },
);

// Response interceptor
apiRequest.interceptors.response.use(
  (response) => {
    // Performing actions with the response data here
    return response;
  },
  (error) => {
    // Handle errors here
    console.error('Error response:', error.response);
    // Handle specific error statuses here
    if (error.response && error.response.status === 401) {
      // Handle unauthorized access (e.g. redirect to login)
    }
    return Promise.reject(error);
  },
);

// Export the apiRequest instance
export default apiRequest;
