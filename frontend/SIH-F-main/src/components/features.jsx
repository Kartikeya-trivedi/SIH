import React from 'react';
import './features.css';

const featuresData = [
  {
    title: 'Interactive Learning',
    points: [
      'Duolingo-style Quizzes: Progressive learning with gamified elements',
      'Progress Tracking: Monitor your learning journey and achievements',
      'Cultural Context: Learn about the history and meaning behind patterns',
      'Difficulty Levels: From beginner to advanced patterns',
    ],
    imagePlaceholder: 'IMAGE',
  },
  {
    title: 'AI-Powered Capabilities',
    points: [
      'Kolam Detection: Upload images and get AI-powered analysis of Kolam patterns',
      'Pattern Generation: Create new Kolam designs using mathematical principles and AI',
      'Smart Recognition: Identify traditional patterns and their cultural significance',
      'AI-Powered Insights: Get explanations and hints using local LLMs',
    ],
    imagePlaceholder: 'IMAGE',
  },
  {
    title: 'Community Features',
    points: [
      'Pattern Sharing: Share your creations with the community',
      'Learning from Others: Discover patterns created by fellow learners',
      'Collaborative Learning: Work together on complex designs',
      'Cultural Exchange: Connect with people passionate about traditional art',
    ],
    imagePlaceholder: 'IMAGE',
  },
  {
    title: 'Technical Features',
    points: [
      'Real-time Processing: Fast image analysis and generation',
      'Offline Capability: Works without internet using local AI models',
      'Cross-platform: Web, mobile, and desktop support',
      'Scalable Architecture: Built for growth and performance',
    ],
    imagePlaceholder: 'IMAGE',
  },
];

const Features = () => {
  return (
    <div className="features-section-container">
      <h2 className="features-main-title">Our Features</h2>
      {featuresData.map((feature, index) => (
        <div
          className={`feature-tile ${index % 2 === 1 ? 'reverse' : ''}`}
          key={index}
        >
          <div className="feature-details">
            <h3 className="feature-title">{feature.title}</h3>
            <ul className="feature-points">
              {feature.points.map((point, i) => (
                <li key={i}>{point}</li>
              ))}
            </ul>
          </div>
          <div className="feature-image-placeholder">
            <span>{feature.imagePlaceholder}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Features;
