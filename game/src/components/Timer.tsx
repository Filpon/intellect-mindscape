import React from 'react';
import { useTimer } from 'react-timer-hook';

interface TimerProps {
  initialTime: number; // in seconds
  onTimeUp: () => void; // Callback function to notify when time is up
  translations: { [key: string]: string };
}

const Timer: React.FC<TimerProps> = React.memo(
  ({ initialTime, onTimeUp, translations }) => {
    const time = new Date();
    time.setSeconds(time.getSeconds() + initialTime); // Set the expiry time based on initialTime

    const { minutes, seconds } = useTimer({
      expiryTimestamp: time,
      onExpire: onTimeUp,
    });

    return (
      <div className="timer">
        <h1>{translations.enjoying_game}</h1>
        <p>{translations.game_duration}</p>
        <div style={{ fontSize: '100px' }}>
          {initialTime >= 60 ? (
            <>
              <span>
                {minutes} {translations.minutes} : {seconds}{' '}
                {translations.minutes}
              </span>
            </>
          ) : (
            <>
              <span>
                {seconds} {translations.seconds}
              </span>
            </>
          )}
        </div>
      </div>
    );
  },
);

export default Timer;
