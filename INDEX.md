"""
ANONYMOUS REPORTING SYSTEM
Quick Navigation & File Index

================================================================================
START HERE 👇
================================================================================

1️⃣  READ FIRST:
    → START_HERE.md        (Quick orientation - 2 min read)
    → QUICKSTART.md        (5-minute setup guide)
    
2️⃣  FOR COMPLETE DETAILS:
    → README.md            (Full documentation)
    
3️⃣  FOR DEVELOPERS:
    → API.md               (Endpoint reference)
    → PROJECT_SUMMARY.md   (Complete overview)
    → MANIFEST.md          (Project structure details)

4️⃣  FOR DEPLOYMENT:
    → README.md            (Deployment section)
    → Dockerfile           (Docker setup)

================================================================================
PROJECT LAYOUT
================================================================================

📁 PROJECT FILES:
  ├─ START_HERE.md              ← Start with this!
  ├─ QUICKSTART.md              ← 5-minute setup
  ├─ README.md                  ← Full guide
  ├─ API.md                     ← Endpoint docs
  ├─ PROJECT_SUMMARY.md         ← Complete summary
  ├─ MANIFEST.md                ← Project details
  │
  ├─ manage.py                  ← Django CLI
  ├─ requirements.txt            ← Python packages
  ├─ .env.example               ← Configuration template
  ├─ .gitignore                 ← Git rules
  │
  ├─ Dockerfile                 ← Docker image
  └─ docker-compose.yml         ← Docker compose

📁 DJANGO APPS:
  ├─ core/                       ← Project settings
  │   ├─ settings.py            ← Django configuration
  │   ├─ urls.py                ← Root URLs
  │   ├─ wsgi.py                ← WSGI app
  │   ├─ asgi.py                ← ASGI app
  │   └─ utils.py               ← Utilities
  │
  ├─ reports/                    ← Report submissions
  │   ├─ views.py               ← Form submission logic
  │   ├─ forms.py               ← Form validation
  │   ├─ urls.py                ← Report URLs
  │   ├─ supabase_client.py      ← Supabase integration
  │   └─ templates/
  │       ├─ report_form.html    ← Submission form
  │       └─ report_submitted.html ← Success page
  │
  └─ adminpanel/                 ← Admin dashboard
      ├─ views.py               ← Admin logic
      ├─ urls.py                ← Admin URLs
      ├─ decorators.py          ← Auth helpers
      └─ templates/
          ├─ admin_login.html   ← Login form
          ├─ admin_dashboard.html ← Reports table
          ├─ report_detail.html  ← Report viewer
          └─ 404.html            ← Error page

📁 STATIC FILES:
  └─ static/                     ← CSS, JS, images (add here)

================================================================================
QUICK COMMANDS
================================================================================

# Setup Virtual Environment:
python -m venv venv
venv\Scripts\activate

# Install Dependencies:
pip install -r requirements.txt

# Configure Environment:
copy .env.example .env
# Then edit .env with your Supabase credentials

# Create Admin User:
python manage.py create_superuser --username admin --password admin123

# Run Development Server:
python manage.py runserver

# Run Docker:
docker-compose up

================================================================================
ACCESS POINTS
================================================================================

After running: python manage.py runserver

📝 USER FORM:
   http://localhost:8000/reports/submit/

🔐 ADMIN LOGIN:
   http://localhost:8000/admin/login/

Default Credentials (after creating superuser):
   Username: admin
   Password: admin123 (change this!)

================================================================================
FEATURES AT A GLANCE
================================================================================

✅ Anonymous Report Submission
   • No login required
   • Optional image upload
   • Categorization
   • Location tagging

✅ Admin Dashboard
   • Secure login
   • Reports table
   • Real-time status updates
   • Full report details
   • CSV export

✅ Built with Best Practices
   • Django 4.2.7
   • Supabase (PostgreSQL + Storage)
   • Bootstrap 5 UI
   • CSRF protection
   • Session security
   • Form validation
   • File validation

================================================================================
DOCUMENTATION FILES GUIDE
================================================================================

FILE                    BEST FOR                    READ TIME
─────────────────────────────────────────────────────────────────────
START_HERE.md          Quick orientation            2 min
QUICKSTART.md          5-minute setup               5 min
README.md              Complete guide               15 min
API.md                 Endpoint reference           10 min
PROJECT_SUMMARY.md     Complete overview            10 min
MANIFEST.md            Project details              10 min
.env.example           Configuration template       1 min

================================================================================
SUPPORT
================================================================================

Having issues? Follow this order:

1. Check START_HERE.md "Troubleshooting" section
2. Check QUICKSTART.md setup steps
3. Check README.md "Troubleshooting" section
4. Check .env configuration
5. Verify Supabase connection
6. Check Django console output

Common Issues:
  • "ModuleNotFoundError: django"
    → pip install -r requirements.txt
    
  • "Supabase connection error"
    → Check SUPABASE_URL and SUPABASE_KEY in .env
    
  • "File upload fails"
    → Ensure bucket is named "report_uploads" and is public
    
  • "Admin login fails"
    → Check credentials, ensure user has is_staff=True

================================================================================
NEXT STEPS
================================================================================

1. Read START_HERE.md (2 minutes)
2. Follow QUICKSTART.md (5 minutes)
3. Run the server
4. Test the system
5. Customize as needed
6. Deploy when ready

That's it! You're ready to go. 🚀

================================================================================
VERSION INFO
================================================================================

Project:    Anonymous Reporting System
Version:    1.0.0
Created:    November 20, 2025
Status:     Complete & Ready to Use
Python:     3.8+
Django:     4.2.7
Database:   Supabase (PostgreSQL)
Storage:    Supabase Storage
UI:         Bootstrap 5

================================================================================
"""
