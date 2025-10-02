import React, { useState, useEffect, useRef } from 'react';
import '../styles/Testimonials.css';

const Testimonials = ({ testimonials }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [touchStart, setTouchStart] = useState(0);
  const [touchEnd, setTouchEnd] = useState(0);
  const sectionRef = useRef(null);

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

  // Auto-rotate
  useEffect(() => {
    if (testimonials.length <= 1 || isPaused) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % testimonials.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [testimonials.length, isPaused]);

  // Touch handlers for mobile swipe
  const handleTouchStart = (e) => {
    setTouchStart(e.targetTouches[0].clientX);
  };

  const handleTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const handleTouchEnd = () => {
    if (!touchStart || !touchEnd) return;

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > 50;
    const isRightSwipe = distance < -50;

    if (isLeftSwipe) {
      setCurrentIndex((prev) => (prev + 1) % testimonials.length);
    }

    if (isRightSwipe) {
      setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length);
    }

    setTouchStart(0);
    setTouchEnd(0);
  };

  if (!testimonials || testimonials.length === 0) {
    return null;
  }

  const currentTestimonial = testimonials[currentIndex];

  return (
    <section className="testimonials-section" id="testimonials" ref={sectionRef}>
      <div className={`testimonials-container ${isVisible ? 'visible' : ''}`}>
        <h2 className="testimonials-title">Client Testimonials</h2>
        <p className="testimonials-subtitle">Hear from our clients about their experience and the impact our photography has made</p>

        <div
          className="testimonial-carousel"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <div className="testimonial-card" key={currentTestimonial.id}>
            <div className="quote-icon">"</div>
            <p className="testimonial-text">{currentTestimonial.testimonialText}</p>
            <div className="testimonial-author">
              <div className="author-avatar">
                {currentTestimonial.clientName.charAt(0).toUpperCase()}
              </div>
              <div className="author-info">
                <p className="author-name">{currentTestimonial.clientName}</p>
                <div className="rating">
                  {[...Array(5)].map((_, i) => (
                    <span
                      key={i}
                      className={`star ${i < currentTestimonial.rating ? 'filled' : ''}`}
                    >
                      ★
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {testimonials.length > 1 && (
          <div className="testimonial-dots">
            {testimonials.map((_, index) => (
              <button
                key={index}
                className={`dot ${index === currentIndex ? 'active' : ''}`}
                onClick={() => setCurrentIndex(index)}
                aria-label={`Go to testimonial ${index + 1}`}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default Testimonials;
