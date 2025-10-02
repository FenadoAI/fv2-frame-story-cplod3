# Design System: Professional Photographer Portfolio

## Theme Selection

**USE CUSTOM THEME: Monochrome Gallery**

A minimal, monochromatic design system that creates a sophisticated gallery experience. The near-black and pure white palette ensures photography remains the hero, with subtle warm accents that complement without competing.

### Light Mode Colors
- **Background**: `hsl(0, 0%, 99%)` - Pure white canvas for images
- **Card**: `hsl(0, 0%, 100%)` - Crisp white
- **Primary**: `hsl(0, 0%, 8%)` - Deep charcoal for text and UI
- **Text**: `hsl(0, 0%, 12%)` - Primary text color
- **Muted**: `hsl(0, 0%, 96%)` - Subtle backgrounds
- **Border**: `hsl(0, 0%, 92%)` - Minimal dividers
- **Secondary**: `hsl(0, 0%, 18%)` - Secondary elements
- **Accent**: `hsl(30, 15%, 45%)` - Warm neutral accent for hover states

### Dark Mode Colors
- **Background**: `hsl(0, 0%, 6%)` - Near-black gallery backdrop
- **Card**: `hsl(0, 0%, 10%)` - Elevated surfaces
- **Primary**: `hsl(0, 0%, 95%)` - Light text on dark
- **Text**: `hsl(0, 0%, 92%)` - Primary text color
- **Muted**: `hsl(0, 0%, 12%)` - Subtle backgrounds
- **Border**: `hsl(0, 0%, 18%)` - Minimal dividers
- **Secondary**: `hsl(0, 0%, 85%)` - Secondary elements
- **Accent**: `hsl(30, 20%, 60%)` - Warm accent for interactions

### Preview Colors
- `hsl(0, 0%, 8%)`
- `hsl(0, 0%, 18%)`
- `hsl(30, 15%, 45%)`

## Foundations

### Typography
- **Primary Font**: Inter (clean, professional, excellent readability)
- **Display Font**: Playfair Display (elegant serif for photographer name/headers)
- **Scale**:
  - Hero/Display: 72px / 4.5rem (photographer name)
  - H1: 48px / 3rem (section headers)
  - H2: 32px / 2rem (subsections)
  - H3: 24px / 1.5rem (photo titles)
  - Body: 16px / 1rem (base text)
  - Small: 14px / 0.875rem (metadata, captions)
  - Tiny: 12px / 0.75rem (category tags)
- **Line Heights**: 1.6 for body, 1.2 for headings, 1.1 for display
- **Letter Spacing**: -0.02em for large headings, 0.01em for body, 0.05em for uppercase labels

### Spacing & Grid
- **Base Unit**: 8px
- **Scale**: 4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px
- **Container Max Width**: 1440px (allows breathing room for large images)
- **Content Max Width**: 1200px (for text sections)
- **Grid**: 12-column fluid grid
- **Gallery Gutter**: 16px (desktop), 8px (mobile)
- **Section Padding**: 128px vertical (desktop), 64px (tablet), 48px (mobile)

### Iconography
- **Library**: Lucide React (minimal, consistent line icons)
- **Size**: 20px default, 24px for prominent actions, 16px for inline
- **Stroke Width**: 1.5px (matches minimal aesthetic)
- **Style**: Line icons only, no fills

## Layout Patterns

### Hero Section
- **Height**: 100vh full-screen immersive entrance
- **Layout**: Full-bleed background image with centered photographer name
- **Overlay**: Subtle gradient overlay (black to transparent) for text readability
- **CTA**: Minimal "View Work" button with arrow icon

### Gallery Masonry
- **Columns**: 3 columns (desktop), 2 columns (tablet), 1 column (mobile)
- **Row Heights**: Dynamic based on image aspect ratio
- **Gaps**: 16px between images (desktop), 8px (mobile)
- **Hover State**: 20px lift, subtle shadow, photo details fade in

### About Section
- **Layout**: Split 40/60 (portrait image / text content)
- **Image**: Large portrait with subtle border
- **Text**: Left-aligned, generous line spacing

### Testimonials
- **Layout**: Centered carousel, single testimonial at a time
- **Max Width**: 800px for optimal readability
- **Quote Marks**: Large decorative quotes in accent color

### Contact Form
- **Layout**: Centered, single column, max-width 600px
- **Fields**: Minimal border-bottom style, no heavy boxes
- **Submit**: Full-width button with hover animation

## Animation & Micro-interactions

### Timing Functions
- **Ease In Out**: cubic-bezier(0.4, 0, 0.2, 1) - Default smooth
- **Ease Out**: cubic-bezier(0.0, 0, 0.2, 1) - Entrances
- **Ease In**: cubic-bezier(0.4, 0, 1, 1) - Exits
- **Spring**: cubic-bezier(0.34, 1.56, 0.64, 1) - Playful hovers

