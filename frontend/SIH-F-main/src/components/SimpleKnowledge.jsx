import React, { useState } from 'react';
import './knowledge.css';
import './knowledge-query-section.css';
import KnowledgeQuery from './knowledge-query';

const SimpleKnowledge = ({ onLevelSelect }) => {
    const [showLevelSelect, setShowLevelSelect] = useState(false);

    const handleStartGameClick = () => {
        setShowLevelSelect(true);
    };

    const handleLevelClick = (level) => {
        if (onLevelSelect) {
            onLevelSelect(level);
        }
    };

    if (showLevelSelect) {
        return (
            <div className="knowledge-container level-select-view">
                <div className="level-select-container">
                    <h2 className="level-select-title">CHOOSE A LEVEL</h2>
                    <div className="level-grid-container">
                        <div className="level-grid">
                            {[...Array(15)].map((_, i) => <div key={i} className="dot"></div>)}
                            <svg className="level-path" viewBox="0 0 220 80">
                                <path d="M 20 20 L 70 60 L 120 20 L 170 60 L 220 20" stroke="#b22222" strokeWidth="3" fill="none" />
                            </svg>
                            {[
                                { level: 1, x: '20px', y: '20px' },
                                { level: 2, x: '70px', y: '60px' },
                                { level: 3, x: '120px', y: '20px' },
                                { level: 4, x: '170px', y: '60px' },
                                { level: 5, x: '220px', y: '20px' },
                            ].map(({ level, x, y }) => (
                                <div key={level} className="level-node" style={{ top: y, left: x }} onClick={() => handleLevelClick(level)}>
                                    {level}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="knowledge-container">
            <div className="knowledge-content-card">
                <div className="user-profile">
                    <img src="https://i.imgur.com/4KeKvtH.png" alt="User Avatar" className="user-avatar" />
                    <div className="user-info">
                        <h1 className="user-name">Kushagra Chaudhary</h1>
                        <div className="user-stats">
                            <span><strong>XP</strong> 2674</span>
                            <span>👑 27</span>
                            <span>👍 7</span>
                            <span>🏆 Rank</span>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content">
                    <div className="stats-overview">
                        <h2>Progress Overview</h2>
                        <div className="stat-cards">
                            <div className="stat-card">
                                <h3>Completed</h3>
                                <p>65%</p>
                            </div>
                            <div className="stat-card">
                                <h3>Accuracy</h3>
                                <p>78%</p>
                            </div>
                            <div className="stat-card">
                                <h3>Score</h3>
                                <p>2350</p>
                            </div>
                        </div>
                    </div>
                </div>

                <button className="start-game-button" onClick={handleStartGameClick}>
                    START THE GAME
                </button>
                
                <div className="knowledge-query-section">
                    <h2>Explore Kolam Knowledge</h2>
                    <KnowledgeQuery />
                </div>
            </div>
        </div>
    );
};

export default SimpleKnowledge;