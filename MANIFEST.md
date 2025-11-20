"""
COMPLETE PROJECT SUMMARY
Anonymous Reporting System - Django + Supabase
"""

# ============================================================================
# PROJECT OVERVIEW
# ============================================================================

This is a production-ready anonymous reporting system built with:
  - Django (backend framework)
  - Supabase (database + storage)
  - Bootstrap 5 (responsive UI)
  - No React, TypeScript, or Django Admin

The system allows anonymous users to submit reports with optional images,
and provides a custom admin dashboard for managing reports.

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

project/
│
├── core/                              # Django project configuration
│   ├── __init__.py
│   ├── settings.py                   # Main Django settings
│   ├── urls.py                       # Root URL configuration
│   ├── wsgi.py                       # WSGI application
│   ├── asgi.py                       # ASGI application
│   ├── utils.py                      # Utility functions
│   └── management/
│       └── commands/
│           └── create_superuser.py   # Custom command to create admin
│
├── reports/                           # Anonymous report submission app
│   ├── __init__.py
│   ├── views.py                      # Views for report submission
│   ├── forms.py                      # Django form validation
│   ├── urls.py                       # App URL routes
│   ├── apps.py                       # App configuration
│   ├── supabase_client.py            # Supabase integration
│   └── templates/
│       ├── report_form.html          # Submission form
│       └── report_submitted.html     # Success page
│
├── adminpanel/                        # Admin dashboard app
│   ├── __init__.py
│   ├── views.py                      # Admin views
│   ├── urls.py                       # Admin routes
│   ├── apps.py                       # App configuration
│   ├── decorators.py                 # Authentication decorators
│   └── templates/
│       ├── admin_login.html          # Login page
│       ├── admin_dashboard.html      # Reports table
│       ├── report_detail.html        # Report details
│       └── 404.html                  # Error page
│
├── static/                            # Static files (CSS, JS, images)
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── README.md                          # Full documentation
├── QUICKSTART.md                      # Quick start guide
├── API.md                             # API documentation
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker compose for dev
└── MANIFEST.md                        # This file

# ============================================================================
# QUICK START (5 MINUTES)
# ============================================================================

1. Setup Virtual Environment:
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux

2. Install Dependencies:
   pip install -r requirements.txt

3. Configure Environment:
   cp .env.example .env
   # Edit .env with your Supabase credentials

4. Create Supabase Table:
   In Supabase SQL Editor, paste from QUICKSTART.md

5. Create Admin User:
   python manage.py create_superuser --username admin --password admin123

6. Run Server:
   python manage.py runserver

7. Access:
   Form: http://localhost:8000/reports/submit/
   Admin: http://localhost:8000/admin/login/

# ============================================================================
# FEATURES
# ============================================================================

USER FEATURES:
  ✅ Anonymous report submission
  ✅ No authentication required
  ✅ Optional image upload (JPEG, PNG, GIF, WEBP)
  ✅ Report categorization
  ✅ Location tagging
  ✅ Success confirmation
  ✅ Mobile responsive design

ADMIN FEATURES:
  ✅ Secure login with Django sessions
  ✅ Reports dashboard with table view
  ✅ Real-time status updates (new, reviewed, archived)
  ✅ View full report details with images
  ✅ CSV export functionality
  ✅ User-friendly interface (no Django Admin)
  ✅ Mobile responsive

TECHNICAL FEATURES:
  ✅ Supabase database integration
  ✅ Supabase file storage
  ✅ CSRF protection
  ✅ Session security
  ✅ Form validation
  ✅ Error handling
  ✅ Clean code architecture

# ============================================================================
# DEPENDENCIES
# ============================================================================

Core:
  - Django 4.2.7          (Web framework)
  - python-supabase 0.3.0 (Supabase client)
  - Pillow 10.1.0         (Image handling)
  - python-dotenv 1.0.0   (Environment variables)

Frontend:
  - Bootstrap 5.3.0       (CSS framework, via CDN)

Development:
  - gunicorn              (Production server)
  - docker                (Containerization)

Optional:
  - pytest                (Testing)
  - black                 (Code formatting)
  - flake8                (Linting)

# ============================================================================
# DJANGO APPS
# ============================================================================

REPORTS APP (reports/)
Purpose: Handle anonymous report submissions
Key Files:
  - views.py: submit_report(), report_submitted()
  - forms.py: ReportForm validation
  - supabase_client.py: Supabase integration
  - urls.py: Route /reports/submit/ and /reports/submitted/

