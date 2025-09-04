import React from 'react';

const NeutralSmile: React.FC = () => (
  <svg
    width="100"
    height="100"
    viewBox="0 0 100 100"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle cx="50" cy="50" r="40" fill="lightgray" />
    <circle cx="35" cy="40" r="5" fill="black" />
    <circle cx="65" cy="40" r="5" fill="black" />
    <line x1="35" y1="60" x2="65" y2="60" stroke="black" strokeWidth="3" />
  </svg>
);

export default NeutralSmile;
