import { apiRequest } from './AxiosRequest.ts';

// Define an interface for the score object
interface Score {
  correct: number;
  incorrect: number;
}

const updateGameResults = async (
  gameId: number | null,
  score: Score,
  currentTime: object,
) => {
  try {
    const response = await apiRequest.patch('/api/v1/games/results', {
      id: gameId,
      status: 'completed',
      finished_at: currentTime,
      correct_score: score.correct,
      incorrect_score: score.incorrect,
      total_score: score.correct + score.incorrect,
    });
    return response.data; // Return the response data if needed
  } catch (error) {
    console.error('Error updating game results:', error);
    throw error; // Rethrow the error for further handling if necessary
  }
};

export { updateGameResults };
