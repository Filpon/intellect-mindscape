import React from 'react';

const PositiveSmile: React.FC = () => (
  <svg
    width="100"
    height="100"
    viewBox="0 0 100 100"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle cx="50" cy="50" r="40" fill="yellow" />
    <circle cx="35" cy="40" r="5" fill="black" />
    <circle cx="65" cy="40" r="5" fill="black" />
    <path d="M35 60 Q50 75, 65 60" stroke="black" strokeWidth="3" fill="none" />
  </svg>
);

export default PositiveSmile;
