// TrebleStaff.tsx
import React from 'react';

interface TrebleStaffProps {
  correctNote: string;
}

interface NotePosition {
  x: number;
  y: number;
} // Define structure of position

const TrebleStaff: React.FC<TrebleStaffProps> = ({ correctNote }) => {
  // Function to determine the position of the note on the staff

  const notePosition = (note: string) => {
    const dNoteYValue: number = Math.random() < 0.5 ? 25 : 95;
    const eNoteYValue: number = Math.random() < 0.5 ? 15 : 85;

    switch (note) {
      case 'C':
      case 'До':
        return { x: 55, y: 35 }; // Randomly above first string or on fourth string
      case 'D':
      case 'Ре':
        return { x: 55, y: dNoteYValue }; // Randomly on second string or below fifth string
      case 'E':
      case 'Ми':
        return { x: 55, y: eNoteYValue }; // Randomly between first and second string or on fifth string
      case 'F':
      case 'Фа':
        return { x: 55, y: 75 }; // Randomly between first and second string or on fifth string
      case 'G':
      case 'Соль':
        return { x: 55, y: 65 }; // Randomly on first string or between fourth and fifth string
      case 'A':
      case 'Ля':
        return { x: 55, y: 55 };
      case 'B':
      case 'Си':
        return { x: 55, y: 45 }; // Randomly on second string or below fifth string
      default:
        return { x: 55, y: 35 }; // Default position
    }
  };

  // Check if the note is valid
  const position: NotePosition = notePosition(correctNote);

  return (
    <div className="treble-staff">
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
          </text> // Fallback if note is not valid
        )}
        {/* Treble clef image */}
        <svg
          version="1.2"
          width="40"
          height="100"
          viewBox="0 0 9803 30549"
          preserveAspectRatio="xMidYMid"
          fill-rule="evenodd"
          stroke-width="19"
          stroke-linejoin="round"
          xmlSpace="preserve"
          id="svg18"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs className="ClipPathGroup" id="defs2">
            <clipPath
              id="presentation_clip_path"
              clipPathUnits="userSpaceOnUse"
            >
              <rect x="0" y="0" width="9803" height="30549" id="rect1" />
            </clipPath>
          </defs>
          <defs className="TextShapeIndex" id="defs3" />
          <defs className="EmbeddedBulletChars" id="defs12" />
          <g className="SlideGroup" id="g18">
            <g id="g17">
              <g id="container-id1">
                <g
                  id="id1"
                  className="Slide"
                  clip-path="url(#presentation_clip_path)"
                >
                  <g className="Page" id="g16">
                    <g className="Graphic" id="g15">
                      <g id="id3">
                        <rect
                          className="BoundingBox"
                          stroke="none"
                          fill="none"
                          x="0"
                          y="0"
                          width="9803"
                          height="30549"
                          id="rect12"
                        />
                        <defs id="defs13">
                          <clipPath
                            id="clip_path_1"
                            clipPathUnits="userSpaceOnUse"
                          >
                            <path d="M 0,0 H 9802 V 30548 H 0 Z" id="path13" />
                          </clipPath>
                        </defs>
                        <g clip-path="url(#clip_path_1)" id="g14">
                          <path
                            fill="#000000"
                            stroke="none"
                            d="m 5594,0 c 0,0 -3028,4129 -3028,7668 0,1038 337,2732 813,4697 C 1692,14614 0,16842 0,18359 c 0,3023 1759,5548 4756,5548 532,0 1035,-53 1502,-155 165,856 282,1585 278,2133 -23,3315 -1442,3980 -2287,4262 -141,46 -317,-4 -495,0 500,-282 831,-764 831,-1312 0,-869 -829,-1573 -1851,-1573 -1021,0 -1850,704 -1850,1573 0,720 572,1328 1351,1514 421,179 1257,94 1879,190 758,117 2884,-1032 2858,-4686 -4,-548 -102,-1309 -272,-2215 1903,-573 3102,-2018 3102,-3956 -1,-2271 -1920,-3823 -4410,-3823 -197,0 -385,13 -566,36 -151,-582 -300,-1161 -443,-1727 C 5850,12949 7206,11238 7276,7864 7353,4195 6267,459 6267,459 Z m 1135,6279 c 0,1460 -1402,3474 -2926,5520 -414,-1784 -699,-3291 -699,-4197 0,-3343 3096,-4260 3096,-4260 0,0 529,131 529,2937 z m -2801,8250 c 127,483 257,973 389,1466 -1764,467 -2626,2057 -2626,3273 0,1224 1407,2282 2140,2654 -866,-477 -1063,-1692 -1063,-2458 0,-647 660,-2087 1743,-2743 592,2207 1188,4418 1579,6219 -505,329 -1038,522 -1505,522 -1413,0 -3938,-918 -3943,-4918 -2,-1957 1637,-2754 3286,-4015 z m -97,7393 c 65,35 133,67 206,94 -60,-23 -129,-55 -206,-94 z m 4186,-2195 c 0,1139 -676,2210 -1519,2911 -385,-1793 -953,-3973 -1516,-6139 215,-74 442,-115 680,-115 1749,0 2355,1375 2355,3343 z"
                            id="path14"
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

export default TrebleStaff;
