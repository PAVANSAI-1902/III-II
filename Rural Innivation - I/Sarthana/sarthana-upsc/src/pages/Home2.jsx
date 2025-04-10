import React from 'react';
import '../styles/Sarthana.css';

const Home2 = () => {
  return (
    <>
      <header className="hero-section">
        <div className="overlay"></div>
        <div className="content" data-aos="fade-up">
          <h1>Sarthana</h1>
          <p>Your Gateway to Excellence in Learning</p>
          <a href="#about" className="btn">Get Started</a>
        </div>
      </header>

      <section id="about" className="section">
        <div className="container" data-aos="fade-right">
          <h2>About Sarthana</h2>
          <p>
            Sarthana is a modern educational platform designed to elevate your learning journey. 
            With interactive lessons, real-world projects, and a dynamic community, your success starts here.
          </p>
        </div>
      </section>

      <section className="section alt-bg">
        <div className="container" data-aos="fade-left">
          <h2>Our Courses</h2>
          <div className="cards">
            <div className="card" data-aos="zoom-in">
              <h3>Web Development</h3>
              <p>Master HTML, CSS, JavaScript, and modern frameworks.</p>
            </div>
            <div className="card" data-aos="zoom-in" data-aos-delay="100">
              <h3>Data Science</h3>
              <p>Learn Python, Machine Learning, and Big Data analysis.</p>
            </div>
            <div className="card" data-aos="zoom-in" data-aos-delay="200">
              <h3>Cyber Security</h3>
              <p>Secure networks, systems, and become a cybersecurity expert.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="contact">
        <div className="container" data-aos="fade-up">
          <h2>Contact Us</h2>
          <p>Have questions? Reach out to us and let's connect!</p>
          <a href="mailto:contact@sarthana.com" className="btn">Email Us</a>
        </div>
      </section>

      <footer>
        <p>© 2025 Sarthana. Crafted with passion and code.</p>
      </footer>
    </>
  );
};

export default Home2;