# Photographer Portfolio Website - Implementation Plan

**Requirement ID**: 3cd6e3d1-28d2-437b-8bc2-bdb7460bb264

## Design System
✅ Created at `plan/design-system.md`

## Backend Implementation

### Database Collections

**1. photos**
```
{
  _id: ObjectId,
  title: String,
  category: String (portrait/wedding/landscape/commercial),
  imageData: String (base64),
  description: String,
  featured: Boolean,
  order: Number,
  createdAt: DateTime
}
```

**2. testimonials**
```
{
  _id: ObjectId,
  clientName: String,
  testimonialText: String,
  rating: Number (1-5),
  order: Number,
  createdAt: DateTime
}
```

**3. contact_inquiries**
```
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String (optional),
  message: String,
  submittedAt: DateTime,
  status: String (new/contacted/closed)
}
```

### API Endpoints

**Photo Management**
- `GET /api/photos` - Get all photos (with optional category filter)
- `POST /api/photos` - Create new photo (admin)
- `PUT /api/photos/{id}` - Update photo (admin)
- `DELETE /api/photos/{id}` - Delete photo (admin)

**Testimonials**
- `GET /api/testimonials` - Get all testimonials
- `POST /api/testimonials` - Create testimonial (admin)

**Contact Form**
- `POST /api/contact` - Submit contact inquiry
- `GET /api/contact/inquiries` - Get all inquiries (admin)

**About Content**
- `GET /api/about` - Get photographer bio/about text
- `PUT /api/about` - Update about content (admin)

## Frontend Implementation

### Page Structure (Single Page Application)

**1. Hero Section**
- Full-screen immersive entrance
- Featured photo background with gradient overlay
- Photographer name (h1) + tagline
- Scroll indicator animation

**2. Gallery Section**
- Category filter pills (All, Portrait, Wedding, Landscape, Commercial)
- Masonry layout (3 columns desktop, 2 tablet, 1 mobile)
- Image cards with hover effects:
  - Scale zoom (1.05)
  - Overlay with title + category
- Lightbox modal for full-screen view
- Lazy loading with scroll-triggered reveals

**3. About Section**
- Split layout (40% image, 60% text)
- Photographer portrait on left
- Bio text with emphasis on style/approach
- Parallax effect on portrait

**4. Testimonials Section**
- Carousel/slider with 3-dot pagination
- Animated pull quote styling
- Client name + rating display
- Auto-rotate with pause on hover

**5. Contact Section**
- Minimal form (600px max-width)
- Fields: Name, Email, Phone (optional), Message
- Success/error messaging
- Submit button with loading state

### Key Features

**Animations**
- Scroll-triggered fade + translate (IntersectionObserver)
- Parallax on about section portrait
- Smooth zoom transitions on gallery items
- Cinematic fade between filtered categories
- Mobile swipe for testimonial carousel

**Responsive Behavior**
- Masonry: 3/2/1 columns
- Touch-friendly tap areas (44px minimum)
- Swipe gestures for mobile gallery/testimonials
- Optimized image loading

**Accessibility**
- Semantic HTML structure
- Alt text for all images
- Keyboard navigation support
- Focus states on interactive elements
- ARIA labels where needed

## Testing Strategy

**Backend Tests**
1. API endpoint connectivity
2. Photo CRUD operations with base64 storage
3. Contact form submission
4. Testimonial retrieval

**Frontend Tests**
1. Gallery filtering functionality
2. Image loading and display
3. Form validation and submission
4. Responsive layout breakpoints

## Success Metrics
- Contact form submission tracking
- Mobile/desktop usage analytics
- Gallery interaction rates
