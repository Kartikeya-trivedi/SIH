import React from 'react';
import './Home.css';

const Home = ({ onNavigate }) => {
  return (
    <>
      <div className="home-container">
        {/* Left Side with Video */}
        <div className="video-container">
          <video 
            src="/kolam-video.mp4" 
            autoPlay 
            loop 
            muted 
            playsInline 
            className="kolam-video"
          >
            Your browser does not support the video tag.
          </video>
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

          <div className="home-cta-buttons">
            <button className="feature-card-cta" onClick={() => onNavigate('/knowledge')}>
              <span>🧠</span> Test your knowledge and learn
            </button>
            <button className="feature-card-cta" onClick={() => onNavigate('/recognize')}>
              <span>📷</span> Let AI Recognize
            </button>
            <button className="feature-card-cta" onClick={() => onNavigate('/recreate')}>
              <span>✨</span> Recreate or complete patterns
            </button>
          </div>

          <div className="platform-description">
              <p>
                  An AI-powered platform for learning, exploring, and celebrating the traditional Indian art of Kolam. This platform blends cultural heritage with modern technology to provide interactive learning experiences.
              </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="features-section" id="features">
          <h2 className="features-main-title">Our Features</h2>
          <div className="features-grid">

              {/* Interactive Learning Tile */}
              <div className="feature-tile">
                  <div className="feature-content">
                      <h3 className="feature-title">Interactive Learning</h3>
                      <ul>
                          <li>Duolingo-style Quizzes: Progressive learning with gamified elements</li>
                          <li>Progress Tracking: Monitor your learning journey and achievements</li>
                          <li>Cultural Context: Learn about the history and meaning behind patterns</li>
                          <li>Difficulty Levels: From beginner to advanced patterns</li>
                      </ul>
                  </div>
                  <div className="feature-image-placeholder">
                      IMAGE
                  </div>
              </div>

              {/* AI-Powered Capabilities Tile */}
              <div className="feature-tile reverse">
                   <div className="feature-image-placeholder">
                      IMAGE
                  </div>
                  <div className="feature-content">
                      <h3 className="feature-title">AI-Powered Capabilities</h3>
                      <ul>
                          <li>Kolam Detection: Upload images and get AI-powered analysis</li>
                          <li>Pattern Generation: Create new Kolam designs using AI</li>
                          <li>Smart Recognition: Identify traditional patterns and their cultural significance</li>
                          <li>AI-Powered Insights: Get explanations and hints using local LLMs</li>
                      </ul>
                  </div>
              </div>

              {/* Community Features Tile */}
              <div className="feature-tile">
                  <div className="feature-content">
                      <h3 className="feature-title">Community Features</h3>
                      <ul>
                          <li>Pattern Sharing: Share your creations with the community</li>
                          <li>Learning from Others: Discover patterns created by fellow learners</li>
                          <li>Collaborative Learning: Work together on complex designs</li>
                          <li>Cultural Exchange: Connect with people passionate about traditional art</li>
                      </ul>
                  </div>
                   <div className="feature-image-placeholder">
                      IMAGE
                  </div>
              </div>
          </div>
      </section>
    </>
  );
};

export default Home;

