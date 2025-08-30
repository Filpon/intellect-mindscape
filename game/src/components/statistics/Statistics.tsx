import React, { useEffect, useState } from 'react';
import '../../styles/Statistics.scss';
import '../../styles/Spinner.scss';
import { fetchUserStats } from '../../services/statsService.ts';
import { Spinner } from '../Spinner.tsx'; // Import the Spinner component

interface UserData {
  correct_score: string;
  incorrect_score: string;
  mode: string;
}

interface UserDataComponentProps {
  userSubId: string | null; // The user_sub_id to fetch data for
}

const Statistics: React.FC<UserDataComponentProps> = ({ userSubId }) => {
  const [userData, setUserData] = useState<UserData[]>([]); // Change to an array of UserData
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      if (!userSubId) {
        setError('User ID is not provided.');
        setLoading(false);
        return;
      }

      try {
        const response = await fetchUserStats(userSubId);
        setUserData(response); // Set the response directly to userData
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to fetch user data.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userSubId]); // Add userSubId as a dependency

  if (loading) {
    return <Spinner />; // Use the Spinner component while loading;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {userData !== null && userData.length > 0 ? (
        <ul>
          {userData.map((data, index) => (
            <li key={index}>
              <strong>Mode:</strong> {data.mode} <br />
              <strong>Correct Answers:</strong> {data.correct_score} <br />
              <strong>Incorrect Answers:</strong> {data.incorrect_score}
            </li>
          ))}
        </ul>
      ) : (
        <div>No user data found</div>
      )}
    </div>
  );
};

export default Statistics;
