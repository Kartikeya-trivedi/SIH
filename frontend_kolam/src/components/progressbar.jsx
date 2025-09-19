import React from "react";
export default function ProgressBar({value, max}){
  const pct = Math.round((value/max)*100);
  return (
    <div style={{width:"520px"}}>
      <div style={{display:"flex", justifyContent:"space-between", marginBottom:6, color:"#333"}}>
        <div>Progress</div>
        <div>{value}/{max}</div>
      </div>
      <div className="progress"><div style={{width: `${pct}%`}}/></div>
    </div>
  );
}
