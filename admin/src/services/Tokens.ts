/* eslint-disable max-lines*/
// eslint-disable-next-line
import { AxiosResponse } from 'axios';

import Cookies from 'js-cookie';

import { apiRequestAuth } from './AxiosRequest.ts';

export const clearTokens = () => {
  Cookies.remove('access_token', { path: '/' });
  Cookies.remove('access_expires', { path: '/' });
  Cookies.remove('refresh_token', { path: '/' });
  Cookies.remove('refresh_expires', { path: '/' });
};

const storeTokens = (data: any) => {
  Cookies.set('access_token', data.access_token, { path: '/', maxAge: data.expires_in });
  const accessExpires = new Date(Date.now() / 1000 + data.expires_in * 1000).toUTCString();
  Cookies.set('access_expires', accessExpires, { path: '/', maxAge: data.expires_in });
  Cookies.set('refresh_token', data.refresh_token, { path: '/', maxAge: data.refresh_expires_in });
  const refreshExpires = new Date(Date.now() / 1000 + data.refresh_expires_in * 1000).toUTCString();
  Cookies.set('refresh_expires', refreshExpires, { path: '/', maxAge: data.refresh_expires_in });
};

export const checkRefreshToken = async () => {
  const refreshExpires = Cookies.get('refresh_expires');
  const refreshToken = Cookies.get('refresh_token');
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
  return Cookies.get('access_token') !== undefined;
};

export const periodicRefreshAuthCheck = (seconds = 60) => {
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
  const refreshToken = Cookies.get('refresh_token');
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
