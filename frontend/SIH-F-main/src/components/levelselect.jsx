import React from "react";

export default function LevelSelect({levels, onStartLevel}){
  return (
    <div style={{display:"flex",flexDirection:"column",gap:14,alignItems:"center"}}>
      <div className="card" style={{textAlign:"center"}}>
        <h1 className="h1">CHOOSE A LEVEL</h1>
        <div style={{marginTop:8, color:"#ddd"}}>Pick a difficulty</div>
        <div style={{height:14}} />
        <div className="level-grid">
          {levels.map((lv, idx) => (
            <div key={lv.level} className="level-item" onClick={()=> onStartLevel(idx)}>
              <div className="level-emoji">{lv.emoji}</div>
              <div style={{fontWeight:700, marginTop:6}}>Level {lv.level}</div>
              <div style={{fontSize:12, marginTop:6, color:"#444"}}>{lv.items.length} questions</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
