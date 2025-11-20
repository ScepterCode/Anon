"""
Quick Start Guide for Anonymous Reporting System
"""

# ============================================================================
# STEP 1: SETUP ENVIRONMENT
# ============================================================================

# 1.1 Create virtual environment
# Windows:
#   python -m venv venv
#   venv\Scripts\activate
# 
# Mac/Linux:
#   python3 -m venv venv
#   source venv/bin/activate

# 1.2 Install dependencies
#   pip install -r requirements.txt

# ============================================================================
# STEP 2: CONFIGURE SUPABASE
# ============================================================================

# 2.1 Create Supabase Project
# Visit https://supabase.com and create a new project

# 2.2 Create Database Table
# In Supabase SQL Editor, run:
"""
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  description TEXT NOT NULL,
  image_url TEXT,
  category TEXT,
  location TEXT,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT now()
);
"""

# 2.3 Create Storage Bucket
# - Go to Storage
# - Create new bucket named "report_uploads"
# - Make it public

# 2.4 Enable RLS (Optional but recommended)
# In the reports table, enable Row Level Security
"""
CREATE POLICY "Allow public insert" ON reports
FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow authenticated select" ON reports
FOR SELECT USING (auth.role() = 'authenticated');
"""

# ============================================================================
# STEP 3: ENVIRONMENT VARIABLES
# ============================================================================

# 3.1 Copy and configure .env file
#   cp .env.example .env

# 3.2 Get your Supabase credentials:
# - SUPABASE_URL: Your project URL (Settings > API)
# - SUPABASE_KEY: Your anon key (Settings > API)

# 3.3 Generate Django SECRET_KEY:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# ============================================================================
# STEP 4: RUN DJANGO
# ============================================================================

# 4.1 Create superuser for admin panel
#   python manage.py createsuperuser
# OR use the custom command:
#   python manage.py create_superuser --username admin --password mypassword

# 4.2 Start development server
#   python manage.py runserver

# ============================================================================
# STEP 5: ACCESS THE SYSTEM
# ============================================================================

# User Submission Form:
#   http://localhost:8000/reports/submit/

# Admin Dashboard:
#   http://localhost:8000/admin/login/
#   Login with superuser credentials

# ============================================================================
# STEP 6: DEPLOYMENT (PRODUCTION)
# ============================================================================

# 6.1 Update Django settings
#   - Set DEBUG=False
#   - Update SECRET_KEY
#   - Configure ALLOWED_HOSTS
#   - Set SESSION_COOKIE_SECURE=True
#   - Use HTTPS

# 6.2 Deploy with Gunicorn
#   pip install gunicorn
#   gunicorn core.wsgi:application --bind 0.0.0.0:8000

# 6.3 Use a process manager (systemd, supervisor, etc.)

# 6.4 Set up SSL with Let's Encrypt
#   - Use Nginx or Apache as reverse proxy
#   - Configure SSL certificate

# ============================================================================
# USEFUL COMMANDS
# ============================================================================

# Create a new superuser:
#   python manage.py createsuperuser

# Run development server:
#   python manage.py runserver

# Collect static files (for production):
#   python manage.py collectstatic

# Check for security issues:
#   python manage.py check --deploy

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Issue: "ModuleNotFoundError: No module named 'django'"
# Solution: Activate virtual environment and install requirements
#   pip install -r requirements.txt

# Issue: "Supabase connection error"
# Solution: Check SUPABASE_URL and SUPABASE_KEY in .env file

# Issue: "File upload fails"
# Solution: 
#   - Check bucket name is "report_uploads"
#   - Ensure bucket is public
#   - Check file size (max 5MB)

# Issue: "Admin login fails"
# Solution:
#   - Ensure user is a superuser (is_staff=True)
#   - Reset password: python manage.py changepassword username
#   - Check database connection

# ============================================================================
# CUSTOMIZATION EXAMPLES
# ============================================================================

# Add more status options:
# 1. Update adminpanel/templates/report_detail.html (add new button)
# 2. Update adminpanel/views.py (update status validation)
# 3. Update database if needed

# Add new report fields:
# 1. Update Supabase table schema (ALTER TABLE reports ADD COLUMN ...)
# 2. Add field to reports/forms.py
# 3. Update templates to display field
# 4. Update supabase_client.py to handle new field

# ============================================================================
# SECURITY CHECKLIST FOR PRODUCTION
# ============================================================================

# [ ] Set DEBUG=False in .env
# [ ] Generate random SECRET_KEY
# [ ] Configure ALLOWED_HOSTS
# [ ] Use HTTPS (SSL certificate)
# [ ] Set SESSION_COOKIE_SECURE=True
# [ ] Set CSRF_COOKIE_SECURE=True
# [ ] Enable HSTS (optional)
# [ ] Set up database backups
# [ ] Configure Supabase RLS policies
# [ ] Monitor application logs
# [ ] Set up rate limiting on submission endpoint
# [ ] Use strong superuser password
# [ ] Consider 2FA for admin panel

# ============================================================================
