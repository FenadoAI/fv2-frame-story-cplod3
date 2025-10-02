#!/usr/bin/env python3
"""Test script for photography API endpoints."""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8001")

def test_photos_api():
    """Test photo CRUD operations."""
    print("\n=== Testing Photos API ===")

    # Create a photo
    print("\n1. Creating a test photo...")
    photo_data = {
        "title": "Sunset Portrait",
        "category": "portrait",
        "imageData": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        "description": "Beautiful sunset portrait session",
        "featured": True,
        "order": 1
    }

    response = requests.post(f"{API_BASE}/api/photos", json=photo_data)
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    photo = response.json()
    photo_id = photo["id"]
    print(f"Created photo: {photo['title']} (ID: {photo_id})")

    # Get all photos
    print("\n2. Fetching all photos...")
    response = requests.get(f"{API_BASE}/api/photos")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    photos = response.json()
    print(f"Found {len(photos)} photo(s)")

    # Filter by category
    print("\n3. Filtering photos by category 'portrait'...")
    response = requests.get(f"{API_BASE}/api/photos?category=portrait")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    portrait_photos = response.json()
    print(f"Found {len(portrait_photos)} portrait photo(s)")

    # Update photo
    print("\n4. Updating photo title...")
    update_data = {"title": "Golden Hour Portrait"}
    response = requests.put(f"{API_BASE}/api/photos/{photo_id}", json=update_data)
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    updated_photo = response.json()
    print(f"Updated title: {updated_photo['title']}")

    # Delete photo
    print("\n5. Deleting photo...")
    response = requests.delete(f"{API_BASE}/api/photos/{photo_id}")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    result = response.json()
    print(f"Result: {result['message']}")

    print("\n✅ Photos API tests passed!")
    return True


def test_testimonials_api():
    """Test testimonials API."""
    print("\n=== Testing Testimonials API ===")

    # Create testimonial
    print("\n1. Creating a test testimonial...")
    testimonial_data = {
        "clientName": "John Doe",
        "testimonialText": "Amazing photographer! Captured our wedding perfectly.",
        "rating": 5,
        "order": 1
    }

    response = requests.post(f"{API_BASE}/api/testimonials", json=testimonial_data)
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    testimonial = response.json()
    print(f"Created testimonial from: {testimonial['clientName']}")

    # Get all testimonials
    print("\n2. Fetching all testimonials...")
    response = requests.get(f"{API_BASE}/api/testimonials")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    testimonials = response.json()
    print(f"Found {len(testimonials)} testimonial(s)")

    print("\n✅ Testimonials API tests passed!")
    return True


def test_contact_api():
    """Test contact inquiry API."""
    print("\n=== Testing Contact API ===")

    # Submit inquiry
    print("\n1. Submitting contact inquiry...")
    inquiry_data = {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "555-1234",
        "message": "I'd like to book a portrait session next month."
    }

    response = requests.post(f"{API_BASE}/api/contact", json=inquiry_data)
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    inquiry = response.json()
    print(f"Created inquiry from: {inquiry['name']} ({inquiry['email']})")

    # Get all inquiries
    print("\n2. Fetching all contact inquiries...")
    response = requests.get(f"{API_BASE}/api/contact/inquiries")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    inquiries = response.json()
    print(f"Found {len(inquiries)} inquiry(ies)")

    print("\n✅ Contact API tests passed!")
    return True


def test_about_api():
    """Test about content API."""
    print("\n=== Testing About API ===")

    # Get default about content
    print("\n1. Fetching about content...")
    response = requests.get(f"{API_BASE}/api/about")
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    about = response.json()
    print(f"Photographer: {about['photographerName']}")
    print(f"Tagline: {about['tagline']}")

    # Update about content
    print("\n2. Updating about content...")
    update_data = {
        "photographerName": "Alex Johnson",
        "tagline": "Capturing Your Story Through My Lens",
        "bioText": "Professional photographer with 10+ years of experience in portrait and wedding photography."
    }

    response = requests.put(f"{API_BASE}/api/about", json=update_data)
    print(f"Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return False

    updated_about = response.json()
    print(f"Updated photographer: {updated_about['photographerName']}")

    print("\n✅ About API tests passed!")
    return True


def main():
    """Run all tests."""
    print(f"Testing API at: {API_BASE}")

    try:
        # Test connection
        print("\nTesting API connection...")
        response = requests.get(f"{API_BASE}/api/")
        if response.status_code != 200:
            print(f"❌ Cannot connect to API at {API_BASE}")
            print("Make sure the backend server is running:")
            print("  cd backend && uvicorn server:app --reload --port 8001")
            sys.exit(1)
        print("✅ API connection successful")

        # Run tests
        all_passed = True
        all_passed &= test_photos_api()
        all_passed &= test_testimonials_api()
        all_passed &= test_contact_api()
        all_passed &= test_about_api()

        if all_passed:
            print("\n" + "="*50)
            print("🎉 ALL TESTS PASSED!")
            print("="*50)
            return 0
        else:
            print("\n" + "="*50)
            print("❌ SOME TESTS FAILED")
            print("="*50)
            return 1

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API at {API_BASE}")
        print("Make sure the backend server is running:")
        print("  cd backend && uvicorn server:app --reload --port 8001")
        return 1
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
