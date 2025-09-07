import { AxiosResponse } from 'axios';

import { apiRequestAuth, apiRequestAuthNonToken } from './AxiosRequest.ts';

export const fetchUsers = async () => {
  const accessToken: string | null = localStorage.getItem('access_token');
  const refreshToken: string | null = localStorage.getItem('refresh_token');

  if (accessToken && refreshToken) {
    try {
      const response: AxiosResponse = await apiRequestAuth.get(
        '/api-auth/v1/auth/users',
        {
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );
      console.log(response.data);
      return response.data;
    } catch (error) {
      console.error('Fetch users', error);
      throw error;
    }
  }

  // Optionally handle the case where tokens are not available
  throw new Error('Access token or refresh token is missing');
};

export const deleteUser = async (userId: string) => {
  const accessToken: string | null = localStorage.getItem('access_token');
  const refreshToken: string | null = localStorage.getItem('refresh_token');

  if (accessToken && refreshToken) {
    try {
      const response: AxiosResponse = await apiRequestAuth.delete(
        `/api-auth/v1/auth/users/${userId}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );
      return response.data; // Return the response data if needed
    } catch (error) {
      console.error('Delete user error', error);
      throw error; // Rethrow the error for handling in the calling function
    }
  }

  // Handle the case where tokens are not available
  throw new Error('Access token or refresh token is missing');
};

export const createFormData = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  return formData;
};

export const handleRegister = async (username: string, password: string) => {
  const formData = await createFormData(username, password);
  const response: AxiosResponse = await apiRequestAuthNonToken.post(
    '/api-auth/v1/auth/register',
    formData,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // Set the correct content type
      },
    },
  );
  if (response.status >= 200 && response.status < 300) {
    console.log('User registered successfully!');
  } else {
    const errorData = await response.data;
    console.error(`Error: ${errorData.detail}`);
  }
};

export const updateUserById = async (
  userId: string,
  newPassword: string,
): Promise<void> => {
  const response = await apiRequestAuth.put(
    `/api-auth/v1/auth/users/${userId}`,
    { new_password: newPassword },
  );
  if (response.status >= 200 && response.status < 300) {
    console.log('User was updated successfully!');
  } else {
    const errorData = await response.data;
    console.error(`Error: ${errorData.detail}`);
  }
};

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
  localStorage.removeItem('access_expires');
  sessionStorage.removeItem('access_expires');
  localStorage.removeItem('refresh_token');
  sessionStorage.removeItem('refresh_token');
  localStorage.removeItem('refresh_expires');
  sessionStorage.removeItem('refresh_expires');
};

export const logout = async () => {
  const refreshToken =
    localStorage.getItem('refresh_token') ||
    sessionStorage.getItem('refresh_token') ||
    null;
  clearTokens();

  await apiRequestAuth.post(
    '/api-auth/v1/auth/logout',
    JSON.stringify({ token: refreshToken }),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  );
};
