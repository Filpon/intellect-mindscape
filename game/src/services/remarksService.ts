import { apiRequest } from './AxiosRequest.ts';

// Define an interface for the score object
const fetchUserRemarks = async (subUserId: string) => {
  try {
    const response = await apiRequest.get(`/api/v1/remarks/${subUserId}`);
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error fetching user remarks:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

export { fetchUserRemarks };
