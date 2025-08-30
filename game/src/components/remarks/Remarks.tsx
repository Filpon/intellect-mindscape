import React, { useEffect, useState } from 'react';
import { fetchUserRemarks } from '../../services/remarksService.ts';
import { Spinner } from '../Spinner.tsx'; // Import the Spinner component
import '../../styles/Spinner.scss';

interface UserData {
  mode: string;
  modeRecomendation: string;
  questionVars: string[];
  user_sub_id: string;
}

interface UserDataComponentProps {
  userSubId: string | null; // The user_sub_id to fetch data for
}

const Remarks: React.FC<UserDataComponentProps> = ({ userSubId }) => {
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
        const response = await fetchUserRemarks(userSubId);
        setUserData(response); // Set the response directly as an array
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to fetch user data.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userSubId]); // userSubId as a dependency

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
              <strong>Mode:</strong> {data.mode}
              <br />
              <strong>Recommendation:</strong> {data.modeRecomendation}
              <br />
            </li>
          ))}
        </ul>
      ) : (
        <div>No user data found</div>
      )}
    </div>
  );
};

export default Remarks;
