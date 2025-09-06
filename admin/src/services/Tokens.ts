/* eslint-disable max-lines*/
// eslint-disable-next-line
import { AxiosResponse } from 'axios';

import { apiRequestAuth } from './AxiosRequest.ts';

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('access_expires');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('refresh_expires');
  sessionStorage.removeItem('access_token');
  sessionStorage.removeItem('access_expires');
  sessionStorage.removeItem('refresh_token');
  sessionStorage.removeItem('refresh_expires');
};

const storeTokens = (data: any) => {
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('access_expires', Date.now() / 1000 + data.expires_in);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem(
    'refresh_expires',
    Date.now() / 1000 + data.refresh_expires_in,
  );
  sessionStorage.setItem('access_token', data.access_token);
  sessionStorage.setItem('access_expires', Date.now() / 1000 + data.expires_in);
  sessionStorage.setItem('refresh_token', data.refresh_token);
  sessionStorage.setItem(
    'refresh_expires',
    Date.now() / 1000 + data.refresh_expires_in,
  );
};

export const checkRefreshToken = async () => {
  const refreshExpires: string | null =
    sessionStorage.getItem('refresh_expires') ||
    localStorage.getItem('refresh_expires') ||
    null;
  const refreshToken: string | null =
    sessionStorage.getItem('refresh_token') ||
    localStorage.getItem('refresh_token') ||
    null;
  const now = Date.now() / 1000;

  if (refreshToken && refreshExpires) {
    if (now > parseFloat(refreshExpires) - 180) {
      try {
        const response: AxiosResponse = await apiRequestAuth.post(
          '/api-auth/v1/auth/refresh',
          JSON.stringify({
            token: refreshToken
          }),
        );
        if (response.status >= 400) {
          const error = await response.data;
          throw error.detail;
        }
        const data = await response.data;
        storeTokens(data);
      } catch (error) {
        console.error(error);
      }
    }
  }
};

export const isAuthenticated = () => {
  return (
    localStorage.getItem('access_token') !== null ||
    sessionStorage.getItem('access_token') !== null
  );
};

export const periodicRefreshAuthCheck = (seconds = 120) => {
  const interval = setInterval(async () => {
    if (isAuthenticated()) {
      try {
        await checkRefreshToken(); // Ensure checkRefreshToken is awaited
      } catch (error) {
        console.error('Error during token refresh:', error);
      }
    }
  }, seconds * 1000);
  // Return cleanup function to clear the interval
  return () => clearInterval(interval);
};

export const introspectToken = async () => {
  try {
    const response: AxiosResponse = await apiRequestAuth.post(
      '/api-auth/v1/auth/introspect',
    );
    return response;
  } catch (error) {
    console.error(error);
  }
};

export const logout = async () => {
  const refreshToken =
    localStorage.getItem('refresh_token') ||
    sessionStorage.getItem('refresh_token') ||
    '';
  try {
    await apiRequestAuth.post(
      '/api-auth/v1/auth/logout',
      JSON.stringify({
        token: refreshToken
      }),
    );
  } catch (error) {
    console.error(error);
  } finally {
    clearTokens();
  }
};
