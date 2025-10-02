# Photo Generation Guide

This guide explains how to generate AI-powered photos for the photography portfolio website.

## Quick Start

To generate fresh AI photos and populate the database:

```bash
cd backend
python seed_data_with_ai.py
```

## What This Does

The script will:
1. Generate 6 professional AI photos across 4 categories:
   - **Portrait**: Golden Hour Portrait, Urban Portrait
   - **Wedding**: Wedding Ceremony
   - **Landscape**: Mountain Landscape, Sunset Over Water
   - **Commercial**: Commercial Product Shot

2. Add 3 testimonials from sample clients
3. Set up the about content for "Alex Rivera"

## Generation Time

- Each photo takes ~5-10 seconds to generate
- Total time for 6 photos: ~1-2 minutes
- Images are stored as Google Cloud Storage URLs
- All photos are photorealistic and professionally styled

## Requirements

- Backend server must be running on port 8001
- `CODEXHUB_MCP_AUTH_TOKEN` must be set in `.env`
- `LITELLM_AUTH_TOKEN` must be set in `.env`

## Customization

To generate different photos, edit `seed_data_with_ai.py`:

```python
PHOTO_PROMPTS = [
    {
        "title": "Your Photo Title",
        "category": "portrait",  # or wedding, landscape, commercial
        "prompt": "Detailed description for AI to generate the image...",
        "description": "Caption shown in gallery",
        "featured": True,  # Shows on hero section
        "order": 1
    },
    # Add more photos...
]
```

## Troubleshooting

**Photos not generating:**
- Check that backend server is running: `curl http://localhost:8001/api/`
- Verify environment variables are set correctly
- Check logs for MCP authentication errors

**Placeholder images appearing:**
- This means image generation failed
- The script falls back to SVG placeholders
- Check `CODEXHUB_MCP_AUTH_TOKEN` is valid

## Old Script (SVG Placeholders)

The original `seed_data.py` script uses SVG placeholders instead of AI images:

```bash
python seed_data.py  # Use this for quick testing without AI
```

Use this for development/testing when you don't need real images.
