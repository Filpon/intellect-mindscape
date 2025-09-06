import React from 'react';
import '../styles/Spinner.scss';

const Spinner: React.FC = () => {
  return (
    <div className="spinner">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="50"
        height="50"
        viewBox="0 0 50 50"
      >
        <circle
          className="path"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          strokeWidth="5"
        />
      </svg>
    </div>
  );
};

export default Spinner;
