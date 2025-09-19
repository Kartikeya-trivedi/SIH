import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title } from 'chart.js';
import KnowledgeQuery from './knowledge-query';
import './Knowledge.css';
import './knowledge-query-section.css';

// Register the necessary components for Chart.js
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title);

const Knowledge = ({ onLevelSelect }) => {
    const [showLevelSelect, setShowLevelSelect] = useState(false);
    const navigate = useNavigate();

    const handleStartGameClick = () => {
        setShowLevelSelect(true);
    };

    const handleLevelClick = (level) => {
        onLevelSelect(level);
    };

    const doughnutData = {
        labels: ['Red', 'Blue', 'Light Blue'],
        datasets: [
            {
                data: [12, 19, 3],
                backgroundColor: ['#b22222', '#00008b', '#add8e6'],
                borderColor: ['rgba(0,0,0,0)'],
                borderWidth: 1,
                cutout: '70%',
            },
        ],
    };

    const doughnutOptions = {
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: true,
            },
        },
        maintainAspectRatio: false,
    };

    const barChartData = {
        labels: ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6'],
        datasets: [
            {
                type: 'bar',
                label: 'Item 1',
                data: [12, 58, 20, 55, 18, 40],
                backgroundColor: '#add8e6',
                borderRadius: 5,
                order: 2,
            },
            {
                type: 'bar',
                label: 'Item 2',
                data: [10, 40, 15, 40, 10, 30],
                backgroundColor: '#00008b',
                borderRadius: 5,
                order: 3,
            },
            {
                type: 'line',
                label: 'Line 1',
                data: [25, 45, 65, 95, 45, 60],
                borderColor: '#b22222',
                backgroundColor: '#b22222',
                fill: false,
                tension: 0.4,
                order: 1,
            },
        ],
    };

    const barChartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#efefef'
                }
            },
            x: {
                 grid: {
                    display: false
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Progress Overview',
                font: {
                    size: 18,
                    family: 'Montserrat',
                    weight: '600'
                },
                padding: {
                    bottom: 20
                }
            },
            legend: {
                position: 'bottom',
                 labels: {
                    font: {
                        family: 'Montserrat'
                    }
                }
            },
        },
        responsive: true,
        maintainAspectRatio: false,
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
                    <div className="stats-charts">
                        <div className="chart-container">
                            <Doughnut data={doughnutData} options={doughnutOptions} />
                            <div className="chart-center-text">
                                <strong>Stats 1</strong>
                                <span>+5%</span>
                            </div>
                        </div>
                        <div className="chart-container">
                            <Doughnut data={doughnutData} options={doughnutOptions} />
                             <div className="chart-center-text">
                                <strong>Stats 2</strong>
                                <span>+12%</span>
                            </div>
                        </div>
                    </div>
                    <div className="main-chart">
                        <Bar data={barChartData} options={barChartOptions} />
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

export default Knowledge;

