import axios from 'axios';

const apiRequest = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_GAME_URL}${process.env.REACT_APP_DOMAIN_NAME}:8004`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json', // Set the Content-Type header
  },
});

const apiRequestAuth = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}${process.env.REACT_APP_DOMAIN_NAME}:8002`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json', // Set the Content-Type header
  },
});

apiRequest.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Interceptor to add the Authorization token to requests
apiRequestAuth.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem('access_token') ||
      sessionStorage.getItem('access_token') ||
      null;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export { apiRequest, apiRequestAuth };