### Duration Scale
- **Instant**: 100ms - Button feedback
- **Fast**: 200ms - Hover states
- **Normal**: 400ms - Gallery transitions
- **Slow**: 600ms - Section reveals
- **Cinematic**: 1000ms - Hero entrance, parallax

### Interaction Patterns
- **Image Hover**: Scale 1.05, duration 400ms, ease-out
- **Button Hover**: Lift 2px, shadow increase, duration 200ms
- **Gallery Filter**: Fade out 300ms, shuffle positions, fade in 400ms with stagger
- **Scroll Reveal**: Fade in + translate up 30px, duration 600ms, stagger 100ms between items
- **Parallax**: Transform translateY based on scroll position, 0.3 factor
- **Zoom Transition**: Scale from 0.95 to 1.1, duration 800ms, overlay fade
- **Mobile Swipe**: Spring physics, velocity-based momentum

### Section Transitions
- **Fade**: Opacity 0 to 1, duration 1000ms
- **Slide Up**: TranslateY 50px to 0, with fade, duration 800ms
- **Scale Reveal**: Scale 0.9 to 1, with fade, duration 600ms

## Component Specifications

### Image Card
- **Border Radius**: 0px (sharp edges for gallery aesthetic)
- **Aspect Ratio**: Maintain original (no cropping)
- **Overlay**: Black gradient from bottom, opacity 0 to 0.8
- **Details Layer**: Title (H3), category tag, date
- **Hover State**: Overlay opacity increases, details fade in 300ms

### Button Styles
- **Primary**: Solid black background, white text, 48px height
- **Secondary**: Border 1px, transparent background, 44px height
- **Hover**: Primary scales 1.02, Secondary fills with accent color
- **Focus**: 2px outline with accent color

### Category Filter Pills
- **Default**: Border 1px, transparent, uppercase text, padding 8px 20px
- **Active**: Solid black background, white text
- **Hover**: Border color transitions to accent
- **Transition**: All properties 200ms ease

### Testimonial Card
- **Background**: Muted background color
- **Padding**: 48px
- **Quote Text**: H2 size, italic
- **Author**: Small text, regular weight
- **Quote Marks**: 120px decorative element, accent color, opacity 0.2

### Form Inputs
- **Style**: Border-bottom only, 2px thickness
- **Height**: 56px
- **Focus State**: Border color transitions to primary, width increases to 3px
- **Label**: Float up animation on focus
- **Validation**: Red border for errors, green for success

## Theming

### Dark Mode Triggers
- **User Toggle**: Manual switch in navigation
- **System Preference**: Respects prefers-color-scheme
- **Transition**: All colors transition over 400ms for smooth mode switch

### Color Mappings
- **Light to Dark**:
  - Background: 99% → 6% lightness
  - Text: 12% → 92% lightness (inverted)
  - Accent: Slightly warmer and brighter in dark mode
  - Shadows: Adjust from black to transparent whites

## Dark Mode & Color Contrast Rules (Critical)

- Always use explicit colors - never rely on browser defaults or component variants like 'variant="outline"'
- Force dark mode with CSS: 'html { color-scheme: dark; }' and 'meta name="color-scheme" content="dark"'
- Use high contrast ratios: minimum 4.5:1 for normal text, 3:1 for large text
- Override browser defaults with '!important' for form elements: 'input, textarea, select { background-color: hsl(0, 0%, 10%) !important; color: hsl(0, 0%, 92%) !important; border-color: hsl(0, 0%, 18%) !important; }'
- Test in both light and dark system modes - system dark mode can override custom styling
- Use semantic color classes instead of component variants: 'className="bg-card text-primary border border-border"' not 'variant="outline"'
- Create CSS custom properties for consistency across components
- Quick debugging: check if using 'variant="outline"', add explicit colors, use '!important' if needed, test system modes

### Color Contrast Checklist (apply to all components):
- [ ] No 'variant="outline"' or similar browser-dependent styles
- [ ] Explicit background and text colors specified
- [ ] High contrast ratios (4.5:1+ for text, 3:1+ for large text)
- [ ] Tested with system dark mode ON and OFF
- [ ] Form elements have forced dark styling
- [ ] Badges and buttons use custom classes, not default variants
- [ ] Placeholder text has proper contrast (hsl(0, 0%, 50%) minimum)
- [ ] Focus states are visible and accessible (2px outline, accent color)
- [ ] Gallery overlays provide sufficient contrast for photo details
- [ ] Category filter pills maintain contrast in all states

## Responsive Breakpoints

- **Mobile**: 320px - 767px (single column, touch-optimized)
- **Tablet**: 768px - 1023px (2 columns, hybrid interactions)
- **Desktop**: 1024px - 1439px (3 columns, full features)
- **Large Desktop**: 1440px+ (max container width, optimal viewing)

## Accessibility Notes

- All images require alt text describing the photograph
- Focus indicators on all interactive elements (2px accent outline)
- Keyboard navigation for gallery and filters
- Skip to content link for screen readers
- ARIA labels for icon-only buttons
- Reduced motion support: disable parallax and complex animations when prefers-reduced-motion is set
