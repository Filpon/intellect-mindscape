import React, { useEffect, useState } from 'react';
import BassSheet from './BassSheet.tsx';

type SupportedLanguage = 'en' | 'ru';

interface Question {
  question: string; // The question string
  correctAnswer: string; // The correct answer
}

interface InteractiveBassNotesSheetProps {
  question: Question; // Include question prop
  onAnswer: (isCorrect: boolean, note: string) => void;
  isGameOver: boolean; // Include isGameOver prop
  translations: { [key: string]: string };
  language: SupportedLanguage;
}

const InteractiveBassNotesSheet: React.FC<InteractiveBassNotesSheetProps> =
  React.memo(({ question, onAnswer, isGameOver, translations, language }) => {
    const [correctNote, setCorrectNote] = useState<string>('');

    const handleNoteClick = (note: string) => {
      if (isGameOver) return; // Prevent answering if the game is over
      const isCorrect = note === correctNote; // Check if the clicked note is correct
      onAnswer(isCorrect, note);
    };

    let constantNotes;

    if (language === 'en') {
      constantNotes = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
    } else if (language === 'ru') {
      constantNotes = ['До', 'Ре', 'Ми', 'Фа', 'Соль', 'Ля', 'Си'];
    } else {
      constantNotes = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
    }

    useEffect(() => {
      // Set the correct note based on the question prop
      setCorrectNote(question.correctAnswer);
    }, [question]);

    return (
      <div className="bass-notes-sheet">
        <h2>{translations.clicking_note}</h2>{' '}
        {/* Display the current question */}
        <div className="notes-container">
          {constantNotes.map((note) => (
            <button
              key={note}
              onClick={() => handleNoteClick(note)}
              className="note-button"
              disabled={isGameOver} // Disable button if game is over
            >
              {note}
            </button>
          ))}
        </div>
        <BassSheet correctNote={correctNote} />
      </div>
    );
  });

export default InteractiveBassNotesSheet;
