import React, { useState } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/home';
import Knowledge from './components/knowledge';
import TestKnowledge from './components/TestKnowledge';
import SimpleKnowledge from './components/SimpleKnowledge';
import KnowledgeFixed from './components/KnowledgeFixed';
import Recognize from './components/recognize';
import AiRecreate from './components/AiRecreate';
import Analysis from './components/analysis';
import Quiz from './components/quiz';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [quizLevel, setQuizLevel] = useState(1);
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigate = (path) => {
    navigate(path);
    window.scrollTo(0, 0);
  };

  const handleAnalysisSuccess = (analysisResult) => {
    setAnalysisData(analysisResult);
    navigate('/analysis');
  };

  const handleLevelSelect = (level) => {
    setQuizLevel(level);
    navigate('/quiz');
  };

  return (
    <div className="App">
      <Navbar currentRoute={location.pathname} />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/knowledge" element={<KnowledgeFixed onLevelSelect={handleLevelSelect} />} />
          <Route path="/recognize" element={<Recognize onAnalysisSuccess={handleAnalysisSuccess} onNavigate={handleNavigate} />} />
          <Route path="/recreate" element={<AiRecreate />} />
          <Route path="/analysis" element={<Analysis analysisData={analysisData} onNavigate={handleNavigate} />} />
          <Route path="/quiz" element={<Quiz level={quizLevel} />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

