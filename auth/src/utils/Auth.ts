import { createContext, Dispatch, SetStateAction } from 'react';

import apiRequest from './AxiosRequest.ts';
import { checkTokens, clearTokens } from './Tokens.ts';

import Cookies from 'js-cookie';

export const AuthContext = createContext({
  authenticated: false,
  // eslint-disable-next-line
  setAuthentication: (auth: boolean) => {},
});

type IntrospectResponse = {
  active?: boolean;
};

export const isAuthenticated = async (): Promise<boolean> => {
  const accessToken = Cookies.get('access_token');

  if (!accessToken) {
    return false;
  }

  try {
    const response = await apiRequest.post<IntrospectResponse>(
      '/api/v1/auth/introspect',
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
      window.location.href = "/"; 
      return false;
    }

    return true;
  } catch (error) {
    console.error('Token introspection failed:', error);
    await logout();
    window.location.href = "/"; 
    return false;
  }
};

export const periodicRefreshAuthCheck = (
  seconds = 60,
  setAuthentication?: Dispatch<SetStateAction<boolean>>,
) => {
  const interval = setInterval(async () => {
    const authenticated = await isAuthenticated(); setAuthentication?.(authenticated);
    if (authenticated) {
      await checkTokens();
    }
  }, seconds * 1000);
  return () => clearInterval(interval);
};

export const logout = async () => {
  const refreshToken = Cookies.get('refresh_token');
  await apiRequest.post(
    '/api/v1/auth/logout',
    JSON.stringify({ token: refreshToken }),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  );
  clearTokens();
};
