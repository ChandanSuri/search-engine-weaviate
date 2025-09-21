import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_fake_products(query: str) -> List[Dict]:
    """Return fake product data for demonstration"""
    logger.info(f"Generating fake products for query: '{query}'")

    products = [
        {"id": "px1", "title": "Quantum Laptop - Model X", "brand": "TechCorp", "description": "The latest high-performance laptop with a quantum processor, perfect for developers and creators.", "color": "Cosmic Gray", "rating": 4.8},
        {"id": "px2", "title": "Stellar Smartwatch Series 7", "brand": "Gadgetron", "description": "A sleek smartwatch with advanced health tracking, GPS, and a vibrant always-on display.", "color": "Midnight Black", "rating": 4.6},
        {"id": "px3", "title": "Eco-Friendly Water Bottle", "brand": "GreenLife", "description": "Stay hydrated with our insulated, BPA-free water bottle made from 100% recycled materials.", "color": "Forest Green", "rating": 4.9},
        {"id": "px4", "title": "Advanced Gaming Mouse", "brand": "PixelPerfect", "description": "Gain a competitive edge with this ergonomic gaming mouse, featuring customizable RGB and a 16,000 DPI sensor.", "color": "RGB Fusion", "rating": 4.7},
        {"id": "px5", "title": "Nebula VR Headset", "brand": "Immersive Inc.", "description": "Experience virtual reality like never before with our 4K resolution VR headset.", "color": "Galaxy Purple", "rating": 4.5},
        {"id": "px6", "title": "Acoustic Pods Pro", "brand": "SoundWave", "description": "Crystal-clear audio with active noise cancellation in a compact form factor.", "color": "Arctic White", "rating": 4.8},
    ]

    logger.debug(f"Returning {len(products)} products")
    return products