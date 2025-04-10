import React, { useState } from 'react';
import '../styles/Sarthana.css';

const Login = () => {
  const [showRegister, setShowRegister] = useState(false);

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    window.location.href = "/dashboard";
  };

  const handleRegisterSubmit = (e) => {
    e.preventDefault();
    alert("Registration successful! Please log in.");
    setShowRegister(false);
  };

  return (
    <section className="hero-section">
      <div className="overlay"></div>
      <div className="content">
        <h1>Welcome Back!</h1>
        <p>Login or Register to continue your journey</p>

        <div className="form-container">
          <form className={`auth-form ${showRegister ? 'hidden' : ''}`} onSubmit={handleLoginSubmit}>
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit" className="btn">Login</button>
            <p className="switch-text">
              Don't have an account?{' '}
              <a href="#" onClick={(e) => { e.preventDefault(); setShowRegister(true); }}>
                Register
              </a>
            </p>
          </form>

          <form className={`auth-form ${!showRegister ? 'hidden' : ''}`} id="register-form" onSubmit={handleRegisterSubmit}>
            <input type="text" placeholder="Full Name" required />
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit" className="btn">Register</button>
            <p className="switch-text">
              Already have an account?{' '}
              <a href="#" onClick={(e) => { e.preventDefault(); setShowRegister(false); }}>
                Login
              </a>
            </p>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Login;