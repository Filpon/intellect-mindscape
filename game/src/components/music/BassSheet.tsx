import React from 'react';

interface BassSheetProps {
  correctNote: string;
}

interface NotePosition {
  x: number;
  y: number;
} // Define the structure of the position

const BassSheet: React.FC<BassSheetProps> = ({ correctNote }) => {
  // Define the note positions
  const aNoteYValue: number = Math.random() < 0.5 ? 25 : 95;
  const bNoteYValue: number = Math.random() < 0.5 ? 15 : 85;

  const notePosition = (note: string) => {
    switch (note) {
      case 'C':
      case 'До':
        return { x: 55, y: 75 }; // Between 3rd and 4th string
      case 'D':
      case 'Ре':
        return { x: 55, y: 65 }; // On the 3rd string
      case 'E':
      case 'Ми':
        return { x: 55, y: 55 }; // Between 2nd and 3rd string
      case 'F':
      case 'Фа':
        return { x: 55, y: 45 }; // Randomly on 2nd string or below 5th string
      case 'G':
      case 'Соль':
        return { x: 55, y: 35 }; // Randomly between 1st and 2nd string or on 5th string
      case 'A':
      case 'Ля':
        return { x: 55, y: aNoteYValue }; // Randomly on 1st string or between 4th and 5th string
      case 'Си':
        return { x: 55, y: bNoteYValue }; // Randomly above 1st string or on 4th string
      default:
        return { x: 55, y: 35 }; // Default position
    }
  };

  // Check if the note is valid
  const position: NotePosition = notePosition(correctNote);

  return (
    <div className="bass-staff">
      <svg width="300" height="100" viewBox="0 0 300 100">
        <line x1="0" y1="20" x2="300" y2="20" stroke="black" strokeWidth="2" />
        <line x1="0" y1="40" x2="300" y2="40" stroke="black" strokeWidth="2" />
        <line x1="0" y1="60" x2="300" y2="60" stroke="black" strokeWidth="2" />
        <line x1="0" y1="80" x2="300" y2="80" stroke="black" strokeWidth="2" />

        {/* Render the correct note on the staff */}
        {position ? (
          <text x={position.x} y={position.y} fontSize="40" fill="red">
            {'\u266A'}
          </text>
        ) : (
          <text x={0} y={0} fontSize="40" fill="red">
            ?
          </text> // Fallback if incorrect note
        )}

        {/* Bass clef SVG */}
        <svg
          version="1.2"
          width="103"
          height="170"
          viewBox="0 0 1689 2760"
          preserveAspectRatio="xMidYMid"
          fill-rule="evenodd"
          stroke-width="19"
          stroke-linejoin="round"
          xmlSpace="preserve"
          id="svg23"
          xmlns="http://www.w3.org/2000/svg"
          x="-9"
          y="12"
        >
          <defs className="ClipPathGroup" id="defs2">
            <clipPath
              id="presentation_clip_path"
              clipPathUnits="userSpaceOnUse"
            >
              <rect x="0" y="0" width="1689" height="2760" id="rect1" />
            </clipPath>
          </defs>
          <defs className="TextShapeIndex" id="defs3" />
          <defs className="EmbeddedBulletChars" id="defs12" />

          <g className="SlideGroup" id="g23" transform="translate(0,38.52518)">
            <g id="g22">
              <g id="container-id1">
                <g
                  id="id1"
                  className="Slide"
                  clip-path="url(#presentation_clip_path)"
                >
                  <g className="Page" id="g21">
                    <g className="Graphic" id="g20">
                      <g id="id3">
                        <rect
                          className="BoundingBox"
                          stroke="none"
                          fill="none"
                          x="0"
                          y="0"
                          width="1031"
                          height="2582"
                          id="rect12"
                        />
                        <defs id="defs13">
                          <clipPath
                            id="clip_path_1"
                            clipPathUnits="userSpaceOnUse"
                          >
                            <path
                              d="m 148,87 h 830 v 961 H 148 Z"
                              id="path13"
                            />
                          </clipPath>
                        </defs>
                        <g clip-path="url(#clip_path_1)" id="g19">
                          <path
                            fill="#000000"
                            stroke="none"
                            d="m 430,92 c -177,4 -313,128 -269,318 0,1 0,1 0,1 5,66 60,117 127,117 70,0 127,-57 127,-127 0,-62 -44,-114 -103,-125 -23,-8 -58,-27 -57,-57 1,-15 19,-43 47,-56 34,-16 69,-25 104,-18 54,10 192,109 202,281 7,130 -66,305 -138,389 -115,131 -299,213 -281,227 16,15 234,-85 347,-210 C 675,682 744,556 737,404 733,252 615,87 430,92 Z"
                            id="path14"
                          />
                          <path
                            fill="none"
                            stroke="#000000"
                            stroke-width="9"
                            stroke-linejoin="miter"
                            d="m 430,92 c -177,4 -313,128 -269,318 0,1 0,1 0,1 5,66 60,117 127,117 70,0 127,-57 127,-127 0,-62 -44,-114 -103,-125 -23,-8 -58,-27 -57,-57 1,-15 19,-43 47,-56 34,-16 69,-25 104,-18 54,10 192,109 202,281 7,130 -66,305 -138,389 -115,131 -299,213 -281,227 16,15 234,-85 347,-210 C 675,682 744,556 737,404 733,252 615,87 430,92 Z"
                            id="path15"
                          />
                          <path
                            fill="#000000"
                            stroke="none"
                            d="m 973,279 v 0 c 0,17 -4,33 -13,47 -9,15 -22,27 -37,35 -15,8 -32,13 -50,13 -18,0 -35,-5 -50,-13 -16,-8 -28,-20 -37,-35 -9,-14 -14,-30 -14,-47 v 0 c 0,-16 5,-33 14,-47 9,-14 21,-26 37,-34 15,-9 32,-13 50,-13 18,0 35,4 50,13 15,8 28,20 37,34 9,14 13,31 13,47 z"
                            id="path16"
                          />
                          <path
                            fill="none"
                            stroke="#000000"
                            stroke-width="9"
                            stroke-linejoin="round"
                            stroke-linecap="round"
                            d="m 973,279 v 0 c 0,17 -4,33 -13,47 -9,15 -22,27 -37,35 -15,8 -32,13 -50,13 -18,0 -35,-5 -50,-13 -16,-8 -28,-20 -37,-35 -9,-14 -14,-30 -14,-47 v 0 c 0,-16 5,-33 14,-47 9,-14 21,-26 37,-34 15,-9 32,-13 50,-13 18,0 35,4 50,13 15,8 28,20 37,34 9,14 13,31 13,47 z"
                            id="path17"
                          />
                          <path
                            fill="#000000"
                            stroke="none"
                            d="m 973,543 v 0 c 0,16 -4,32 -13,47 -9,14 -22,26 -37,34 -15,9 -32,13 -50,13 -18,0 -35,-4 -50,-13 -16,-8 -28,-20 -37,-34 -9,-15 -14,-31 -14,-47 v 0 c 0,-17 5,-33 14,-47 9,-15 21,-27 37,-35 15,-8 32,-13 50,-13 18,0 35,5 50,13 15,8 28,20 37,35 9,14 13,30 13,47 z"
                            id="path18"
                          />
                          <path
                            fill="none"
                            stroke="#000000"
                            stroke-width="9"
                            stroke-linejoin="round"
                            stroke-linecap="round"
                            d="m 973,543 v 0 c 0,16 -4,32 -13,47 -9,14 -22,26 -37,34 -15,9 -32,13 -50,13 -18,0 -35,-4 -50,-13 -16,-8 -28,-20 -37,-34 -9,-15 -14,-31 -14,-47 v 0 c 0,-17 5,-33 14,-47 9,-15 21,-27 37,-35 15,-8 32,-13 50,-13 18,0 35,5 50,13 15,8 28,20 37,35 9,14 13,30 13,47 z"
                            id="path19"
                          />
                        </g>
                      </g>
                    </g>
                  </g>
                </g>
              </g>
            </g>
          </g>
        </svg>
      </svg>
    </div>
  );
};

export default BassSheet;
