import React, {useState, useEffect, useRef} from "react";
import QuizCard from "./quizcard";
import ProgressBar from "./progressbar";

export default function QuizGame({questions, startLevel=0, onFinish, onBackToLevels}){
  const [levelIndex, setLevelIndex] = useState(startLevel);
  const [qIndex, setQIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [reveal, setReveal] = useState(false);
  const [score, setScore] = useState(0);
  const timeoutRef = useRef();

  const totalQuestions = questions.reduce((s, lv)=> s + lv.items.length, 0);
  const currentProgressNumber = questions.slice(0,levelIndex).reduce((s,lv)=> s + lv.items.length, 0) + (qIndex + 1);

  const currentLevel = questions[levelIndex];
  const currentQ = currentLevel.items[qIndex];

  useEffect(()=>{
    // reset when level changed externally
    setSelected(null);
    setReveal(false);
    return ()=> clearTimeout(timeoutRef.current);
  },[levelIndex]);

  const handleChoose = (idx) => {
    setSelected(idx);
    setReveal(true);
    if (idx === currentQ.answer) setScore(s=>s+1);

    // auto-advance short delay (1.2s)
    timeoutRef.current = setTimeout(()=> {
      setSelected(null);
      setReveal(false);
      if (qIndex + 1 < currentLevel.items.length) {
        setQIndex(qIndex + 1);
      } else if (levelIndex + 1 < questions.length) {
        setLevelIndex(levelIndex + 1);
        setQIndex(0);
      } else {
        onFinish?.();
      }
    }, 900);
  };

  useEffect(()=> {
    return ()=> clearTimeout(timeoutRef.current);
  },[]);

  return (
    <div style={{display:"flex", flexDirection:"column", alignItems:"center", gap:12}}>
      <div style={{width:520, display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <div style={{color:"#333"}}>
          <div style={{fontSize:14, fontWeight:700}}>Score: {score}</div>
          <div style={{fontSize:13, color:"#555"}}>Level {currentLevel.level} • Q{currentQ.id}</div>
        </div>
        <div>
          <button onClick={onBackToLevels}>Back</button>
        </div>
      </div>

      <QuizCard
        level={currentLevel.level}
        qnum={currentQ.id}
        data={currentQ}
        onChoose={handleChoose}
        selectedIndex={selected}
        reveal={reveal}
      />

      <div style={{width:520}}>
        <ProgressBar value={currentProgressNumber} max={totalQuestions} />
      </div>
    </div>
  );
}
