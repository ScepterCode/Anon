"""
Supabase client for reports app
"""
import uuid
import logging
from datetime import datetime
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client with credentials from Django settings"""
        from django.conf import settings
        
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.bucket = settings.SUPABASE_BUCKET
        
        # Validate credentials exist
        if not self.url or not self.key:
            logger.error("Missing Supabase credentials")
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in environment variables")
        
        # Check for placeholder values
        if self.url == 'https://example.supabase.co' or 'example' in self.url:
            logger.error("Supabase URL is still set to placeholder value")
            raise ValueError("Please configure your actual Supabase project URL")
        
        logger.info(f"Initializing Supabase client with URL: {self.url}")
        
        try:
            self.client: Client = create_client(self.url, self.key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to create Supabase client: {e}")
            raise
    
    def upload_file(self, file_obj):
        """
        Upload a file to Supabase Storage.
        Returns the public URL of the uploaded file.
        """
        try:
            # Generate unique filename
            ext = file_obj.name.split('.')[-1] if '.' in file_obj.name else 'jpg'
            filename = f"{uuid.uuid4()}.{ext}"
            
            # Read file content
            file_content = file_obj.read()
            
            logger.info(f"Uploading file: {filename} to bucket: {self.bucket}")
            
            # Upload to Supabase Storage
            self.client.storage.from_(self.bucket).upload(
                path=filename,
                file=file_content,
                file_options={"content-type": file_obj.content_type}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(filename)
            
            logger.info(f"File uploaded successfully: {public_url}")
            return public_url
            
        except Exception as e:
            logger.error(f"File upload error: {e}", exc_info=True)
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
            
            logger.info(f"Creating report with category: {category}")
            
            response = self.client.table('reports').insert(report_data).execute()
            
            if response.data:
                logger.info(f"Report created successfully with ID: {response.data[0].get('id')}")
                return response.data[0]
            else:
                logger.warning("Report creation returned no data")
                return None
                
        except Exception as e:
            logger.error(f"Database insert error: {e}", exc_info=True)
            return None
    
    def get_all_reports(self):
        """
        Fetch all reports from the database.
        """
        try:
            logger.info("Fetching all reports")
            response = self.client.table('reports').select('*').order('created_at', desc=True).execute()
            
            logger.info(f"Retrieved {len(response.data)} reports")
            return response.data
            
        except Exception as e:
            logger.error(f"Database fetch error: {e}", exc_info=True)
            return []
    
    def get_report(self, report_id):
        """
        Fetch a single report by ID.
        """
        try:
            logger.info(f"Fetching report with ID: {report_id}")
            response = self.client.table('reports').select('*').eq('id', report_id).execute()
            
            if response.data:
                logger.info(f"Report found: {report_id}")
                return response.data[0]
            else:
                logger.warning(f"Report not found: {report_id}")
                return None
                
        except Exception as e:
            logger.error(f"Database fetch error for report {report_id}: {e}", exc_info=True)
            return None
    
    def update_report_status(self, report_id, status):
        """
        Update the status of a report.
        """
        try:
            logger.info(f"Updating report {report_id} status to: {status}")
            response = self.client.table('reports').update({'status': status}).eq('id', report_id).execute()
            
            if response.data:
                logger.info(f"Report {report_id} status updated successfully")
                return response.data[0]
            else:
                logger.warning(f"Report {report_id} status update returned no data")
                return None
                
        except Exception as e:
            logger.error(f"Database update error for report {report_id}: {e}", exc_info=True)
            return None
    
    def delete_report(self, report_id):
        """
        Delete a report by ID.
        """
        try:
            logger.info(f"Deleting report with ID: {report_id}")
            self.client.table('reports').delete().eq('id', report_id).execute()
            
            logger.info(f"Report {report_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database delete error for report {report_id}: {e}", exc_info=True)
            return False


# Singleton instance
_supabase_instance = None
_supabase_url = None

def get_supabase_client():
    """
    Get or create Supabase client singleton.
    Resets the instance if URL changes (for hot reloading during development).
    """
    global _supabase_instance, _supabase_url
    
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
