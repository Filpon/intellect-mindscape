import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.scss';

interface Translations {
  [key: string]: string; // Dynamic keys for translations
}

interface NavbarProps {
  onStartNewGame: () => void;
  onGameStatistics: () => void;
  onGameRemarks: () => void;
  onGameLogout: () => void;
  isGameStarted: boolean; // Add gameStarted prop
  isGameStatistics: boolean;
  isGameRemarks: boolean;
  setLanguage: (lang: 'en' | 'ru') => void; // New prop for setting language
  translations: Translations;
  isAdmin: boolean;
}

const Navbar: React.FC<NavbarProps> = ({
  onStartNewGame,
  onGameStatistics,
  onGameRemarks,
  onGameLogout,
  isGameStarted,
  isGameStatistics,
  isGameRemarks,
  translations,
  setLanguage,
  isAdmin,
}) => {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        {!isGameStarted && (
          <li className="navbar-item">
            <button onClick={() => setLanguage('en')}>EN</button>
            <button onClick={() => setLanguage('ru')}>RU</button>
          </li>
        )}

        {(isGameStarted || isGameStatistics || isGameRemarks) && (
          <li className="navbar-item">
            <Link to="/game" onClick={() => (window.location.href = '/game')}>
              {translations.home}
            </Link>
          </li>
        )}

        {!isGameStarted && !isGameStatistics && !isGameRemarks && (
          <li className="navbar-item">
            <Link to="/new-game" onClick={onStartNewGame}>
              {translations.new}
            </Link>
          </li>
        )}
        <li className="navbar-item">
          <Link to="/statistics" onClick={onGameStatistics}>
            {translations.statistics_page}
          </Link>
        </li>
        <li className="navbar-item">
          <Link to="/remarks" onClick={onGameRemarks}>
            {translations.recommendations_page}
          </Link>
        </li>
        {isAdmin && ( // Conditionally render the admin button
          <li className="navbar-item">
            <Link to="/admin" onClick={() => (window.location.href = '/admin')}>
              {translations.admin}
            </Link>
          </li>
        )}
        <li className="navbar-item">
          <Link to="/logout" onClick={onGameLogout}>
            {translations.logging_out}
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
