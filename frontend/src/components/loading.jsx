import React from 'react';

function LoadingIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" width="450px" height="450px" style={{ shapeRendering: 'auto', display: 'block', background: 'transparent' }} xmlnsXlink="http://www.w3.org/1999/xlink">
      <g>
        <circle strokeLinecap="round" fill="none" strokeDasharray="45.553093477052 45.553093477052" stroke="#2172c3" strokeWidth="4" r="29" cy="50" cx="50">
          <animateTransform values="0 50 50;360 50 50" keyTimes="0;1" dur="2s" repeatCount="indefinite" type="rotate" attributeName="transform" />
        </circle>
      </g>
    </svg>
  );
}

export default LoadingIcon;