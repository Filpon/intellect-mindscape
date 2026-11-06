/* eslint-disable max-lines*/
// eslint-disable-next-line
import { Dispatch, SetStateAction } from 'react';
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
  Cookies.set('access_token', data.access_token, {
    path: '/',
    maxAge: data.expires_in,
  });
  const accessExpires = new Date(
    Date.now() / 1000 + data.expires_in * 1000,
  ).toUTCString();
  Cookies.set('access_expires', accessExpires, {
    path: '/',
    maxAge: data.expires_in,
  });
  Cookies.set('refresh_token', data.refresh_token, {
    path: '/',
    maxAge: data.refresh_expires_in,
  });
  const refreshExpires = new Date(
    Date.now() / 1000 + data.refresh_expires_in * 1000,
  ).toUTCString();
  Cookies.set('refresh_expires', refreshExpires, {
    path: '/',
    maxAge: data.refresh_expires_in,
  });
};

export const checkTokens = async () => {
  const refreshToken = Cookies.get('refresh_token');
  try {
    const response: AxiosResponse = await apiRequestAuth.post(
      '/api-auth/v1/auth/refresh',
      JSON.stringify({
        token: refreshToken,
      }),
      {
        headers: {
          'Content-Type': 'application/json',
        },
      },
    );
    if (response.status >= 400) {
      const error = await response.data;
      throw error.detail;
    }
    const data = await response.data;
    clearTokens();
    storeTokens(data);
  } catch (error) {
    console.error(error);
  }
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
            token: refreshToken,
          }),
        );
        if (response.status >= 400) {
          const error = await response.data;
          throw error.detail;
        }
        const data = await response.data;
        storeTokens(data);
      } catch (error) {
        await logout();
        window.location.href = '/';
        console.error(error);
      }
    }
  }
};

type IntrospectResponse = {
  active?: boolean;
};

export const isAuthenticated = async (): Promise<boolean> => {
  const accessToken = Cookies.get('access_token');

  if (!accessToken) {
    return false;
  }

  try {
    const response = await apiRequestAuth.post<IntrospectResponse>(
      '/api-auth/v1/auth/introspect',
      { token: accessToken },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      },
    );

    const isReturnedAccessTokenActive = response.data?.active;

    if (!isReturnedAccessTokenActive) {
      console.error('Token is not active');
      await logout();
      window.location.href = '/';
      return false;
    }

    return true;
  } catch (error) {
    console.error('Token introspection failed:', error);
    await logout();
    window.location.href = '/';
    return false;
  }
};

export const periodicRefreshAuthCheck = (
  seconds = 60,
  setAuthentication?: Dispatch<SetStateAction<boolean>>,
) => {
  const interval = setInterval(async () => {
    const authenticated = await isAuthenticated();
    setAuthentication?.(authenticated);
    if (authenticated) {
      await checkTokens();
    }
  }, seconds * 1000);
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
        token: refreshToken,
      }),
    );
    // Clear tokens from local storage
  } catch (error) {
    console.error(error);
  } finally {
    clearTokens();
  }
};
