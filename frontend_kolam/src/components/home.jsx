import React from 'react';
import './Home.css';

// This is the main landing page component.
// It receives `setCurrentRoute` as a prop to handle navigation.

const Home = ({ setCurrentRoute }) => {
  return (
    <>
      <div className="home-container">
        {/* Left Side with Kolam Graphics */}
        <div className="kolam-graphics">
          <div className="kolam-pattern">
            <img src="https://i.imgur.com/uRkYf7g.png" alt="Kolam design 1" style={{ width: "150px" }} />
          </div>
          <div className="kolam-pattern">
            <img src="https://i.imgur.com/gK2R4Xp.png" alt="Kolam design 2" style={{ width: "100px" }} />
          </div>
          <div className="kolam-pattern">
            <img src="https://i.imgur.com/U8E6XwF.png" alt="Kolam design 3" style={{ width: "150px" }} />
          </div>
          <div className="kolam-pattern">
            <img src="https://i.imgur.com/9O3t1gQ.png" alt="Kolam design 4" style={{ width: "80px" }} />
          </div>
        </div>

        {/* Right Side with Text Content */}
        <div className="content-section">
          <h1 className="title">Kolam Vision</h1>
          <h2 className="subtitle">From Dots to Designs — Rediscover Kolams with AI™</h2>

          <div className="description-box">
            <p>
              Kolams are more than art—they are symbols of positivity, creativity, and community. By digitizing them, we aim to preserve this cultural treasure while making it accessible to the next generation.
            </p>
          </div>

          <button className="learn-more-button">
            Learn more about Kolams <span>&#x1F50D;</span>
          </button>

          <div className="features-grid">
            {/* These cards now act as buttons to navigate to different routes */}
            <div className="feature-card feature-card-clickable" onClick={() => setCurrentRoute('/knowledge')}>
              <span>&#x1F4D6;</span> Test your knowledge and learn
            </div>
            <div className="feature-card feature-card-clickable" onClick={() => setCurrentRoute('/recognize')}>
              <span>&#x1F4F7;</span> Let AI Recognize
            </div>
            <div className="feature-card feature-card-clickable" onClick={() => setCurrentRoute('/recreate')}>
              <span>&#x2699;&#xFE0F;</span> Recreate or complete patterns
            </div>
          </div>

          <div className="platform-description">
            <p>
              An AI-powered platform for learning, exploring, and celebrating the traditional Indian art of Kolam. This platform blends cultural heritage with modern technology to provide interactive learning experiences.
            </p>
          </div>
        </div>
      </div>
      <FeaturesSection />
    </>
  );
};

// --- Integrated "Our Features" Section ---

const FeatureCard = ({ title, points, imageSrc, imageAlt, reverse }) => {
  const directionClass = reverse ? 'feature-row-reverse' : '';
  return (
    <div className={`feature-row ${directionClass}`}>
      <div className="feature-text-content">
        <h3>{title}</h3>
        <ul>
          {points.map((point, index) => (
            <li key={index}>{point}</li>
          ))}
        </ul>
      </div>
      <div className="feature-image-content">
        <div className="image-placeholder">{imageAlt}</div>
      </div>
    </div>
  );
};

const FeaturesSection = () => {
  const featuresData = [
    {
      title: 'Interactive Learning',
      points: [
        'Duolingo-style Quizzes: Progressive learning with gamified elements',
        'Progress Tracking: Monitor your learning journey and achievements',
        'Cultural Context: Learn about the history and meaning behind patterns',
        'Difficulty Levels: From beginner to advanced patterns',
      ],
      imageAlt: 'IMAGE',
    },
    {
      title: 'AI-Powered Capabilities',
      points: [
        'Kolam Detection: Upload images and get AI-powered analysis of Kolam patterns',
        'Pattern Generation: Create new Kolam designs using mathematical principles and AI',
        'Smart Recognition: Identify traditional patterns and their cultural significance',
        'AI-Powered Insights: Get explanations and hints using local LLMs',
      ],
      imageAlt: 'IMAGE',
      reverse: true,
    },
    {
      title: 'Community Features',
      points: [
          'Pattern Sharing: Share your creations with the community',
          'Learning from Others: Discover patterns created by fellow learners',
          'Collaborative Learning: Work together on complex designs',
          'Cultural Exchange: Connect with people passionate about traditional art'
      ],
      imageAlt: 'IMAGE'
    },
    {
      title: 'Technical Features',
      points: [
          'Real-time Processing: Fast image analysis and generation',
          'Offline Capability: Works without internet using local AI models',
          'Cross-platform: Web, mobile, and desktop support',
          'Scalable Architecture: Built for growth and performance'
      ],
      imageAlt: 'IMAGE',
      reverse: true
    }
  ];

  return (
    <section className="features-section">
      <h2 className="features-title">Our Features</h2>
      <div className="features-container">
        {featuresData.map((feature, index) => (
          <FeatureCard
            key={index}
            title={feature.title}
            points={feature.points}
            imageAlt={feature.imageAlt}
            reverse={feature.reverse}
          />
        ))}
      </div>
    </section>
  );
};

export default Home;

