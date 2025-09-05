// TrigonometryQuestion.tsx
import React from 'react';
import { evaluateTrigonometricFunction } from '../../utils/commonUtils.ts';

interface TrigonometryQuestionData {
  question: string; // The question string
  correctAnswer: string; // The correct answer string
}

interface TrigonometryQuestionProps {
  question: TrigonometryQuestionData; // Change to match MathQuestion
  onAnswer: (isCorrect: boolean, answer: number) => void;
  isGameOver: boolean;
}

const TrigonometryQuestion: React.FC<TrigonometryQuestionProps> = ({
  question,
  onAnswer,
  isGameOver,
}) => {
  const possibleAnswers = [
    '-√3/3',
    '-√3',
    -1,
    '-√3/2',
    '-√2/2',
    -1 / 2,
    '-1/√3',
    0,
    '1/√3',
    1 / 2,
    '√3/3',
    '√2/2',
    '√3/2',
    1,
    '√3',
    'not exists',
  ];

  const areAlmostEqual = (
    numberFirst: number,
    numberSecond: number,
    epsilon = 0.1,
  ) => {
    return Math.abs(numberFirst - numberSecond) < epsilon;
  };

  const handleAnswerClick = (answer: any) => {
    if (isGameOver) return; // Prevent answering if the game is over
    let sliceNumber: number = 1;
    let correctAnswer = evaluateTrigonometricFunction(question.question);
    if (answer === 'not exists') answer = Infinity;
    if (typeof correctAnswer === 'number' && Math.abs(correctAnswer) > 1000000)
      correctAnswer = Infinity;
    if (typeof answer === 'string' && answer.includes('√')) {
      if (answer.indexOf('√') > 1) {
        if (answer.includes('-')) {
          answer = -1 / Math.sqrt(3);
        } else {
          answer = 1 / Math.sqrt(3);
        }
      } else {
        if (answer.includes('-')) {
          sliceNumber = 2;
          answer = answer.slice(sliceNumber);
          if (answer.includes('/')) {
            const [numerator, denominator] = answer.split('/').map(Number);
            answer = -Math.sqrt(numerator) / denominator;
          } else {
            answer = -Math.sqrt(answer);
          }
        } else {
          answer = answer.slice(sliceNumber);
          if (answer.includes('/')) {
            const [numerator, denominator] = answer.split('/').map(Number);
            answer = Math.sqrt(numerator) / denominator;
          } else {
            answer = Math.sqrt(answer);
          }
        }
      }
    }

    if (
      typeof answer === 'number' &&
      typeof correctAnswer === 'number' &&
      answer !== Infinity
    ) {
      onAnswer(areAlmostEqual(answer, correctAnswer), answer);
    } else {
      onAnswer(answer === correctAnswer, answer);
    }
  };

  return (
    <div>
      <h2>{question.question}</h2>
      <div>
        {possibleAnswers.map((answer, index) => (
          <button
            key={index}
            onClick={() => handleAnswerClick(answer)}
            disabled={isGameOver}
          >
            {answer}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TrigonometryQuestion;
