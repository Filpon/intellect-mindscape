// useWebSocket.ts
import { useEffect, useRef, useState } from 'react';

const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<string[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    socketRef.current = new WebSocket(url);

    socketRef.current.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    socketRef.current.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    socketRef.current.onerror = (event) => {
      // Create a new Error object with a custom message
      const error = new Error(`WebSocket error: ${event.type}`);
      setError(error);
      console.error('WebSocket error:', event);
    };

    socketRef.current.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    return () => {
      socketRef.current?.close();
    };
  }, [url]);

  const sendMessage = (message: string) => {
    if (socketRef.current && isConnected) {
      socketRef.current.send(message);
    } else {
      console.error('WebSocket is not connected');
    }
  };

  return { messages, error, isConnected, sendMessage };
};

export default useWebSocket;
