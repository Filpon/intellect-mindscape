import axios from 'axios';

import Cookies from 'js-cookie';

const apiRequestAuth = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}${process.env.REACT_APP_DOMAIN_NAME}:8002`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json', // Set the Content-Type header
  },
});

const apiRequestAuthNonToken = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}${process.env.REACT_APP_DOMAIN_NAME}:8002`,
  timeout: 5000,
});

const apiRequestGame = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_GAME_URL}${process.env.REACT_APP_DOMAIN_NAME}:8004`,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json', // Set the Content-Type header
  },
});

apiRequestAuth.interceptors.request.use(
  (config) => {
    const token = Cookies.get('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

apiRequestGame.interceptors.request.use(
  (config) => {
    const token = Cookies.get('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export { apiRequestAuth, apiRequestAuthNonToken, apiRequestGame };
