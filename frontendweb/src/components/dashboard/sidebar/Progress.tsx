import React from "react";

const ProgressCircle = ({
  strokeWidth,
  percentage,
  size,
  color,
}: {
  strokeWidth: number;
  percentage: number;
  size: number;
  color: string;
}) => {
  const radius = 50 - strokeWidth / 2;
  const pathDescription = `
      M 50,50 m 0,-${radius}
      a ${radius},${radius} 0 1 1 0,${2 * radius}
      a ${radius},${radius} 0 1 1 0,-${2 * radius}
    `;

  const diameter = Math.PI * 2 * radius;
  const progressStyle = {
    stroke: color,
    strokeLinecap: "round",
    strokeDasharray: `${diameter}px ${diameter}px`,
    strokeDashoffset: `${((100 - percentage) / 100) * diameter}px`,
  } as React.CSSProperties;

  return (
    <div className="progress-circle">
      <svg className={"CircularProgressbar"} viewBox="0 0 100 100" width={size} height={size}>
        <path
          className="CircularProgressbar-trail"
          d={pathDescription}
          strokeWidth={strokeWidth}
          fillOpacity={0}
          style={{
            stroke: "#d6d6d6",
          }}
        />

        <path
          className={`CircularProgressbar-path stroke-${color}`}
          d={pathDescription}
          strokeWidth={strokeWidth}
          fillOpacity={0}
          style={progressStyle}
        />

        <text
          className="CircularProgressbar-text"
          x={50}
          y={50}
          style={{
            fill: "black",
            fontWeight: "bold",
            fontSize: "32px",
            dominantBaseline: "central",
            textAnchor: "middle",
          }}
        >
          {`${Math.floor(Number(percentage.toPrecision(2)))}%`}
        </text>
      </svg>
    </div>
  );
};

export default ProgressCircle;