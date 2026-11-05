import { apiRequestGame } from './AxiosRequest.ts';
import { AxiosResponse } from 'axios';
import Cookies from 'js-cookie';

export const fetchGames = async () => {
  const accessToken = Cookies.get('access_token');
  const refreshToken = Cookies.get('refresh_token');

  if (accessToken && refreshToken) {
    try {
      const response: AxiosResponse = await apiRequestGame.get(
        '/api/v1/games/results',
        {
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );
      return response.data;
    } catch (error) {
      console.error('Fetch games', error);
      throw error;
    }
  }

  // Optionally handle the case where tokens are not available
  throw new Error('Access token or refresh token is missing');
};
