import React from 'react';
import '../styles/Sarthana.css';

const Home = () => {
  return (
    <>
      <header className="hero-section">
        <div className="overlay"></div>
        <div className="content" data-aos="fade-up">
          <h1>Sarthana</h1>
          <p>Your Gateway to Excellence in Learning</p>
          <a href="/login" className="btn">Get Started</a>
        </div>
      </header>

      <section id="about" className="section">
        <div className="container" data-aos="fade-right">
          <h2>About Sarthana</h2>
          <p>
            Sarthana is a premier platform tailored for UPSC aspirants. We blend quality content, strategy, and practice to fuel your success.
          </p>
        </div>
      </section>

      <section className="section dark-bg">
        <div className="container" data-aos="fade-left">
          <h2>Our Courses</h2>
          <div className="cards">
            <div className="card" data-aos="zoom-in">
              <h3>UPSC GS</h3>
              <p>Master General Studies with clarity & precision.</p>
            </div>
            <div className="card" data-aos="zoom-in" data-aos-delay="100">
              <h3>Essay & Ethics</h3>
              <p>Develop strong essay & ethical analysis skills.</p>
            </div>
            <div className="card" data-aos="zoom-in" data-aos-delay="200">
              <h3>Optional Subjects</h3>
              <p>Detailed coverage & guidance for optionals.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container" data-aos="fade-up">
          <h2>Preparation Strategy</h2>
          <p>Effective study plans, smart revisions, & topper strategies.</p>
          <a href="#strategy" className="btn">View Strategy</a>
        </div>
      </section>

      <section className="section dark-bg">
        <div className="container" data-aos="fade-up">
          <h2>Daily Quizzes & Mock Tests</h2>
          <p>Daily quizzes and Prelims & Mains mocks to sharpen your skills.</p>
          <div className="cards">
            <div className="card" data-aos="flip-left">
              <h3>Daily Quiz</h3>
              <p>Stay updated & self-evaluate regularly.</p>
            </div>
            <div className="card" data-aos="flip-right" data-aos-delay="100">
              <h3>Mock Test</h3>
              <p>Simulate real exam conditions.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container" data-aos="fade-up">
          <h2>Contact Us</h2>
          <p>Reach out for queries or assistance.</p>
          <a href="mailto:contact@sarthana.com" className="btn">Email Us</a>
        </div>
      </section>

      <footer>
        <p>© 2025 Sarthana. Crafted with passion & purpose.</p>
      </footer>
    </>
  );
};

export default Home;