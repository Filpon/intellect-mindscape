import { apiRequestGame } from './AxiosRequest.ts';
import { AxiosResponse } from 'axios';

export const fetchGames = async () => {
  const accessToken: string | null = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
  const refreshToken: string | null = localStorage.getItem('refresh_token') ||  sessionStorage.getItem('refresh_token');

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
