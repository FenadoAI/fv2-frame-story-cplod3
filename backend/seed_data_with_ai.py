#!/usr/bin/env python3
"""Seed script to populate database with AI-generated photography portfolio data."""

import os
import sys
import asyncio
import requests
from dotenv import load_dotenv

# Add backend to path to import ai_agents
sys.path.insert(0, os.path.dirname(__file__))

from ai_agents import ImageAgent, AgentConfig

# Load environment
load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8001")

# Photo prompts for AI generation
PHOTO_PROMPTS = [
    {
        "title": "Golden Hour Portrait",
        "category": "portrait",
        "prompt": "A professional portrait of a person during golden hour, warm lighting, soft focus background, natural outdoor setting, photorealistic",
        "description": "A stunning portrait captured during golden hour",
        "featured": True,
        "order": 1
    },
    {
        "title": "Mountain Landscape",
        "category": "landscape",
        "prompt": "Majestic snow-capped mountain ranges at dawn, dramatic sky with clouds, alpine landscape, photorealistic nature photography",
        "description": "Majestic mountain ranges at dawn",
        "featured": False,
        "order": 2
    },
    {
        "title": "Wedding Ceremony",
        "category": "wedding",
        "prompt": "Elegant wedding ceremony moment, bride and groom at altar, romantic lighting, flower decorations, photorealistic wedding photography",
        "description": "Beautiful wedding moments captured",
        "featured": False,
        "order": 3
    },
    {
        "title": "Commercial Product Shot",
        "category": "commercial",
        "prompt": "Professional commercial product photography, luxury watch on black background, studio lighting, high-end advertising style, photorealistic",
        "description": "Professional commercial photography",
        "featured": False,
        "order": 4
    },
    {
        "title": "Urban Portrait",
        "category": "portrait",
        "prompt": "Street portrait with urban city backdrop, fashionable person, urban graffiti wall, natural lighting, photorealistic street photography",
        "description": "Street portrait with urban backdrop",
        "featured": False,
        "order": 5
    },
    {
        "title": "Sunset Over Water",
        "category": "landscape",
        "prompt": "Breathtaking sunset over calm ocean waters, colorful sky with orange and pink hues, peaceful seascape, photorealistic landscape photography",
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

async def generate_image(image_agent: ImageAgent, prompt: str) -> str:
    """Generate an image using AI and return the URL."""
    try:
        print(f"   Generating: {prompt[:60]}...")
        result = await image_agent.generate_image_structured(prompt)

        if result.success and result.image_url:
            print(f"   ✅ Image generated: {result.image_url[:80]}...")
            return result.image_url
        else:
            print(f"   ⚠️  Image generation failed: {result.description}")
            # Return a placeholder SVG as fallback
            return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Crect fill='%23ccc' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='30'%3EImage Generation Failed%3C/text%3E%3C/svg%3E"
    except Exception as e:
        print(f"   ❌ Error generating image: {str(e)}")
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='1000'%3E%3Crect fill='%23ccc' width='800' height='1000'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='30'%3EImage Generation Failed%3C/text%3E%3C/svg%3E"

async def seed_photos_with_ai():
    """Seed photos into database with AI-generated images."""
    print("\n=== Seeding Photos with AI Generation ===")

    # Initialize ImageAgent
    config = AgentConfig()
    image_agent = ImageAgent(config)

    for photo_spec in PHOTO_PROMPTS:
        try:
            print(f"\n📸 Creating: {photo_spec['title']} ({photo_spec['category']})")

            # Generate image using AI
            image_url = await generate_image(image_agent, photo_spec["prompt"])

            # Create photo data
            photo_data = {
                "title": photo_spec["title"],
                "category": photo_spec["category"],
                "imageData": image_url,
                "description": photo_spec["description"],
                "featured": photo_spec["featured"],
                "order": photo_spec["order"]
            }

            # Send to API
            response = requests.post(f"{API_BASE}/api/photos", json=photo_data)
            if response.status_code == 200:
                print(f"✅ Saved to database: {photo_spec['title']}")
            else:
                print(f"❌ Failed to save {photo_spec['title']}: {response.status_code}")

        except Exception as e:
            print(f"❌ Error creating {photo_spec['title']}: {str(e)}")

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

async def seed_about():
    """Update about content with portrait."""
    print("\n=== Seeding About Content ===")

    # Generate portrait
    print("Generating photographer portrait...")
    config = AgentConfig()
    image_agent = ImageAgent(config)

    portrait_prompt = "Professional photographer portrait, middle-aged person with camera, warm friendly smile, professional studio lighting, neutral background, photorealistic headshot"
    result = await image_agent.generate_image_structured(portrait_prompt)

    portrait_url = ""
    if result.success and result.image_url:
        portrait_url = result.image_url
        print(f"✅ Portrait generated: {portrait_url[:80]}...")
    else:
        print(f"⚠️  Portrait generation failed, using placeholder")

    about_data = {
        "photographerName": "Alex Rivera",
        "tagline": "Capturing Life's Beautiful Moments",
        "bioText": "With over 10 years of experience in photography, I specialize in portraits, weddings, and landscape photography. My approach combines technical expertise with creative vision to create images that tell your story. Every photograph is an opportunity to capture something extraordinary, and I'm passionate about helping you preserve your most important moments.",
        "portraitImage": portrait_url
    }

    try:
        response = requests.put(f"{API_BASE}/api/about", json=about_data)
        if response.status_code == 200:
            print(f"✅ Updated about content for: {about_data['photographerName']}")
        else:
            print(f"❌ Failed to update about content: {response.status_code}")
    except Exception as e:
        print(f"❌ Error updating about content: {str(e)}")

async def main():
    """Run all seed functions."""
    print(f"Seeding data to API at: {API_BASE}")
    print("This will generate real AI images for the photography portfolio.")
    print("⏳ This may take 1-2 minutes depending on image generation service...")

    try:
        # Test connection
        response = requests.get(f"{API_BASE}/api/")
        if response.status_code != 200:
            print(f"❌ Cannot connect to API at {API_BASE}")
            print("Make sure the backend server is running")
            sys.exit(1)

        # Seed data with AI-generated images
        await seed_photos_with_ai()
        seed_testimonials()
        await seed_about()

        print("\n" + "="*50)
        print("🎉 SEEDING COMPLETE!")
        print("="*50)
        print("\nYour portfolio website is now populated with AI-generated photography!")
        print("Visit the website to see the results!")
        return 0

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API at {API_BASE}")
        print("Make sure the backend server is running")
        return 1
    except Exception as e:
        print(f"\n❌ Seeding error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
