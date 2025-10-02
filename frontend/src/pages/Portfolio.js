import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Hero from '../components/Hero';
import Gallery from '../components/Gallery';
import About from '../components/About';
import Testimonials from '../components/Testimonials';
import Contact from '../components/Contact';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';
const API = `${API_BASE}/api`;

const Portfolio = () => {
  const [photos, setPhotos] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [about, setAbout] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [photosRes, testimonialsRes, aboutRes] = await Promise.all([
          axios.get(`${API}/photos`),
          axios.get(`${API}/testimonials`),
          axios.get(`${API}/about`)
        ]);

        setPhotos(photosRes.data);
        setTestimonials(testimonialsRes.data);
        setAbout(aboutRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-950">
        <div className="text-neutral-100 text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="portfolio-container">
      <Hero
        photographerName={about?.photographerName || 'Your Name'}
        tagline={about?.tagline || 'Capturing Life\'s Beautiful Moments'}
        featuredPhoto={photos.find(p => p.featured)?.imageData}
      />
      <Gallery photos={photos} />
      <About about={about} />
      <Testimonials testimonials={testimonials} />
      <Contact />
    </div>
  );
};

export default Portfolio;
