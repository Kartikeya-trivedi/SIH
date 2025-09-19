import React, {useEffect} from "react";

export default function SplashScreen({onFinish}){
  useEffect(()=>{
    const t = setTimeout(()=> onFinish?.(), 1200);
    return ()=> clearTimeout(t);
  },[onFinish]);

  return (
    <div style={{
      width:"520px",
      textAlign:"center",
      paddingTop:40
    }}>
      <div style={{fontFamily:"Squada One", fontSize:36, marginBottom:8}}>Kolam Quiz</div>
      <div style={{opacity:.85}}>Test your knowledge and learn about Kolams</div>
      <div style={{height:24}}/>
      <img src="/splash1.png" alt="splash" style={{width:420, borderRadius:16}} />
    </div>
  );
}
