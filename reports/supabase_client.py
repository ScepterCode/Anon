"""
Supabase client for reports app
"""
import os
import uuid
import logging
from datetime import datetime
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        # Get from Django settings instead of os.getenv for better reliability
        from django.conf import settings
        
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.bucket = settings.SUPABASE_BUCKET
        
        logger.info(f"Initializing Supabase client with URL: {self.url}")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
        
        if self.url == 'https://dxggngekixmxghldgwpq.supabase.co':
            raise ValueError("Please configure your Supabase credentials in .env file")
        
        self.client: Client = create_client(self.url, self.key)
    
    def upload_file(self, file_obj):
        """
        Upload a file to Supabase Storage.
        Returns the public URL of the uploaded file.
        """
        try:
            # Generate unique filename
            ext = file_obj.name.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            
            # Read file content
            file_content = file_obj.read()
            
            # Upload to Supabase Storage
            self.client.storage.from_(self.bucket).upload(
                path=filename,
                file=file_content,
                file_options={"content-type": file_obj.content_type}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(filename)
            
            return public_url
        except Exception as e:
            logger.error(f"File upload error: {e}")
            return None
    
    def create_report(self, description, category=None, location=None, image_url=None, username=None):
        """
        Insert a report into the Supabase database.
        """
        try:
            report_data = {
                'id': str(uuid.uuid4()),
                'description': description,
                'category': category,
                'location': location,
                'image_url': image_url,
                'username': username,
                'status': 'new',
                'created_at': datetime.utcnow().isoformat(),
            }
            
            response = self.client.table('reports').insert(report_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Database insert error: {e}")
            return None
    
    def get_all_reports(self):
        """
        Fetch all reports from the database.
        """
        try:
            response = self.client.table('reports').select('*').order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"Database fetch error: {e}")
            return []
    
    def get_report(self, report_id):
        """
        Fetch a single report by ID.
        """
        try:
            response = self.client.table('reports').select('*').eq('id', report_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Database fetch error for report {report_id}: {e}")
            return None
    
    def update_report_status(self, report_id, status):
        """
        Update the status of a report.
        """
        try:
            response = self.client.table('reports').update({'status': status}).eq('id', report_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Database update error for report {report_id}: {e}")
            return None
    
    def delete_report(self, report_id):
        """
        Delete a report by ID.
        """
        try:
            self.client.table('reports').delete().eq('id', report_id).execute()
            return True
        except Exception as e:
            logger.error(f"Database delete error for report {report_id}: {e}")
            return False

# Singleton instance
_supabase_instance = None
_supabase_url = None

def get_supabase_client():  # noqa: PLW0603
    global _supabase_instance, _supabase_url  # noqa: PLW0603
    
    # Get current URL from settings
    from django.conf import settings
    current_url = settings.SUPABASE_URL
    
    # Reset singleton if URL changed (e.g., after .env update)
    if _supabase_instance is not None and _supabase_url != current_url:
        logger.info(f"Supabase URL changed from {_supabase_url} to {current_url}, resetting client")
        _supabase_instance = None
    
    # Create new instance if needed
    if _supabase_instance is None:
        _supabase_instance = SupabaseClient()
        _supabase_url = current_url
    
    return _supabase_instance

def __init__(self):
    # Get from Django settings instead of os.getenv for better reliability
    from django.conf import settings
    
    self.url = settings.SUPABASE_URL
    self.key = settings.SUPABASE_KEY
    self.bucket = settings.SUPABASE_BUCKET
    
    # DEBUG - Remove after fixing
    logger.info(f"Initializing Supabase client with URL: {self.url}")
    logger.info(f"Supabase KEY exists: {bool(self.key)}")
    logger.info(f"Supabase KEY length: {len(self.key) if self.key else 0}")
    
    if not self.url or not self.key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
    
    if self.url == 'https://example.supabase.co':
        raise ValueError("Please configure your Supabase credentials in .env file")
    
    self.client: Client = create_client(self.url, self.key)
