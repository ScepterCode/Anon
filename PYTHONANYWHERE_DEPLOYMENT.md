# PythonAnywhere Deployment Guide

Complete step-by-step instructions for deploying your Django anonymous reporting system to PythonAnywhere.

---

## **STEP 1: Prepare Your Project**

### 1.1 Create a `.gitignore` file (if not already present)

Your project should ignore sensitive files:

```
# Virtual environment
venv/
env/

# Django
*.pyc
__pycache__/
db.sqlite3
*.db
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### 1.2 Update `requirements.txt`

Make sure all dependencies are listed:

```bash
# In your project directory, run:
pip freeze > requirements.txt
```

Your `requirements.txt` should contain:
```
Django==4.2.7
supabase==2.24.0
python-dotenv==1.0.0
Pillow==10.1.0
```

### 1.3 Create GitHub Repository (Recommended)

1. Go to https://github.com/new
2. Create a new repository (e.g., `anonymous-reporting-system`)
3. Push your code:

```powershell
cd c:\Users\DELL\Desktop\Anon\project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/anonymous-reporting-system.git
git push -u origin main
```

**Without GitHub?** You can upload files directly to PythonAnywhere (Step 3.3).

---

## **STEP 2: Create PythonAnywhere Account**

1. Go to https://www.pythonanywhere.com/
2. Click "Sign up for free"
3. Create account with email/username
4. Verify email
5. Log in to your dashboard

---

## **STEP 3: Clone/Upload Your Project**

### **Option A: Clone from GitHub (Easiest)**

1. Log in to PythonAnywhere dashboard
2. Open **Bash console** (bottom of page)
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/anonymous-reporting-system.git

# Navigate to project
cd anonymous-reporting-system

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 mysite

# Install dependencies
pip install -r requirements.txt
```

### **Option B: Upload Files Directly**

1. Log in to PythonAnywhere
2. Go to **Files** tab (left sidebar)
3. Create new folder: `anonymous-reporting-system`
4. Upload your project files via web interface
5. Open Bash console and:

```bash
cd ~/anonymous-reporting-system
mkvirtualenv --python=/usr/bin/python3.10 mysite
pip install -r requirements.txt
```

---

## **STEP 4: Configure Django Settings**

### 4.1 Update `core/settings.py`

Edit the file to allow PythonAnywhere domain:

Find this line:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

Replace with:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'YOUR_USERNAME.pythonanywhere.com']
```

### 4.2 Set `DEBUG = False` for Production

Find:
```python
DEBUG = True
```

Replace with:
```python
DEBUG = False
```

### 4.3 Generate a Secret Key

In PythonAnywhere Bash console:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and update `settings.py`:

```python
SECRET_KEY = 'paste_the_generated_key_here'
```

---

## **STEP 5: Run Django Migrations**

In PythonAnywhere Bash console:

```bash
# Activate virtual environment
workon mysite

# Navigate to project
cd ~/anonymous-reporting-system

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

---

## **STEP 6: Create Superuser (Admin Account)**

```bash
# Still in bash console with virtual environment active
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: your@email.com
# Password: (enter secure password)
```

---

## **STEP 7: Configure Web App on PythonAnywhere**

### 7.1 Create Web App

1. Go to **Web** tab (left sidebar)
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click **Next**

### 7.2 Configure WSGI File

1. You'll see a WSGI file path: `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`
2. Click on this file to edit
3. Replace entire content with:

```python
import os
import sys

# Add project to path
project_home = '/home/YOUR_USERNAME/anonymous-reporting-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `YOUR_USERNAME` with your actual PythonAnywhere username!**

### 7.3 Configure Virtual Environment

Back in the **Web** tab:

1. Find **"Virtualenv"** section
2. Enter path: `/home/YOUR_USERNAME/.virtualenvs/mysite`
3. Click tick icon to confirm

### 7.4 Configure Static Files

In the **Web** tab, find **"Static files"** section:

Click **Add a new static files mapping**:
- **URL:** `/static/`
- **Directory:** `/home/YOUR_USERNAME/anonymous-reporting-system/static`

Click **Add**:
- **URL:** `/media/`
- **Directory:** `/home/YOUR_USERNAME/anonymous-reporting-system/media`

---

## **STEP 8: Set Environment Variables**

### 8.1 Create `.env` File

In PythonAnywhere Bash console:

```bash
cd ~/anonymous-reporting-system
nano .env
```

Add these lines (replace with YOUR actual Supabase credentials):

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_BUCKET=report_uploads
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your_username.pythonanywhere.com
```

Save: `Ctrl + X`, then `Y`, then `Enter`

