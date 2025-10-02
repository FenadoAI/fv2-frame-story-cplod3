#!/usr/bin/env python3
"""Seed script to populate database with sample photography portfolio data."""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8001")

# Sample photos (using placeholder base64 images)
SAMPLE_PHOTOS = [
    {
        "title": "Golden Hour Portrait",
        "category": "portrait",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad1' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23d4a373;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%238b5a3c;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad1)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-family='serif' font-size='40' opacity='0.6'%3EGolden Hour%3C/text%3E%3C/svg%3E",
        "description": "A stunning portrait captured during golden hour",
        "featured": True,
        "order": 1
    },
    {
        "title": "Mountain Landscape",
        "category": "landscape",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad2' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%234a5568;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%232d3748;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad2)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-family='serif' font-size='40' opacity='0.6'%3EMountains%3C/text%3E%3C/svg%3E",
        "description": "Majestic mountain ranges at dawn",
        "featured": False,
        "order": 2
    },
    {
        "title": "Wedding Ceremony",
        "category": "wedding",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad3' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23f7fafc;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23e2e8f0;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad3)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%23718096' font-family='serif' font-size='40' opacity='0.8'%3EWedding%3C/text%3E%3C/svg%3E",
        "description": "Beautiful wedding moments captured",
        "featured": False,
        "order": 3
    },
    {
        "title": "Commercial Product Shot",
        "category": "commercial",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad4' x1='0%25' y1='0%25' x2='100%25' y2='0%25'%3E%3Cstop offset='0%25' style='stop-color:%23171717;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23262626;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad4)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-family='serif' font-size='40' opacity='0.6'%3EProduct%3C/text%3E%3C/svg%3E",
        "description": "Professional commercial photography",
        "featured": False,
        "order": 4
    },
    {
        "title": "Urban Portrait",
        "category": "portrait",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad5' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23667eea;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23764ba2;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad5)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-family='serif' font-size='40' opacity='0.6'%3EUrban%3C/text%3E%3C/svg%3E",
        "description": "Street portrait with urban backdrop",
        "featured": False,
        "order": 5
    },
    {
        "title": "Sunset Over Water",
        "category": "landscape",
        "imageData": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Cdefs%3E%3ClinearGradient id='grad6' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23ff6b6b;stop-opacity:1' /%3E%3Cstop offset='50%25' style='stop-color:%23f9a826;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%234a5568;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad6)' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-family='serif' font-size='40' opacity='0.6'%3ESunset%3C/text%3E%3C/svg%3E",
        "description": "Breathtaking sunset over calm waters",
        "featured": False,
        "order": 6
    }
]

# Sample testimonials
SAMPLE_TESTIMONIALS = [
    {
        "clientName": "Sarah Johnson",
        "testimonialText": "Absolutely stunning work! The photographer captured our wedding day perfectly. Every moment was beautifully documented and we couldn't be happier with the results.",
        "rating": 5,
        "order": 1
    },
    {
        "clientName": "Michael Chen",
        "testimonialText": "Professional, creative, and a pleasure to work with. The portrait session was relaxed and fun, and the final images exceeded all expectations.",
        "rating": 5,
        "order": 2
    },
    {
        "clientName": "Emily Rodriguez",
        "testimonialText": "Incredible eye for detail and lighting. Our commercial product shots look amazing and have really elevated our brand presence. Highly recommend!",
        "rating": 5,
        "order": 3
    }
]

def seed_photos():
    """Seed photos into database."""
    print("\n=== Seeding Photos ===")
    for photo in SAMPLE_PHOTOS:
        try:
            response = requests.post(f"{API_BASE}/api/photos", json=photo)
            if response.status_code == 200:
                print(f"✅ Created: {photo['title']} ({photo['category']})")
            else:
                print(f"❌ Failed to create {photo['title']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error creating {photo['title']}: {str(e)}")

def seed_testimonials():
    """Seed testimonials into database."""
    print("\n=== Seeding Testimonials ===")
    for testimonial in SAMPLE_TESTIMONIALS:
        try:
            response = requests.post(f"{API_BASE}/api/testimonials", json=testimonial)
            if response.status_code == 200:
                print(f"✅ Created testimonial from: {testimonial['clientName']}")
            else:
                print(f"❌ Failed to create testimonial: {response.status_code}")
        except Exception as e:
            print(f"❌ Error creating testimonial: {str(e)}")

def seed_about():
    """Update about content."""
    print("\n=== Seeding About Content ===")
    about_data = {
        "photographerName": "Alex Rivera",
        "tagline": "Capturing Life's Beautiful Moments",
        "bioText": "With over 10 years of experience in photography, I specialize in portraits, weddings, and landscape photography. My approach combines technical expertise with creative vision to create images that tell your story. Every photograph is an opportunity to capture something extraordinary, and I'm passionate about helping you preserve your most important moments."
    }

    try:
        response = requests.put(f"{API_BASE}/api/about", json=about_data)
        if response.status_code == 200:
            print(f"✅ Updated about content for: {about_data['photographerName']}")
        else:
            print(f"❌ Failed to update about content: {response.status_code}")
    except Exception as e:
        print(f"❌ Error updating about content: {str(e)}")

def main():
    """Run all seed functions."""
    print(f"Seeding data to API at: {API_BASE}")

    try:
        # Test connection
        response = requests.get(f"{API_BASE}/api/")
        if response.status_code != 200:
            print(f"❌ Cannot connect to API at {API_BASE}")
            print("Make sure the backend server is running")
            sys.exit(1)

        # Seed data
        seed_photos()
        seed_testimonials()
        seed_about()

        print("\n" + "="*50)
        print("🎉 SEEDING COMPLETE!")
        print("="*50)
        print("\nYour portfolio website is now populated with sample data.")
        print("Visit the website to see the results!")
        return 0

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API at {API_BASE}")
        print("Make sure the backend server is running")
        return 1
    except Exception as e:
        print(f"\n❌ Seeding error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
