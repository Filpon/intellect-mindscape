import React, { useEffect, useState } from 'react';
import { fetchGames } from '../services/gameService.ts';
import Spinner from './Spinner.tsx';
import '../styles/GameSessionList.scss';
import NavBar from './NavBar.tsx';
import { handleNavigate } from '../utils/commonUtils.ts';

interface Game {
  id: number;
  mode_name: string;
  user_sub_id: string;
  status: string;
  correct_score: number;
  total_score: number;
}

const GameSessionList: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState<boolean>(false); // Loading state

  const fetchGamesList = async () => {
    try {
      setLoading(true);
      const data = await fetchGames();
      // Ensure data is an array before setting state
      if (Array.isArray(data)) {
        setGames(data);
      } else {
        console.error('Fetched data is not an array:', data);
      }
    } catch (error) {
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false); // Set loading to false when fetching ends
    }
  };

  useEffect(() => {
    fetchGamesList();
  }, []);

  return (
    <div>
      <NavBar onNavigate={handleNavigate} />
      <h2>Game Session List</h2>
      {loading ? ( // Show loading spinner if loading is true
        <Spinner />
      ) : (
        <ul>
          {games.length > 0 ? (
            games.map((game) => (
              <li key={game.id}>
                ID: {game.id} - User ID: {game.user_sub_id} - Total score:{' '}
                {game.total_score} - Correct score: {game.correct_score} - Mode:{' '}
                {game.mode_name} - Status: {game.status}
              </li>
            ))
          ) : (
            <li>No games found.</li>
          )}
        </ul>
      )}
    </div>
  );
};

export default GameSessionList;
