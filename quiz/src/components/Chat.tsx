import React, { useEffect, useState, useMemo } from 'react';
import './Chat.scss';

interface ChatProps {
  mode: 'music' | 'math';
  onAnswer: (isCorrect: boolean) => void;
}

const Chat: React.FC<ChatProps> = ({ mode, onAnswer }) => {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState<string>('');

  const ws = useMemo(
    () => new WebSocket(`ws://${process.env.REACT_APP_BACKEND_DOMEN_CHAT}${process.env.REACT_APP_DOMAIN_NAME}:8005/ws`),
    [],
  );

  useEffect(() => {
    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    return () => {
      ws.close();
    };
  }, [ws]);

  const sendMessage = () => {
    if (input) {
      const isCorrect = eval(input); // Evaluate the input for math mode
      onAnswer(isCorrect); // Call the onAnswer function with the result
      setInput('');
    }
  };

  return (
    <div className="chat">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index}>{msg}</div>
        ))}
      </div>
      {mode === 'math' && (
        <>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </>
      )}
    </div>
  );
};

export default Chat;
