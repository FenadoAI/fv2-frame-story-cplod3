import React, { useEffect, useState } from 'react';
import '../styles/Hero.css';

const Hero = ({ photographerName, tagline, featuredPhoto }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setTimeout(() => setIsVisible(true), 100);
  }, []);

  const defaultImage = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1920' height='1080'%3E%3Crect fill='%23171717' width='1920' height='1080'/%3E%3C/svg%3E";

  return (
    <section className="hero-section" id="home">
      <div className="hero-background">
        <img
          src={featuredPhoto || defaultImage}
          alt="Featured work"
          className="hero-image"
        />
        <div className="hero-overlay" />
      </div>

      <div className={`hero-content ${isVisible ? 'visible' : ''}`}>
        <h1 className="hero-title">{photographerName}</h1>
        <p className="hero-tagline">{tagline}</p>

        <div className="scroll-indicator">
          <div className="scroll-arrow">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
