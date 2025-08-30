import { createContext } from 'react';

import apiRequest from './AxiosRequest.ts';
import { checkRefreshToken, clearTokens } from './Tokens.ts';

export const AuthContext = createContext({
  authenticated: false,
  // eslint-disable-next-line
  setAuthentication: (auth: boolean) => {},
});

export const isAuthenticated = () => {
  return (
    localStorage.getItem('access_token') !== null ||
    sessionStorage.getItem('access_token') !== null
  );
};

export const periodicRefreshAuthCheck = (seconds = 120) => {
  const interval = setInterval(() => {
    if (isAuthenticated()) checkRefreshToken();
  }, seconds * 1000);
  return () => clearInterval(interval);
};

export const logout = async () => {
  const refreshToken =
    localStorage.getItem('refresh_token') ||
    sessionStorage.getItem('refresh_token') ||
    null;
  clearTokens();

  await apiRequest.post(
    '/api-auth/v1/auth/refresh',
    JSON.stringify({ token: refreshToken }),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  );
};
