import React, { useState } from 'react';
import '../../styles/arithmetic/MathQuestion.scss';

interface MathQuestionProps {
  question: { question: string; correctAnswer: string };
  onAnswer: (isCorrect: boolean, userAnswer: number) => void;
  isGameOver: boolean; // Add isGameOver prop
  translations: { [key: string]: string };
}

const MathQuestion: React.FC<MathQuestionProps> = ({
  question,
  onAnswer,
  isGameOver,
  translations,
}) => {
  const [userAnswer, setUserAnswer] = useState<string>('');

  const handleSubmit = () => {
    if (isGameOver) return; // Prevent answering if the game is over
    const userAnswerFloat = parseFloat(userAnswer);
    const correctAnswerFloat = parseFloat(question.correctAnswer);
    const isCorrect: boolean =
      !isNaN(userAnswerFloat) &&
      !isNaN(correctAnswerFloat) &&
      userAnswerFloat === correctAnswerFloat;
    onAnswer(isCorrect, userAnswerFloat);
    setUserAnswer(''); // Reset user answer after submission
  };

  return (
    <div className="math-question">
      <p>{question.question}</p>
      <input
        type="number"
        value={userAnswer}
        onChange={(e) => setUserAnswer(e.target.value)}
        placeholder="Your answer"
        disabled={isGameOver} // Disable input if game is over
      />
      <button
        onClick={handleSubmit}
        disabled={isGameOver}
        className={isGameOver ? 'disabled-button' : ''}
      >
        {translations.submit}
      </button>
    </div>
  );
};

export default MathQuestion;
