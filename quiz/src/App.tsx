import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import Game from './components/Game.tsx';
import Navbar from './components/Navbar.tsx';
import Remarks from './components/remarks/Remarks.tsx';
import Statistics from './components/statistics/Statistics.tsx';
import { apiRequest } from './services/AxiosRequest.ts';
import {
  introspectToken,
  periodicRefreshAuthCheck,
  logout,
} from './services/Tokens.ts'; // Import the token functions
import './styles/App.scss';

interface Translations {
  [key: string]: string; // Dynamic keys for translations
}

// Define a union type for supported languages
type SupportedLanguage = 'en' | 'ru';

export const App: React.FC = () => {
  const [isGameStarted, setGameStarted] = useState(false);
  const [isGameStatistics, setiIsGameStatistics] = useState(false);
  const [isGameRemarks, setIsGameRemarks] = useState(false);
  const [gameModes, setGameModes] = useState<{
    music: boolean;
    arithmetic: boolean;
    trigonometry: boolean;
  }>({
    music: false,
    arithmetic: false,
    trigonometry: false,
  });
  const [gameId, setGameId] = useState<number | null>(null); // State to hold game_id
  const [gameLatency, setGameLatency] = useState<number>(21); // State for game latency
  const [translations, setTranslations] = useState<Translations>({});
  const [language, setLanguage] = useState<SupportedLanguage>('en'); // Default language
  const [userSubId, setUserSubId] = useState<string | null>(null);
  const [isAuth, setIsAuth] = useState<boolean>(false);
  const [isAdmin, setIsAdmin] = useState<boolean>(false);

  useEffect(() => {
    const fetchUserSubId = async () => {
      try {
        // Make a request to the /introspect endpoint
        const response = await introspectToken();
        // Check if the response contains the user ID
        if (response && response.data.active && response.data.sub) {
          setIsAuth(true);
          setUserSubId(response.data.sub); // Set user_id in App.tsx
          if (response.data.groups && response.data.groups.includes('admin')) {
            setIsAdmin(true); // Set admin status
          } else {
            setIsAdmin(false); // Not admin
          }
        } else {
          setUserSubId(null);
          await handleLogout();
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
    const fetchTranslations = async () => {
      try {
        const response = await apiRequest.get(
          `/api/v1/translations/${language}`,
        );
        setTranslations(response.data);
      } catch (error) {
        console.error('Error fetching translations:', error);
      }
    };

    fetchTranslations();
  }, [language]);

  useEffect(() => {
    if (process.env.REACT_APP_NODE_MODE === 'development') {
      console.log('Tokens are not refeshed in development mode');
    } else {
      const cleanup = periodicRefreshAuthCheck(30);
      return cleanup; // Cleanup function to clear the interval on unmount
    }
  }, []); // Run this effect only once when the component mounts

  const handleStartNewGame = async () => {
    setiIsGameStatistics(false);
    setIsGameRemarks(false);
    const selectedModes = Object.keys(gameModes).filter(
      (mode) => gameModes[mode as keyof typeof gameModes],
    );
    let mode: string = '';

    if (selectedModes.length === 0) {
      alert(translations.confirm_game_start_error);
      return;
    } else if (selectedModes.length === 1) {
      mode = selectedModes.join('');
    } else {
      mode = selectedModes.join(',');
    }

    try {
      const response = await apiRequest.post('/api/v1/games/create', {
        user_sub_id: userSubId, // Actual user subID
        mode: mode,
        latency_seconds: gameLatency, // Including the game latency here
      });
      if (response.status === 200) {
        setGameStarted(true);
        return response.data.id; // Return the game_id
      } else {
        alert('Failed to start a new game.');
      }
    } catch (error) {
      console.error('Error starting new game:', error);
      alert('Failed to start a new game.');
    }
  };

  const confirmStartNewGame = async () => {
    const confirmStart = window.confirm(translations.confirm_game_start);
    if (confirmStart) {
      const gameIdValue = await handleStartNewGame();
      if (gameIdValue) {
        setGameId(gameIdValue); // Set the game_id in state
      }
    }
  };

  const handleModeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name } = event.target;
    // Set only the selected mode to true and the other to false
    setGameModes({
      music: name === 'music',
      arithmetic: name === 'arithmetic',
      trigonometry: name === 'trigonometry',
    });
  };

  const handleLatencyChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setGameLatency(Number(event.target.value)); // Update latency based on selection
  };

  const handleGameStatistics = () => {
    setiIsGameStatistics(true);
  };

  const handleGameRemarks = () => {
    setIsGameRemarks(true);
  };

  const handleLogout = async () => {
    try {
      await logout();
      setUserSubId(null);
      if (
        window.location.href !==
        `${process.env.REACT_APP_FRONTEND_GAME_URL}${process.env.REACT_APP_DOMAIN_NAME}/`
      ) {
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <BrowserRouter basename="/game">
      <div className="app">
        {isAuth && (
          <Navbar
            onStartNewGame={confirmStartNewGame}
            translations={translations}
            onGameStatistics={handleGameStatistics}
            isGameStarted={isGameStarted}
            setLanguage={setLanguage}
            onGameRemarks={handleGameRemarks}
            onGameLogout={handleLogout}
            isGameStatistics={isGameStatistics}
            isGameRemarks={isGameRemarks}
            isAdmin={isAdmin}
          />
        )}
        <Routes>
          <Route
            path="/"
            element={
              !isGameStarted && isAuth ? (
                <div className="welcome-screen">
                  <h1>{translations.welcome}</h1>
                  <div>
                    <label>
                      <input
                        type="checkbox"
                        name="music"
                        checked={gameModes.music}
                        onChange={handleModeChange}
                      />
                      {translations.music}
                    </label>
                    <label>
                      <input
                        type="checkbox"
                        name="arithmetic"
                        checked={gameModes.arithmetic}
                        onChange={handleModeChange}
                      />
                      {translations.arithmetic}
                    </label>
                    <label>
                      <input
                        type="checkbox"
                        name="trigonometry"
                        checked={gameModes.trigonometry}
                        onChange={handleModeChange}
                      />
                      {translations.trigonometry}
                    </label>
                    <div>
                      <label htmlFor="latency">
                        {translations.selecting_game}
                      </label>
                      <select
                        id="latency"
                        onChange={handleLatencyChange}
                        value={gameLatency}
                      >
                        <option value={21}>
                          {translations.tweny_one_seconds}
                        </option>
                        <option value={90}>
                          {translations.ninety_seconds}
                        </option>
                        <option value={180}>
                          {translations.hundred_and_eighty_seconds}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              ) : (
                <Navigate to="/new-game" state={{ gameId, gameLatency }} />
              )
            }
          />
          <Route
            path="/new-game"
            element={
              isGameStarted && isAuth ? (
                <Game
                  modes={gameModes}
                  userSubId={userSubId}
                  gameId={gameId}
                  gameLatency={gameLatency}
                  translations={translations}
                  language={language}
                />
              ) : (
                <Navigate to="/" />
              )
            }
          />
          <Route
            path="/statistics"
            element={
              isAuth ? (
                <Statistics userSubId={userSubId} />
              ) : (
                <Navigate to="/" />
              )
            }
          />
          <Route
            path="/remarks"
            element={
              isAuth ? <Remarks userSubId={userSubId} /> : <Navigate to="/" />
            }
          />
          <Route
            path="/logout"
            element={
              isAuth ? <h2>{translations.logging_out}</h2> : <Navigate to="/" />
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
