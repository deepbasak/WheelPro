#!/usr/bin/env python
"""
Script to migrate existing images from local storage to Cloudinary.
This is useful when you're moving from local storage to Cloudinary.

Usage:
    1. Make sure your Cloudinary environment variables are set:
       - CLOUDINARY_CLOUD_NAME
       - CLOUDINARY_API_KEY
       - CLOUDINARY_API_SECRET
    
    2. Run this script:
       python migrate_to_cloudinary.py
"""

import os
import sys
import logging
from sqlalchemy import text
import cloudinary
import cloudinary.uploader
from app import app, db
from models import Product

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def initialize_cloudinary():
    """Initialize Cloudinary with credentials from environment variables."""
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )
    logger.info("Cloudinary initialized successfully")

def upload_to_cloudinary(local_path, public_id=None):
    """Upload a file to Cloudinary and return the URL."""
    if not os.path.exists(local_path):
        logger.warning(f"File does not exist: {local_path}")
        return None
    
    try:
        folder = "wheelrpo/wheels"
        options = {"folder": folder}
        if public_id:
            options["public_id"] = public_id
            
        result = cloudinary.uploader.upload(local_path, **options)
        return result['secure_url']
    except Exception as e:
        logger.error(f"Error uploading to Cloudinary: {e}")
        return None

def is_local_url(url):
    """Check if the URL is a local URL."""
    return url.startswith('/static/') or url.startswith('static/')

def get_local_path(url):
    """Convert a local URL to a filesystem path."""
    if url.startswith('/'):
        url = url[1:]  # Remove leading slash
    
    # Get the path relative to the app root
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), url)

def migrate_product_images():
    """Migrate all product images from local storage to Cloudinary."""
    logger.info("Starting migration of product images to Cloudinary")
    
    with app.app_context():
        # Get all products
        products = Product.query.all()
        logger.info(f"Found {len(products)} products to process")
        
        for product in products:
            logger.info(f"Processing product: {product.id} - {product.name}")
            
            # Process main image
            if product.main_image and is_local_url(product.main_image):
                local_path = get_local_path(product.main_image)
                logger.info(f"Uploading main image: {local_path}")
                
                cloudinary_url = upload_to_cloudinary(local_path)
                if cloudinary_url:
                    product.main_image = cloudinary_url
                    logger.info(f"Main image migrated to: {cloudinary_url}")
                else:
                    logger.warning(f"Failed to migrate main image for product {product.id}")
            
            # Process additional images
            if product.additional_images:
                new_additional_images = []
                
                for i, img_url in enumerate(product.additional_images):
                    if is_local_url(img_url):
                        local_path = get_local_path(img_url)
                        logger.info(f"Uploading additional image {i+1}: {local_path}")
                        
                        cloudinary_url = upload_to_cloudinary(local_path)
                        if cloudinary_url:
                            new_additional_images.append(cloudinary_url)
                            logger.info(f"Additional image migrated to: {cloudinary_url}")
                        else:
                            logger.warning(f"Failed to migrate additional image {i+1} for product {product.id}")
                    else:
                        # Image is already on Cloudinary or external service
                        new_additional_images.append(img_url)
                
                product.additional_images = new_additional_images
            
            # Save changes to database
            db.session.commit()
            logger.info(f"Successfully updated product {product.id}")
    
    logger.info("Migration completed successfully")

if __name__ == "__main__":
    # Check if Cloudinary credentials are set
    if not all([
        os.environ.get('CLOUDINARY_CLOUD_NAME'),
        os.environ.get('CLOUDINARY_API_KEY'),
        os.environ.get('CLOUDINARY_API_SECRET')
    ]):
        logger.error("Cloudinary environment variables are not set. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET.")
        sys.exit(1)
    
    # Initialize Cloudinary
    initialize_cloudinary()
    
    # Migrate product images
    migrate_product_images()
