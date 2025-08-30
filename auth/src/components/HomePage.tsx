import { FC, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { isAuthenticated } from '../utils/Auth.ts';
import '../styles/HomePage.scss';

/**
 * Functional component that represents project home page
 *
 * @returns TSX element representing the home page container
 */
export const Home: FC = () => {
  document.title = 'Events';
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the user is authenticated
    if (isAuthenticated()) {
      window.location.href = '/game';
    } else {
      // Optionally, navigate to the login page if not authenticated
      navigate('/login');
    }
  }, [navigate]);

  return <></>;
};
