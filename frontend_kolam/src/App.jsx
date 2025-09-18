import React, { useState } from 'react';
import Navbar from './components/navbar';
import Home from './components/home';
import Knowledge from './components/knowledge';
import Recognize from './components/recognize';
import Analysis from './components/analysis';
import AiRecreate from './components/AiRecreate';
import Quiz from './components/quiz';

function App() {
  const [currentRoute, setCurrentRoute] = useState('/home');
  const [analysisData, setAnalysisData] = useState(null);
  const [quizLevel, setQuizLevel] = useState(1);

  const handleAnalysisSuccess = (imageData) => {
    setAnalysisData({ image: imageData });
    setCurrentRoute('/analysis');
  };

  const handleLevelSelect = (level) => {
    setQuizLevel(level);
    setCurrentRoute('/quiz');
  };

  const renderContent = () => {
    switch (currentRoute) {
      case '/knowledge':
        return <Knowledge setCurrentRoute={setCurrentRoute} onLevelSelect={handleLevelSelect} />;
      case '/recognize':
        return <Recognize setCurrentRoute={setCurrentRoute} onAnalysisSuccess={handleAnalysisSuccess} />;
      case '/analysis':
        return <Analysis analysisData={analysisData} />;
      case '/recreate':
        return <AiRecreate />;
       case '/quiz':
        return <Quiz level={quizLevel} setCurrentRoute={setCurrentRoute} />;
      case '/home':
      default:
        return <Home setCurrentRoute={setCurrentRoute} />;
    }
  };

  return (
    <div className="App">
      <Navbar />
      <main>
        {renderContent()}
      </main>
    </div>
  );
}

export default App;

