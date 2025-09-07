import React, { useState, useEffect } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import AdminPanel from './components/AdminPanel.tsx';
import UserList from './components/UserList.tsx';
import GameSessionList from './components/GameSessionList.tsx';
import {
  introspectToken,
  periodicRefreshAuthCheck,
  logout,
} from './services/Tokens.ts';

const App: React.FC = () => {
  const [userSubId, setUserSubId] = useState<string | null>(null);
  const [isAuth, setIsAuth] = useState<boolean>(false);
  const [__, setIsAdmin] = useState<boolean>(false);

  useEffect(() => {
    const fetchUserSubId = async () => {
      try {
        // Make request to the /introspect endpoint
        const response = await introspectToken();
        // Check if the response contains the user ID
        if (response && response.data.active && response.data.sub) {
          setIsAuth(true);
          setUserSubId(response.data.sub); // Set user_id in App.tsx
          if (response.data.groups && response.data.groups.includes('admin')) {
            console.log('Admin mode');
          } else {
            await handleLogout();
          }
        } else {
          await handleLogout();
          console.log('Token is not valid');
        }
      } catch (error) {
        console.error('Error fetching user ID:', error);
      }
    };

    if (process.env.REACT_APP_NODE_MODE !== 'development') {
      fetchUserSubId();
    } else {
      setIsAuth(true);
    }
  }, []);

  useEffect(() => {
    if (process.env.REACT_APP_NODE_MODE === 'development') {
      console.log('Tokens are not refeshed in development mode');
    } else {
      const cleanup = periodicRefreshAuthCheck(30);
      return cleanup; // Cleanup function to clear the interval on unmount
    }
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      setUserSubId(null);
      setIsAuth(false);
      setIsAdmin(false);
      if (
        window.location.href !==
        `${process.env.REACT_APP_ADMIN_URL}${process.env.REACT_APP_DOMAIN_NAME}/`
      ) {
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <BrowserRouter basename="/admin">
      <Routes>
        <Route
          path="/"
          element={isAuth ? <AdminPanel /> : <Navigate to="/" />}
        />
        <Route
          path="/users"
          element={isAuth ? <UserList currentUserId={userSubId} /> : <Navigate to="/" />}
        />
        <Route
          path="/games"
          element={isAuth ? <GameSessionList /> : <Navigate to="/" />}
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
