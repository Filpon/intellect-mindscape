import { apiRequest } from './AxiosRequest.ts';

const fetchUserStats = async (userSubId: string) => {
  try {
    const response = await apiRequest.get(`/api/v1/stats/all/${userSubId}`);
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error fetching user remarks:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

const fetchUserModeStats = async (
  userSubId: string | null,
  mode: string | null,
) => {
  try {
    const response = await apiRequest.get(`/api/v1/stats/${userSubId}/${mode}`);
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error fetching user stats:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

const createUserModeStats = async (
  userSubId: string | null,
  mode: string | null,
) => {
  try {
    const response = await apiRequest.post(
      `/api/v1/stats/${userSubId}/${mode}`,
    );
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error fetching user stats:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

const updateUserModeStats = async (
  userSubId: string | null,
  mode: string | null,
  correctScore: number,
  incorrectScore: number,
) => {
  try {
    const response = await apiRequest.patch(
      `/api/v1/stats/${userSubId}/${mode}`,
      {
        correct_score: correctScore,
        incorrect_score: incorrectScore,
      },
    );
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error updating mode user stats:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

export {
  fetchUserStats,
  fetchUserModeStats,
  createUserModeStats,
  updateUserModeStats,
};
