import { FC, useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

import { isAuthenticated } from '../utils/Auth.ts';
import '../styles/HomePage.scss';

/**
 * Functional component that represents project home page
 *
 * @returns TSX element representing the home page container
 */
export const Home: FC = () => {
  document.title = 'Auth';
  const navigate = useNavigate();
  const [authenticated, setAuthenticated] = useState(false);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const checkAuthentication = async () => {
      const result = await isAuthenticated();

      if (!cancelled) {
        setAuthenticated(result);
        setChecked(true);
      }
    };

    void checkAuthentication();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    // Check if the user is authenticated
    if (authenticated) {
      window.location.href = '/game';
    } else {
      // Optionally, navigate to the login page if not authenticated
      navigate('/login');
    }
  }, [navigate]);

  if (!checked) {
    return (
      <Container className="home-page-container">
        Authorization check
      </Container>
    );
  }

  return <></>;
};
