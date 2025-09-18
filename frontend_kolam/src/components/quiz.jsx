import React, { useState, useEffect } from 'react';
import quizData from './quizData';
import './Quiz.css';

const Quiz = ({ level, setCurrentRoute }) => {
    const [currentLevel, setCurrentLevel] = useState(level - 1);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [feedback, setFeedback] = useState(''); // 'correct', 'wrong', ''
    const [selectedAnswer, setSelectedAnswer] = useState(null); // Track the user's choice
    const [isAnswered, setIsAnswered] = useState(false);
    const [isLevelComplete, setIsLevelComplete] = useState(false);

    useEffect(() => {
        const levelData = quizData[currentLevel];
        if (levelData && levelData.items[questionIndex]) {
            setCurrentQuestion(levelData.items[questionIndex]);
            // Reset state for the new question
            setIsAnswered(false);
            setSelectedAnswer(null);
            setFeedback('');
        } else {
            setIsLevelComplete(true);
        }
    }, [currentLevel, questionIndex]);

    const handleAnswer = (selectedIndex) => {
        if (isAnswered) return;

        setIsAnswered(true);
        setSelectedAnswer(selectedIndex);

        if (selectedIndex === currentQuestion.answer) {
            setFeedback('correct');
        } else {
            setFeedback('wrong');
        }

        setTimeout(() => {
            setQuestionIndex(prevIndex => prevIndex + 1);
        }, 2000); // Increased delay to see the feedback
    };
    
    const handleNextLevel = () => {
        if (currentLevel < quizData.length - 1) {
            setCurrentLevel(prevLevel => prevLevel + 1);
            setQuestionIndex(0);
            setIsLevelComplete(false);
        } else {
            setCurrentRoute('/knowledge');
        }
    }
    
    const getOptionClassName = (index) => {
        if (!isAnswered) return ''; // Default state

        const isCorrect = index === currentQuestion.answer;
        const isSelected = index === selectedAnswer;

        if (isCorrect) return 'correct';
        if (isSelected && !isCorrect) return 'wrong-selection';
        
        return 'disabled';
    };

    if (isLevelComplete) {
         return (
            <div className="quiz-container completion-screen">
                <h2>Level {currentLevel + 1} Complete!</h2>
                {currentLevel < quizData.length - 1 ? (
                    <button onClick={handleNextLevel}>Go to Level {currentLevel + 2}</button>
                ) : (
                    <button onClick={handleNextLevel}>Finish Quiz</button>
                )}
            </div>
        );
    }
    
    if (!currentQuestion) {
        return <div className="quiz-container loading">Loading question...</div>;
    }

    return (
        <div className="quiz-container">
            <div className={`quiz-card ${feedback}`}>
                 {/* This container will be blurred */}
                <div className="quiz-content">
                    <div className="quiz-header">
                        <h2>Level {currentLevel + 1}</h2>
                        <p>Q{questionIndex + 1}</p>
                    </div>
                    <h3 className="question-text">{currentQuestion.question}</h3>
                    <div className="options-grid">
                        {currentQuestion.options.map((option, index) => (
                            <button
                                key={index}
                                className={`option-card ${getOptionClassName(index)}`}
                                onClick={() => handleAnswer(index)}
                                disabled={isAnswered}
                            >
                                <span>{String.fromCharCode(65 + index)}</span> {option}
                            </button>
                        ))}
                    </div>
                </div>
                 {feedback && <div className={`feedback-overlay ${feedback}-anim`}>{feedback.toUpperCase()} ANSWER</div>}
            </div>
        </div>
    );
};

export default Quiz;

