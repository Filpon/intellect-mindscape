import React, { useEffect, useState } from 'react';
import TrebleSheet from './TrebleSheet.tsx';

type SupportedLanguage = 'en' | 'ru';

interface Question {
  question: string; // The question string
  correctAnswer: string; // The correct answer
}

interface InteractiveTrebleNotesSheetProps {
  question: Question; // Question prop
  onAnswer: (isCorrect: boolean, note: string) => void;
  isGameOver: boolean; // isGameOver prop
  translations: { [key: string]: string };
  language: SupportedLanguage;
}

const InteractiveTrebleNotesSheet: React.FC<InteractiveTrebleNotesSheetProps> =
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
      setCorrectNote(question.correctAnswer); // Use the correct answer from the question object
    }, [question]);

    return (
      <div className="treble-notes-sheet">
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
        <TrebleSheet correctNote={correctNote} />
      </div>
    );
  });

export default InteractiveTrebleNotesSheet;
