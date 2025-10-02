import React, { useEffect, useRef, useState } from 'react';
import '../styles/About.css';

const About = ({ about }) => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);
  const imageRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.2 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  // Parallax effect
  useEffect(() => {
    const handleScroll = () => {
      if (imageRef.current && sectionRef.current) {
        const rect = sectionRef.current.getBoundingClientRect();
        const scrolled = window.pageYOffset;
        const sectionTop = sectionRef.current.offsetTop;
        const offset = (scrolled - sectionTop) * 0.3;
        imageRef.current.style.transform = `translateY(${offset}px)`;
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const defaultImage = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='800'%3E%3Crect fill='%23262626' width='600' height='800'/%3E%3C/svg%3E";

  return (
    <section className="about-section" id="about" ref={sectionRef}>
      <div className={`about-container ${isVisible ? 'visible' : ''}`}>
        <div className="about-image-wrapper">
          <div className="about-image-container" ref={imageRef}>
            <img
              src={defaultImage}
              alt={about?.photographerName}
              className="about-image"
            />
          </div>
        </div>

        <div className="about-content">
          <h2 className="about-title">About</h2>
          <h3 className="about-name">{about?.photographerName || 'Your Name'}</h3>
          <p className="about-bio">
            {about?.bioText || 'Professional photographer capturing moments that matter. With years of experience and a passion for visual storytelling, I create images that resonate with emotion and authenticity.'}
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;
