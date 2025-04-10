import React, { useState } from 'react';
import '../styles/Sarthana.css';

const Dashboard = () => {
  const [navOpen, setNavOpen] = useState(false);

  return (
    <>
      <header className="dashboard-header" data-aos="fade-down">
        <h1>Sarthana</h1>
        <div className="menu-toggle" onClick={() => setNavOpen(!navOpen)}>
          ☰
        </div>
        <nav className={`dashboard-nav ${navOpen ? 'active' : ''}`}>
          <a href="#">Home</a>
          <a href="#">Current Affairs</a>
          <a href="#">Topic Summarisation</a>
          <a href="#">Mock Test</a>
          <a href="#">Essay Writing</a>
          <a href="#">Saved Notes</a>
          <a href="#">NCERTs</a>
        </nav>
      </header>

      <div className="dashboard-container">
        <div className="dashboard-card" data-aos="fade-up">
          <h2>Welcome Back!</h2>
          <p>Stay focused and persistent. Your UPSC journey is one step closer to success! 🌟</p>
        </div>

        <div className="dashboard-card" data-aos="fade-right">
          <h2>Quick Access</h2>
          <ul>
            <li><a href="#">📜 Current Affairs</a></li>
            <li><a href="#">📝 Essay Practice</a></li>
            <li><a href="#">🧠 Topic Summaries</a></li>
            <li><a href="#">📚 NCERT Library</a></li>
          </ul>
        </div>

        <div className="dashboard-card" data-aos="zoom-in">
          <h2>Quote of the Day</h2>
          <blockquote>"Success doesn't come from what you do occasionally, it comes from what you do consistently."</blockquote>
        </div>

        <div className="dashboard-card" data-aos="flip-left">
          <h2>Next Mock Test</h2>
          <p>📅 28 March 2025<br />📖 Topic: Indian Economy</p>
          <a href="#" className="dashboard-btn">Enroll Now</a>
        </div>

        <div className="dashboard-card" data-aos="fade-left">
          <h2>Saved Notes</h2>
          <p>Review and revise your saved notes anytime.</p>
          <a href="#" className="dashboard-btn">View Notes</a>
        </div>

        <div className="dashboard-card" data-aos="fade-up-right">
          <h2>NCERT eBooks</h2>
          <p>Access all essential NCERT books categorized for UPSC preparation.</p>
          <a href="#" className="dashboard-btn">Explore</a>
        </div>
      </div>

      <footer className="dashboard-footer" data-aos="fade-up">
        <p>© 2025 Sarthana. Crafted with passion & purpose.</p>
      </footer>
    </>
  );
};

export default Dashboard;