import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
import logging

# Set up logging
logger = logging.getLogger(__name__)

def initialize_cloudinary():
    """Initialize Cloudinary with credentials from environment variables."""
    try:
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            secure=True
        )
        logger.info("Cloudinary initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Cloudinary: {str(e)}")
        raise

def upload_file(file, folder="uploads", resource_type="image"):
    """
    Upload a file to Cloudinary
    
    Args:
        file: File object to upload
        folder: Cloudinary folder to store the file
        resource_type: Type of resource ('image', 'video', 'raw')
        
    Returns:
        Dictionary with upload result including public_id and url
    """
    try:
        if not file:
            logger.warning("No file provided for upload")
            return None
            
        upload_result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type=resource_type
        )
        logger.info(f"File uploaded successfully to Cloudinary: {upload_result['public_id']}")
        return upload_result
    except Exception as e:
        logger.error(f"Error uploading file to Cloudinary: {str(e)}")
        return None

def upload_local_file(file_path, folder="uploads", resource_type="image"):
    """
    Upload a local file to Cloudinary
    
    Args:
        file_path: Path to the local file
        folder: Cloudinary folder to store the file
        resource_type: Type of resource ('image', 'video', 'raw')
        
    Returns:
        Dictionary with upload result including public_id and url
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Local file not found: {file_path}")
            return None
            
        upload_result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type=resource_type
        )
        logger.info(f"Local file uploaded successfully: {upload_result['public_id']}")
        return upload_result
    except Exception as e:
        logger.error(f"Error uploading local file to Cloudinary: {str(e)}")
        return None

def delete_file(public_id, resource_type="image"):
    """
    Delete a file from Cloudinary
    
    Args:
        public_id: The public_id of the file to delete
        resource_type: Type of resource ('image', 'video', 'raw')
        
    Returns:
        Dictionary with deletion result
    """
    try:
        deletion_result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        logger.info(f"File deleted from Cloudinary: {public_id}")
        return deletion_result
    except Exception as e:
        logger.error(f"Error deleting file from Cloudinary: {str(e)}")
        return None

def get_url(public_id, **options):
    """
    Get the URL of a file stored in Cloudinary
    
    Args:
        public_id: The public_id of the file
        options: Additional transformations or options
        
    Returns:
        String URL to the file
    """
    try:
        url = cloudinary.CloudinaryImage(public_id).build_url(**options)
        return url
    except Exception as e:
        logger.error(f"Error getting URL for file {public_id}: {str(e)}")
        return None
