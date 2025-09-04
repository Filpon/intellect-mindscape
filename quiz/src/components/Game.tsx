import React, { useEffect, useState } from 'react';
import Avatar from './Avatar.tsx';
import { updateGameResults } from '../services/gameService.ts';
import {
  fetchUserModeStats,
  updateUserModeStats,
} from '../services/statsService.ts'; // updateModeUserStats
import InteractiveBassNotesSheet from './music/InteractiveBassNotesSheet.tsx';
import InteractiveTrebleNotesSheet from './music/InteractiveTrebleNotesSheet.tsx';
import { evaluateTrigonometricFunction } from '../utils/commonUtils.ts';
import MathQuestion from './arithmetic/MathQuestion.tsx';
import TrigonometryQuestion from './trigonometry/TrigonometryQuestion.tsx'; // Import the new component
import '../styles/Game.scss';
import Timer from './Timer.tsx';

type SupportedLanguage = 'en' | 'ru';

interface GameProps {
  modes: { music: boolean; arithmetic: boolean; trigonometry: boolean };
  gameId: number | null; // Accept gameId as a prop
  userSubId: string | null;
  gameLatency: number; // Accept gameLatency as a prop
  translations: { [key: string]: string };
  language: SupportedLanguage;
}

const Game: React.FC<GameProps> = ({
  modes,
  gameId,
  userSubId,
  gameLatency,
  translations,
  language,
}) => {
  const [avatarEmotion, setAvatarEmotion] = useState<
    'normal' | 'stressed' | 'rejoices'
  >('normal');
  const [currentQuestion, setCurrentQuestion] = useState<{
    question: string;
    correctAnswer: string;
  }>({ question: '', correctAnswer: '' });
  const [score, setScore] = useState({ correct: 0, incorrect: 0 });
  const [mode, setMode] = useState<
    'music' | 'arithmetic' | 'trigonometry' | null
  >(null); // Default mode
  const [selectedSheet, setSelectedSheet] = useState<'bass' | 'treble' | null>(
    null,
  ); // State for selected sheet
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [isGameOver, setIsGameOver] = useState(false); // New state for game over
  const [isUpdating, setIsUpdating] = useState(false); // Flag to control updates
  const [previousQuestion, setPreviousQuestion] = useState<string | null>(null); // State to track the last question

  useEffect(() => {
    // Randomly select mode if both are available
    if (modes.music) {
      setMode('music');
    } else if (modes.arithmetic) {
      setMode('arithmetic');
    } else if (modes.trigonometry) {
      setMode('trigonometry');
    }

    generateQuestion(); // Generate the first question
  }, [modes, mode]);

  useEffect(() => {
    // Randomize the selected sheet when the current question changes
    if (mode === 'music' && isUpdating) {
      // timeLeftRef.current === 21
      const randomSheet = Math.random() < 0.5 ? 'bass' : 'treble';
      setSelectedSheet(randomSheet);
    }
  }, [currentQuestion, mode]); // Depend on currentQuestion and mode

  useEffect(() => {
    // Initialize WebSocket connection for arithmetic mode
    if (!ws && !isGameOver) {
      const websocket = new WebSocket(
        `ws://${process.env.REACT_APP_BACKEND_DOMEN_CHAT}${process.env.REACT_APP_DOMAIN_NAME}:8005/ws`,
      );
      setWs(websocket);
    }
    if (mode === 'arithmetic' && ws && !isGameOver) {

      ws.onmessage = (event) => {
        const question = JSON.parse(event.data);
        setCurrentQuestion(question); // Set the current question from WebSocket
      };

      ws.onopen = () => {
        console.log('WebSocket connected');
      };
    }
  }, [mode, ws]);

  useEffect(() => {
    // Disconnect WebSocket when the game is over
    if (isGameOver && ws) {
      console.log('WebSocket disconnected');
      setWs(null); // Clear the WebSocket reference
      ws.close();
    }
  }, [isGameOver, ws]);

  const handleTimeUp = () => {
    setIsGameOver(true); // Set game over when time runs out
    sendResults();
  };

  const sendResults = async () => {
    const currentTime: Date = new Date(); // Current date and time
    try {
      let modeUserStatsResponse = await fetchUserModeStats(userSubId, mode);
      if (!modeUserStatsResponse) {
        modeUserStatsResponse = { correct_score: 0, incorrect_score: 0 };
      }
      await updateGameResults(gameId, score, currentTime);
      if (score.correct || score.incorrect) {
        await updateUserModeStats(
          userSubId,
          mode,
          Number(modeUserStatsResponse.correct_score) + score.correct,
          Number(modeUserStatsResponse.incorrect_score) + score.incorrect,
        );
      }
    } catch (error) {
      console.error('Error sending results:', error);
    }
  };

  const generateQuestion = () => {
    if (mode === 'music') {
      let notes;

      if (language === 'en') {
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
      } else if (language === 'ru') {
        notes = ['До', 'Ре', 'Ми', 'Фа', 'Соль', 'Ля', 'Си'];
      } else {
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
      }

      // Filter out the previous question
      const availableNotes = notes.filter((note) => note !== previousQuestion);

      if (availableNotes.length > 0) {
        // Selecting a random note from the available notes
        const randomIndex = Math.floor(Math.random() * availableNotes.length);
        const randomNote = availableNotes[randomIndex];
        const questionObject = {
          question: `What note is this?`,
          correctAnswer: randomNote,
        };
        setCurrentQuestion(questionObject);
        setPreviousQuestion(randomNote); // Update the previous question
        setIsUpdating(true);
      }
    } else if (mode === 'trigonometry') {
      const functions = ['sin', 'cos', 'tg', 'ctg'];
      const angles = Array.from({ length: 12 }, (_, i) => i * 30); // Angles from -360 to 360
      const additionalAngles = [45, 135, 225, 315, 360];
      const allAngles = [...new Set([...angles, ...additionalAngles])];
      allAngles.sort((a, b) => a - b);
      const randomFunction =
        functions[Math.floor(Math.random() * functions.length)];
      const randomAngle =
        allAngles[Math.floor(Math.random() * allAngles.length)];
      const correctAnswer = evaluateTrigonometricFunction(
        `${randomFunction} ${randomAngle}°`,
      );
      // Create the question object
      const questionObject = {
        question: `${randomFunction} ${randomAngle}°`,
        correctAnswer: correctAnswer.toString(), // Convert to string for consistency
      };
      setCurrentQuestion(questionObject);
    } else {
      console.log(`mode=${mode}`);
    }
  };

  const handleAnswer = async (
    isCorrect: boolean,
    userAnswerFloat: number | string,
  ) => {
    if (isCorrect) {
      setAvatarEmotion('rejoices');
      setScore((prev) => ({ ...prev, correct: prev.correct + 1 }));
    } else {
      setAvatarEmotion('stressed');
      setScore((prev) => ({ ...prev, incorrect: prev.incorrect + 1 }));
    }

    if (ws) {
      const message = {
        gameId: gameId, // Include the game ID
        mode: mode,
        question: currentQuestion.question, // Current question
        userAnswer: `${userAnswerFloat}`, // User's answer
        correctAnswer: currentQuestion.correctAnswer,
        isCorrect: isCorrect, // Indicate if the answer was correct
        answerTime: new Date(),
      };
      ws.send(JSON.stringify(message)); // Send the message as a JSON string
    }

    // Generate the next question after a short delay to allow for the avatar's emotion to be displayed
    setTimeout(() => {
      generateQuestion(); // Update the current question only when the user answers
    }, 100);
  };

  const renderNotesSheet = () => {
    if (mode === 'music' && selectedSheet) {
      const currentQuestionObject =
        currentQuestion && typeof currentQuestion === 'object'
          ? currentQuestion
          : { question: '', correctAnswer: '' };
      return selectedSheet === 'bass' && currentQuestion ? (
        <InteractiveBassNotesSheet
          question={currentQuestionObject}
          onAnswer={handleAnswer}
          isGameOver={isGameOver} // Pass the game over state
          language={language}
          translations={translations}
        />
      ) : (
        <InteractiveTrebleNotesSheet
          question={currentQuestionObject}
          onAnswer={handleAnswer}
          isGameOver={isGameOver} // Pass the game over state
          language={language}
          translations={translations}
        />
      );
    }
    return null; // Return null if not in music mode
  };

  return (
    <div className="game-container">
      <Timer
        initialTime={gameLatency}
        onTimeUp={handleTimeUp}
        translations={translations}
      />
      {/* <div className="timer">Time Left: {timeLeft} seconds</div> */}
      <div className="avatar-container">
        <Avatar emotion={avatarEmotion} />
      </div>
      <div className="notes-container">
        {mode === 'music' ? (
          renderNotesSheet()
        ) : mode === 'arithmetic' &&
          currentQuestion &&
          typeof currentQuestion === 'object' ? (
          <MathQuestion
            question={currentQuestion}
            onAnswer={handleAnswer}
            isGameOver={isGameOver} // Pass the game over state
            translations={translations}
          />
        ) : mode === 'trigonometry' &&
          currentQuestion &&
          typeof currentQuestion === 'object' ? (
          <TrigonometryQuestion
            question={currentQuestion}
            onAnswer={handleAnswer}
            isGameOver={isGameOver} // Pass the game over state
          />
        ) : null}
      </div>
      {isGameOver && ( // Check if the game is over
        <div className="statistics">
          <h2>{translations.game_over}</h2>
          <p>
            {translations.correct_answers}: {score.correct}
          </p>
          <p>
            {translations.incorrect_answers}: {score.incorrect}
          </p>
          <button onClick={() => (window.location.href = '/game')}>
            {translations.home}
          </button>
        </div>
      )}
    </div>
  );
};

export default Game;
