import React from "react";

export default function QuizCard({level, qnum, data, onChoose, selectedIndex, reveal}) {
  return (
    <div className="card">
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <div style={{textAlign:"center"}}>
          <div className="h1">Level {level}</div>
          <div className="q-label">Q{qnum}</div>
        </div>
      </div>

      <div className="question">{data.question}</div>

      <div className="options">
        {data.options.map((opt, idx) => {
          let cls = "option";
          if (reveal) {
            if (idx === data.answer) cls += " correct";
            else if (idx === selectedIndex && selectedIndex !== data.answer) cls += " wrong";
            else cls += " disabled";
          } else if (selectedIndex !== null) {
            cls += " disabled";
          }
          return (
            <button
              key={idx}
              className={cls}
              onClick={()=> !reveal && onChoose(idx)}
              disabled={reveal || selectedIndex !== null}
              aria-label={`Option ${String.fromCharCode(65 + idx)} ${opt}`}
            >
              <div className="letter">{String.fromCharCode(65 + idx)}</div>
              <div>{opt}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