### 8.2 Set Environment Variables in PythonAnywhere

1. Go to **Web** tab
2. Scroll to **"Environment variables"**
3. Click to add:
   - `SUPABASE_URL` = `https://your-project.supabase.co`
   - `SUPABASE_KEY` = `your-anon-key`
   - `SUPABASE_BUCKET` = `report_uploads`

---

## **STEP 9: Reload Web App**

1. In **Web** tab, click **Reload** button (green button at top)
2. Wait 10-20 seconds for app to restart

---

## **STEP 10: Test Your Deployment**

1. Go to: `https://YOUR_USERNAME.pythonanywhere.com/reports/submit/`
   - You should see the report form
   
2. Go to: `https://YOUR_USERNAME.pythonanywhere.com/admin/login/`
   - You should see the login page
   - Login with your superuser credentials

3. If you see errors:
   - Check **Web** tab → **Error log** for details
   - Check **Web** tab → **Server log** for details

---

## **STEP 11: Create Supabase Project (If Not Done)**

### 11.1 Create Supabase Account

1. Go to https://supabase.com
2. Sign up with GitHub/Google
3. Create new project
4. Wait for project to initialize (5-10 minutes)

### 11.2 Create "reports" Table

1. Go to **SQL Editor**
2. Create new query, paste:

```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  description TEXT NOT NULL,
  category TEXT,
  location TEXT,
  image_url TEXT,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- Create policy to allow anonymous inserts
CREATE POLICY "Allow anonymous insert" ON reports
  FOR INSERT
  WITH CHECK (true);

-- Create policy to allow authenticated select
CREATE POLICY "Allow authenticated select" ON reports
  FOR SELECT
  USING (true);

-- Create policy to allow authenticated update
CREATE POLICY "Allow authenticated update" ON reports
  FOR UPDATE
  USING (true);

-- Create policy to allow authenticated delete
CREATE POLICY "Allow authenticated delete" ON reports
  FOR DELETE
  USING (true);
```

3. Run query

### 11.3 Create Storage Bucket

1. Go to **Storage** (left sidebar)
2. Create new bucket: `report_uploads`
3. Make it **Public**
4. Click bucket, go to **Policies**
5. Enable public read/write

### 11.4 Get API Keys

1. Go to **Settings** → **API**
2. Copy:
   - `Project URL` (SUPABASE_URL)
   - `anon public` key (SUPABASE_KEY)
3. Add these to your `.env` file and PythonAnywhere environment variables

---

## **STEP 12: Final Testing**

1. Visit: `https://YOUR_USERNAME.pythonanywhere.com/reports/submit/`
2. Submit a test report
3. Log in at: `https://YOUR_USERNAME.pythonanywhere.com/admin/login/`
4. View reports in dashboard

---

## **TROUBLESHOOTING**

### **500 Error - Check Logs**

In **Web** tab:
- Click **Error log** (red icon)
- Click **Server log** (blue icon)
- Look for error messages

### **Module not found**

In Bash console:
```bash
workon mysite
cd ~/anonymous-reporting-system
pip install -r requirements.txt
```

Then reload web app.

### **Static files not loading**

In **Web** tab:
- Click **Reload static files** button
- Wait 30 seconds
- Refresh browser

### **Database connection fails**

Check:
1. `SUPABASE_URL` is correct (https://...)
2. `SUPABASE_KEY` is correct
3. Supabase project is running
4. Table `reports` exists in Supabase

### **Admin login not working**

In Bash console:
```bash
workon mysite
cd ~/anonymous-reporting-system
python manage.py createsuperuser
```

Re-create superuser with new password.

---

## **IMPORTANT NOTES**

- **Free tier:** Limited to 100MB disk, 512MB RAM
- **Always-on:** Your app runs 24/7 (unlike Render)
- **Custom domain:** Available on paid plans
- **Backups:** Manual export reports to CSV regularly

---

## **USEFUL COMMANDS** (Bash Console)

```bash
# Activate virtual environment
workon mysite

# Navigate to project
cd ~/anonymous-reporting-system

# Run migrations after code changes
python manage.py migrate

# Restart web app
python manage.py runserver

# View error logs
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log

# Check Django status
python manage.py check
```

---

## **NEXT STEPS**

1. ✅ Deploy to PythonAnywhere (this guide)
2. ✅ Configure Supabase database
3. Test all features
4. Set up custom domain (paid)
5. Enable HTTPS (automatic on PythonAnywhere)
6. Regular backups of reports (via CSV export)

**Your site will be live at:** `https://YOUR_USERNAME.pythonanywhere.com/`