ADMINPANEL APP (adminpanel/)
Purpose: Admin dashboard and authentication
Key Files:
  - views.py: Login, dashboard, report detail, CSV export
  - urls.py: Routes for /admin/* endpoints
  - decorators.py: Authentication helpers

# ============================================================================
# VIEWS & URLS
# ============================================================================

USER VIEWS:
  GET  /reports/submit/     -> Show form
  POST /reports/submit/     -> Process submission
  GET  /reports/submitted/  -> Success page

ADMIN VIEWS:
  GET  /admin/login/        -> Login form
  POST /admin/login/        -> Process login
  GET  /admin/logout/       -> Logout
  GET  /admin/dashboard/    -> Reports table
  GET  /admin/report/<id>/  -> Report details
  POST /admin/report/<id>/status/ -> Update status
  GET  /admin/export/csv/   -> Export reports

# ============================================================================
# DATABASE SCHEMA (SUPABASE)
# ============================================================================

TABLE: reports

Columns:
  id          UUID (Primary Key, auto-generated)
  description TEXT (Required, max 5000 chars)
  image_url   TEXT (Optional, public URL to Supabase Storage)
  category    TEXT (Optional, choice field)
  location    TEXT (Optional, max 255 chars)
  status      TEXT (Default: 'new', values: 'new', 'reviewed', 'archived')
  created_at  TIMESTAMP (Default: now())

Indexes:
  - PRIMARY KEY on id
  - Optional: Index on created_at for better query performance

# ============================================================================
# SUPABASE STORAGE
# ============================================================================

Bucket Name: report_uploads
Access: Public
File Format: /{uuid}.{extension}

Files are stored as:
  /report_uploads/f47ac10b-58cc-4372-a567-0e02b2c3d479.jpg

Public URLs are stored in the database:
  https://{project}.supabase.co/storage/v1/object/public/report_uploads/{filename}

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

Required (.env file):
  SECRET_KEY              Django secret key
  DEBUG                   Debug mode (True/False)
  ALLOWED_HOSTS           Comma-separated allowed hosts
  SUPABASE_URL            Supabase project URL
  SUPABASE_KEY            Supabase anonymous key
  SUPABASE_BUCKET         Storage bucket name (default: report_uploads)

Example:
  SECRET_KEY=django-insecure-your-secret-key-here
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1
  SUPABASE_URL=https://your-project.supabase.co
  SUPABASE_KEY=eyJhbGc...
  SUPABASE_BUCKET=report_uploads

# ============================================================================
# AUTHENTICATION & AUTHORIZATION
# ============================================================================

User Submission (Anonymous):
  - No authentication required
  - Anyone can submit reports
  - Optional CSRF protection (enabled by default)

Admin Dashboard:
  - Django session-based authentication
  - Username + password login
  - User must be a Django superuser (is_staff=True)
  - Session cookie expires after 7 days
  - Cookies: Secure, HttpOnly (in production)

# ============================================================================
# SECURITY FEATURES
# ============================================================================

Built-in:
  ✅ CSRF protection
  ✅ Session security
  ✅ Password validation
  ✅ File upload validation
  ✅ SQL injection protection (via ORM)
  ✅ XSS prevention (template escaping)

Recommended for Production:
  ⚠️  HTTPS/SSL certificate
  ⚠️  Supabase Row Level Security (RLS)
  ⚠️  Rate limiting on submission endpoint
  ⚠️  Rate limiting on login endpoint
  ⚠️  Strong Django SECRET_KEY
  ⚠️  DEBUG=False
  ⚠️  Secure superuser password
  ⚠️  Regular database backups

# ============================================================================
# FORM VALIDATION
# ============================================================================

ReportForm Fields:
  description (Required):
    - Type: Textarea
    - Max length: 5000 characters
    - Validation: Non-empty after stripping whitespace

  category (Optional):
    - Type: Select dropdown
    - Choices: safety, infrastructure, environmental, other
    - Default: Empty/None

  location (Optional):
    - Type: Text input
    - Max length: 255 characters
    - Validation: None

  image (Optional):
    - Type: File input
    - Accepted: image/* (JPEG, PNG, GIF, WEBP)
    - Max size: 5MB
    - Validation: Via Pillow library

# ============================================================================
# ADMIN FEATURES
# ============================================================================

Dashboard:
  - Table view of all reports
  - Sort by: Created date (newest first)
  - Columns: Category, Location, Status, Date, Action
  - Statistics: Total report count
  - Actions: View detail, Export CSV

Report Detail:
  - Full description
  - Image preview (if uploaded)
  - Metadata (ID, category, location, date)
  - Status update buttons (live update with AJAX)
  - Back button to dashboard

Status Management:
  - new:      Initial status (yellow badge)
  - reviewed: Reviewed status (green badge)
  - archived: Archived status (gray badge)

CSV Export:
  - All reports
  - Columns: ID, Category, Location, Status, Created, Description, Image URL
  - Filename: reports.csv
  - Format: Standard RFC 4180

# ============================================================================
# DEPLOYMENT GUIDES
# ============================================================================

LOCAL DEVELOPMENT:
  python manage.py runserver

HEROKU:
  1. heroku create your-app-name
  2. heroku buildpacks:add heroku/python
  3. heroku config:set SECRET_KEY=your-key
  4. heroku config:set SUPABASE_URL=your-url
  5. git push heroku main

DOCKER:
  docker build -t anon-reporting .
  docker run -p 8000:8000 --env-file .env anon-reporting

GUNICORN (Production):
  gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4

NGINX (Reverse Proxy):
  See documentation for nginx configuration with Gunicorn

# ============================================================================
# TESTING
# ============================================================================

Not included by default, but easy to add:

Create tests/test_reports.py:
  - Test form validation
  - Test report submission
  - Test file upload
  - Test admin views

Create tests/test_admin.py:
  - Test login
  - Test dashboard
  - Test status update
  - Test CSV export

Run tests:
  python manage.py test

# ============================================================================
# COMMON CUSTOMIZATIONS
# ============================================================================

Add More Status Options:
  1. Update report_detail.html buttons
  2. Update adminpanel/views.py validation
  3. Update database if needed

Add Custom Fields:
  1. Update Supabase table schema
  2. Add to ReportForm in reports/forms.py
  3. Update templates

Change Styling:
  1. Modify <style> sections in templates
  2. Create static/style.css and link it
  3. Use custom Bootstrap theme

Add 2FA:
  1. Install django-otp
  2. Add OTP verification to login
  3. Update admin_login.html

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"ModuleNotFoundError: No module named 'django'"
  → Activate virtual environment
  → pip install -r requirements.txt

"Supabase connection error"
  → Check SUPABASE_URL and SUPABASE_KEY in .env
  → Ensure project is active
  → Test connection in Supabase dashboard

"File upload fails"
  → Check bucket name is 'report_uploads'
  → Ensure bucket is public
  → Check file size (max 5MB)
  → Check file format (JPEG, PNG, GIF, WEBP)

"Admin login fails"
  → Check user is_staff=True
  → Use correct username/password
  → Clear browser cookies
  → python manage.py changepassword username

"404 on report detail"
  → Ensure report ID exists
  → Check Supabase table has data
  → Check database connection

# ============================================================================
# PRODUCTION CHECKLIST
# ============================================================================

Before deploying to production:

[ ] Set DEBUG=False
[ ] Generate random SECRET_KEY
[ ] Configure ALLOWED_HOSTS
[ ] Set up HTTPS/SSL
[ ] Configure database backups
[ ] Set up monitoring/logging
[ ] Run security checks: python manage.py check --deploy
[ ] Set up email notifications (optional)
[ ] Configure rate limiting
[ ] Set up Supabase RLS policies
[ ] Test all admin functions
[ ] Test all user functions
[ ] Test file upload
[ ] Test email notifications
[ ] Create backup strategy
[ ] Document deployment process
[ ] Set up error tracking (Sentry, etc.)

# ============================================================================
# FILE SIZE SPECIFICATIONS
# ============================================================================

Image Upload Limits:
  - Max file size: 5 MB (5,242,880 bytes)
  - Configurable in: core/settings.py
  - Settings: FILE_UPLOAD_MAX_MEMORY_SIZE, DATA_UPLOAD_MAX_MEMORY_SIZE

Text Field Limits:
  - Description: 5,000 characters
  - Location: 255 characters

Database:
  - No explicit size limits, depends on Supabase plan

# ============================================================================
# SUPPORT & DOCUMENTATION
# ============================================================================

Documentation Files:
  - README.md        Full documentation
  - QUICKSTART.md    5-minute setup guide
  - API.md           API endpoint documentation
  - This file        Complete project overview

External Documentation:
  - Django Docs:     https://docs.djangoproject.com/
  - Supabase Docs:   https://supabase.com/docs
  - Bootstrap Docs:  https://getbootstrap.com/docs/

# ============================================================================
# VERSION HISTORY
# ============================================================================

Version 1.0.0 (Initial Release)
  - Anonymous report submission
  - Admin dashboard
  - Image upload
  - Status management
  - CSV export
  - Bootstrap UI
  - Supabase integration

# ============================================================================
