import React, { useState } from 'react';
import '../../styles/MathCaptcha.scss';

const MathCaptcha: React.FC = () => {
  const [firstNum] = useState(Math.floor(Math.random() * 10));
  const [secondNum] = useState(Math.floor(Math.random() * 10));
  const [userAnswer, setUserAnswer] = useState<number | ''>('');
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const handleSubmit = () => {
    const correctAnswer = firstNum + secondNum;
    setIsCorrect(userAnswer === correctAnswer);
  };

  return (
    <div className="math-captcha">
      <h3>
        What is {firstNum} + {secondNum}?
      </h3>
      <input
        type="number"
        value={userAnswer}
        onChange={(e) => setUserAnswer(Number(e.target.value))}
      />
      <button onClick={handleSubmit}>Submit</button>
      {isCorrect !== null && (
        <div className={`result ${isCorrect ? 'correct' : 'incorrect'}`}>
          {isCorrect ? 'Correct!' : 'Incorrect!'}
        </div>
      )}
    </div>
  );
};

export default MathCaptcha;
