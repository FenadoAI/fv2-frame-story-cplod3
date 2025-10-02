import React, { useState, useEffect, useRef } from 'react';
import '../styles/Gallery.css';

const categories = ['All', 'portrait', 'wedding', 'landscape', 'commercial'];

const Gallery = ({ photos }) => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [filteredPhotos, setFilteredPhotos] = useState([]);
  const [lightboxPhoto, setLightboxPhoto] = useState(null);
  const [visiblePhotos, setVisiblePhotos] = useState(new Set());
  const photoRefs = useRef([]);

  useEffect(() => {
    if (selectedCategory === 'All') {
      setFilteredPhotos(photos);
    } else {
      setFilteredPhotos(photos.filter(p => p.category === selectedCategory));
    }
  }, [selectedCategory, photos]);

  // Intersection Observer for scroll-triggered reveals
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = photoRefs.current.indexOf(entry.target);
            if (index !== -1) {
              setVisiblePhotos(prev => new Set([...prev, index]));
            }
          }
        });
      },
      { threshold: 0.1, rootMargin: '50px' }
    );

    photoRefs.current.forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => observer.disconnect();
  }, [filteredPhotos]);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setVisiblePhotos(new Set()); // Reset visibility on filter change
  };

  return (
    <section className="gallery-section" id="gallery">
      <div className="gallery-container">
        <h2 className="gallery-title">Portfolio Gallery</h2>
        <p className="gallery-subtitle">Explore our diverse collection of photographic works spanning various styles and subjects</p>

        <div className="category-filters">
          {categories.map((category) => (
            <button
              key={category}
              className={`filter-pill ${selectedCategory === category ? 'active' : ''}`}
              onClick={() => handleCategoryChange(category)}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>

        <div className="masonry-grid">
          {filteredPhotos.map((photo, index) => (
            <div
              key={photo.id}
              ref={(el) => (photoRefs.current[index] = el)}
              className={`photo-card ${visiblePhotos.has(index) ? 'visible' : ''}`}
              onClick={() => setLightboxPhoto(photo)}
            >
              <img
                src={photo.imageData}
                alt={photo.title}
                className="photo-image"
                loading="lazy"
              />
              <div className="photo-overlay">
                <h3 className="photo-title">{photo.title}</h3>
                <p className="photo-category">{photo.category}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {lightboxPhoto && (
        <div className="lightbox" onClick={() => setLightboxPhoto(null)}>
          <button className="lightbox-close" onClick={() => setLightboxPhoto(null)}>
            ×
          </button>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <img src={lightboxPhoto.imageData} alt={lightboxPhoto.title} />
            <div className="lightbox-info">
              <h3>{lightboxPhoto.title}</h3>
              <p>{lightboxPhoto.description}</p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default Gallery;
