import React, { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/navbar';
import Home from './components/home';
import Knowledge from './components/knowledge';
import Recognize from './components/recognize';
import Analysis from './components/analysis';
import AiRecreate from './components/AiRecreate';
import Quiz from './components/quiz';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [quizLevel, setQuizLevel] = useState(1);
  const navigate = useNavigate();

  const handleAnalysisSuccess = (data) => {
    console.log('App received analysis data:', data);
    setAnalysisData(data); // Pass the complete data object directly
    navigate('/analysis');
  };

  const handleLevelSelect = (level) => {
    setQuizLevel(level);
    navigate('/quiz');
  };

  return (
    <div className="App">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/knowledge" element={<Knowledge onLevelSelect={handleLevelSelect} />} />
          <Route path="/recognize" element={<Recognize onAnalysisSuccess={handleAnalysisSuccess} />} />
          <Route path="/analysis" element={<Analysis analysisData={analysisData} />} />
          <Route path="/recreate" element={<AiRecreate />} />
          <Route path="/quiz" element={<Quiz level={quizLevel} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

