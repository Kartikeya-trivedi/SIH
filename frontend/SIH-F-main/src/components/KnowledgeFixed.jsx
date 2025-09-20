import React, { useState } from 'react';
import './knowledge.css';
import './knowledge-query-section.css';
import KnowledgeQuery from './knowledge-query';

const KnowledgeFixed = ({ onLevelSelect }) => {
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
        <div className="knowledge-container" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #f9f2e9 0%, #f5e9da 100%)',
            padding: '40px 20px',
            fontFamily: 'Montserrat, sans-serif',
        }}>
            <div className="knowledge-content-card" style={{
                backgroundColor: 'white',
                borderRadius: '24px',
                boxShadow: '0 20px 40px rgba(0, 0, 0, 0.08)',
                padding: '40px',
                width: '100%',
                maxWidth: '1000px',
                display: 'flex',
                flexDirection: 'column',
                gap: '25px',
            }}>
                <div className="user-profile" style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '25px',
                    borderBottom: '1px solid rgba(0,0,0,0.05)',
                    padding: '20px 10px 30px 10px',
                    margin: '0 0 20px 0',
                }}>
                    <div style={{
                        position: 'relative',
                        borderRadius: '50%',
                        padding: '4px',
                        background: 'linear-gradient(45deg, #b22222, #781010)',
                        boxShadow: '0 10px 20px rgba(0,0,0,0.07)'
                    }}>
                        <img 
                            src="https://i.imgur.com/4KeKvtH.png" 
                            alt="User Avatar" 
                            className="user-avatar"
                            style={{
                                width: '85px',
                                height: '85px',
                                borderRadius: '50%',
                                objectFit: 'cover',
                                border: '4px solid white',
                            }}
                        />
                    </div>
                    <div className="user-info">
                        <h1 className="user-name" style={{
                            margin: '0 0 12px 0',
                            fontSize: '1.9rem',
                            fontWeight: '700',
                            color: '#333',
                            letterSpacing: '0.5px',
                        }}>Kushagra Chaudhary</h1>
                        <div className="user-stats" style={{
                            display: 'flex',
                            gap: '25px',
                            color: '#555',
                            fontWeight: '600',
                            fontSize: '15px',
                        }}>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                <strong style={{ color: '#b22222' }}>XP</strong> 2674
                            </span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>👑 27</span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>👍 7</span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>🏆 Rank</span>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content" style={{ display: 'flex', flexDirection: 'column', width: '100%', gap: '30px', marginBottom: '30px' }}>
                    <div className="stats-overview" style={{ 
                        display: 'flex', 
                        flexDirection: 'column', 
                        alignItems: 'center', 
                        textAlign: 'center', 
                        width: '100%',
                        padding: '20px 0',
                        borderRadius: '15px',
                        background: 'linear-gradient(145deg, #f9f9f9, #f0f0f0)',
                    }}>
                        <h2 style={{ 
                            fontSize: '28px', 
                            marginBottom: '25px', 
                            color: '#333',
                            fontWeight: '700',
                            letterSpacing: '1px',
                            position: 'relative',
                            paddingBottom: '15px',
                        }}>
                            Progress Overview
                            <span style={{
                                position: 'absolute',
                                bottom: 0,
                                left: '50%',
                                transform: 'translateX(-50%)',
                                height: '4px',
                                width: '60px',
                                background: 'linear-gradient(90deg, #b22222, #781010)',
                                borderRadius: '2px',
                            }}></span>
                        </h2>
                        <div className="stat-cards" style={{ 
                            display: 'flex', 
                            flexWrap: 'wrap', 
                            gap: '25px', 
                            justifyContent: 'center', 
                            width: '100%', 
                            marginTop: '20px',
                            padding: '10px 20px',
                        }}>
                                <div className="stat-card" style={{ 
                                    background: 'linear-gradient(145deg, #ffffff, #f0f0f0)',
                                    padding: '30px 25px',
                                    borderRadius: '16px',
                                    width: '200px',
                                    boxShadow: '0 10px 20px rgba(0,0,0,0.05), 0 6px 6px rgba(0,0,0,0.07)',
                                    transition: 'transform 0.3s, box-shadow 0.3s',
                                    cursor: 'pointer',
                                    border: '1px solid rgba(255,255,255,0.8)',
                                }}>
                                    <div style={{ marginBottom: '15px' }}>
                                        <span style={{ 
                                            fontSize: '22px', 
                                            display: 'inline-block',
                                            color: '#b22222',
                                            marginBottom: '5px',
                                        }}>🏆</span>
                                    </div>
                                    <h3 style={{ 
                                        fontSize: '18px', 
                                        marginBottom: '15px',
                                        color: '#555',
                                        fontWeight: '600',
                                    }}>Completed</h3>
                                    <p style={{ 
                                        fontSize: '32px', 
                                        fontWeight: 'bold', 
                                        color: '#b22222',
                                        margin: '0',
                                    }}>65%</p>
                                </div>
                                <div className="stat-card" style={{ 
                                    background: 'linear-gradient(145deg, #ffffff, #f0f0f0)',
                                    padding: '30px 25px',
                                    borderRadius: '16px',
                                    width: '200px',
                                    boxShadow: '0 10px 20px rgba(0,0,0,0.05), 0 6px 6px rgba(0,0,0,0.07)',
                                    transition: 'transform 0.3s, box-shadow 0.3s',
                                    cursor: 'pointer',
                                    border: '1px solid rgba(255,255,255,0.8)',
                                }}>
                                    <div style={{ marginBottom: '15px' }}>
                                        <span style={{ 
                                            fontSize: '22px', 
                                            display: 'inline-block',
                                            color: '#00008b',
                                            marginBottom: '5px',
                                        }}>🎯</span>
                                    </div>
                                    <h3 style={{ 
                                        fontSize: '18px', 
                                        marginBottom: '15px',
                                        color: '#555',
                                        fontWeight: '600',
                                    }}>Accuracy</h3>
                                    <p style={{ 
                                        fontSize: '32px', 
                                        fontWeight: 'bold', 
                                        color: '#00008b',
                                        margin: '0',
                                    }}>78%</p>
                                </div>
                                <div className="stat-card" style={{ 
                                    background: 'linear-gradient(145deg, #ffffff, #f0f0f0)',
                                    padding: '30px 25px',
                                    borderRadius: '16px',
                                    width: '200px',
                                    boxShadow: '0 10px 20px rgba(0,0,0,0.05), 0 6px 6px rgba(0,0,0,0.07)',
                                    transition: 'transform 0.3s, box-shadow 0.3s',
                                    cursor: 'pointer',
                                    border: '1px solid rgba(255,255,255,0.8)',
                                }}>
                                    <div style={{ marginBottom: '15px' }}>
                                        <span style={{ 
                                            fontSize: '22px', 
                                            display: 'inline-block',
                                            color: '#28a745',
                                            marginBottom: '5px',
                                        }}>💯</span>
                                    </div>
                                    <h3 style={{ 
                                        fontSize: '18px', 
                                        marginBottom: '15px',
                                        color: '#555',
                                        fontWeight: '600',
                                    }}>Score</h3>
                                    <p style={{ 
                                        fontSize: '32px', 
                                        fontWeight: 'bold', 
                                        color: '#28a745',
                                        margin: '0',
                                    }}>2350</p>
                                </div>
                            </div>
                        </div>
                </div>

                <button 
                    className="start-game-button" 
                    onClick={handleStartGameClick}
                    style={{
                        background: 'linear-gradient(45deg, #b22222, #781010)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '15px',
                        padding: '18px 35px',
                        fontSize: '1.2rem',
                        fontWeight: '700',
                        letterSpacing: '1.5px',
                        cursor: 'pointer',
                        margin: '20px 0',
                        boxShadow: '0 10px 20px rgba(120, 0, 0, 0.2)',
                        transition: 'all 0.3s ease',
                        position: 'relative',
                        overflow: 'hidden',
                    }}
                >
                    <span style={{ position: 'relative', zIndex: '2' }}>START THE GAME</span>
                </button>
                
                <div className="knowledge-query-section" style={{
                    padding: '30px 20px',
                    borderRadius: '20px',
                    background: 'linear-gradient(145deg, #ffffff, #f0f0f0)',
                    boxShadow: '0 10px 25px rgba(0,0,0,0.05)',
                    margin: '20px 0',
                }}>
                    <h2 style={{
                        textAlign: 'center',
                        fontSize: '24px',
                        fontWeight: '700',
                        color: '#333',
                        marginBottom: '25px',
                        position: 'relative',
                        paddingBottom: '15px',
                    }}>
                        Explore Kolam Knowledge
                        <span style={{
                            position: 'absolute',
                            bottom: 0,
                            left: '50%',
                            transform: 'translateX(-50%)',
                            height: '3px',
                            width: '50px',
                            background: 'linear-gradient(90deg, #b22222, #781010)',
                            borderRadius: '2px',
                        }}></span>
                    </h2>
                    <KnowledgeQuery />
                </div>
            </div>
        </div>
    );
};

export default KnowledgeFixed;