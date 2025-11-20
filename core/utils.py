"""
Utility functions for the reporting system
"""

from django.conf import settings

def get_supabase_config():
    """
    Get Supabase configuration from settings
    """
    return {
        'url': settings.SUPABASE_URL,
        'key': settings.SUPABASE_KEY,
        'bucket': settings.SUPABASE_BUCKET,
    }

def validate_image_file(file_obj):
    """
    Validate that uploaded file is a valid image
    """
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    
    if not file_obj:
        return True  # Images are optional
    
    # Check file extension
    filename = file_obj.name.lower()
    file_ext = filename.split('.')[-1] if '.' in filename else ''
    
    if file_ext not in valid_extensions:
        return False
    
    # Check MIME type
    if file_obj.content_type not in valid_mime_types:
        return False
    
    # Check file size (5MB max)
    if file_obj.size > 5242880:
        return False
    
    return True

def format_timestamp(timestamp_str):
    """
    Format ISO timestamp for display
    """
    if not timestamp_str:
        return 'N/A'
    try:
        # Handle ISO format timestamps
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, AttributeError, TypeError):
        return timestamp_str
