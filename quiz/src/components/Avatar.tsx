import '../styles/Avatar.scss';
import './reactions/PositiveSmile.tsx';

import React from 'react';

import NegativeSmile from './reactions/NegativeSmile.tsx';
import NeutralSmile from './reactions/NeutralSmile.tsx';
import PositiveSmile from './reactions/PositiveSmile.tsx';

interface AvatarProps {
  emotion: 'normal' | 'stressed' | 'rejoices';
}

const Avatar: React.FC<AvatarProps> = ({ emotion }) => {
  return (
    <div className={`avatar ${emotion}`}>
      {emotion === 'rejoices' && <PositiveSmile />}
      {emotion === 'stressed' && <NegativeSmile />}
      {emotion === 'normal' && <NeutralSmile />}
    </div>
  );
};

export default Avatar;
