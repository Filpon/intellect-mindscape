import React from 'react';

interface QuestionProps {
  question: string;
  onAnswer: (answer: string) => void;
}

const Question: React.FC<QuestionProps> = ({ question, onAnswer }) => {
  const handleAnswer = (answer: string) => {
    onAnswer(answer);
  };

  return (
    <div className="question-container">
      <div className="question-text">{question}</div>
      <div className="answer-buttons">
        <button onClick={() => handleAnswer('correct')}>Correct</button>
        <button onClick={() => handleAnswer('incorrect')}>Incorrect</button>
      </div>
    </div>
  );
};

export default Question;
