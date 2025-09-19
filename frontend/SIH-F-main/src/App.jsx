import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Knowledge from './components/Knowledge';
import Recognize from './components/Recognize';
import AiRecreate from './components/AiRecreate';
import Analysis from './components/Analysis';
import Quiz from './components/Quiz';
import './App.css';

function App() {
  // Initialize route from the browser's current URL path
  const [route, setRoute] = useState(window.location.pathname);
  const [analysisData, setAnalysisData] = useState(null);
  const [quizLevel, setQuizLevel] = useState(1);

  // Effect to handle browser back/forward navigation
  useEffect(() => {
    const handlePopState = () => {
      setRoute(window.location.pathname);
    };

    window.addEventListener('popstate', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const handleNavigate = (newRoute) => {
    setRoute(newRoute);
    // Update the browser's URL without a full page reload
    window.history.pushState(null, '', newRoute);
    window.scrollTo(0, 0);
  };

  /**
   * UPDATED: Now accepts the full analysis object from the Recognize component
   * @param {object} analysisResult - Object containing image and prediction data
   */
  const handleAnalysisSuccess = (analysisResult) => {
    setAnalysisData(analysisResult);
    handleNavigate('/analysis');
  };

  const handleLevelSelect = (level) => {
    setQuizLevel(level);
    handleNavigate('/quiz');
  };

  const renderContent = () => {
    // Now rendering is based on the 'route' state, which syncs with the URL
    switch (route) {
      case '/knowledge':
        return <Knowledge onLevelSelect={handleLevelSelect} />;
      case '/recognize':
        return <Recognize onAnalysisSuccess={handleAnalysisSuccess} onNavigate={handleNavigate} />;
      case '/recreate':
        return <AiRecreate />;
      case '/analysis':
        return <Analysis analysisData={analysisData} onNavigate={handleNavigate} />;
      case '/quiz':
        return <Quiz level={quizLevel} />;
      case '/':
      default:
        // Default to home for any unrecognized routes
        return <Home onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="App">
      <Navbar onNavigate={handleNavigate} currentRoute={route} />
      <main>
        {renderContent()}
      </main>
    </div>
  );
}

export default App;

