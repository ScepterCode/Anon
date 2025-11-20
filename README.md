# Anonymous Reporting System

A simple, privacy-focused anonymous reporting system built with Django and Supabase.

## Features

✅ Anonymous report submission (no login required)
✅ Optional image uploads to Supabase Storage
✅ Custom admin dashboard (no Django Admin)
✅ Admin authentication via Django sessions
✅ Report status management (new, reviewed, archived)
✅ CSV export functionality
✅ Mobile-responsive design with Bootstrap

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- A Supabase account with:
  - Database table named `reports`
  - Storage bucket named `report_uploads`

## Installation

### 1. Clone the repository

```bash
cd project
```

### 2. Create a virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `SECRET_KEY`: Generate a random Django secret key

### 5. Create Supabase table

In your Supabase dashboard, run this SQL:

```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  description TEXT NOT NULL,
  image_url TEXT,
  category TEXT,
  location TEXT,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT now()
);
```

### 6. Create Supabase storage bucket

1. Go to Storage in your Supabase dashboard
2. Create a new bucket named `report_uploads`
3. Set it as public (enable public access)

### 7. Create Django superuser

```bash
python manage.py createsuperuser
```

This user will be used for admin login (must have `is_staff=True`).

### 8. Run the development server

```bash
python manage.py runserver
```

Visit:
- **User form**: http://localhost:8000/reports/submit/
- **Admin panel**: http://localhost:8000/admin/login/

## Project Structure

```
project/
├── core/                          # Django project settings
│   ├── settings.py               # Main configuration
│   ├── urls.py                   # Root URL router
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py                   # ASGI application
│
├── reports/                       # Anonymous report submission app
│   ├── views.py                  # Report submission views
│   ├── forms.py                  # Django form for reports
│   ├── urls.py                   # App URL patterns
│   ├── supabase_client.py        # Supabase integration
│   └── templates/
│       ├── report_form.html      # Submission form
│       └── report_submitted.html # Success page
│
├── adminpanel/                    # Admin dashboard app
│   ├── views.py                  # Admin views & authentication
│   ├── urls.py                   # Admin URL patterns
│   └── templates/
│       ├── admin_login.html      # Login page
│       ├── admin_dashboard.html  # Reports table
│       └── report_detail.html    # Single report detail
│
├── static/                        # Static files (CSS, JS, images)
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## API Endpoints

### User-facing URLs
- `GET /reports/submit/` - Display report submission form
- `POST /reports/submit/` - Submit a new report
- `GET /reports/submitted/` - Confirmation page

### Admin URLs
- `GET /admin/login/` - Admin login page
- `POST /admin/login/` - Process admin login
- `GET /admin/logout/` - Logout user
- `GET /admin/dashboard/` - View all reports (requires authentication)
- `GET /admin/report/<id>/` - View single report details
- `POST /admin/report/<id>/status/` - Update report status
- `GET /admin/export/csv/` - Export reports as CSV

## Admin Dashboard Features

1. **Dashboard View**
   - Table of all reports
   - Filter by status (new, reviewed, archived)
   - Shows: category, location, status, submission date
   - CSV export button

2. **Report Detail View**
   - Full report description
   - Image preview (if uploaded)
   - Category and location metadata
   - Status update buttons
   - Real-time status changes

3. **Status Management**
   - **New**: Initial status for all submissions
   - **Reviewed**: Admin has examined the report
   - **Archived**: Report is closed/resolved

## Security Considerations

### For Production

1. **Update Django SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set DEBUG=False**
   - Update `.env` with `DEBUG=False`

3. **Use HTTPS**
   - Set `SESSION_COOKIE_SECURE=True` (automatically set when DEBUG=False)
   - Deploy with SSL certificate

4. **Configure ALLOWED_HOSTS**
   - Update `ALLOWED_HOSTS` in `.env` with your domain

5. **Supabase Security**
   - Use Row Level Security (RLS) policies
   - Restrict storage bucket access if needed
   - Keep your keys private (use environment variables)

6. **Admin Authentication**
   - Create strong password for superuser
   - Disable superuser when not needed
   - Consider adding IP whitelisting

## Deployment

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:

```bash
docker build -t anon-reporting .
docker run -p 8000:8000 --env-file .env anon-reporting
```

## Customization

### Change Status Options

Edit `report_detail.html` buttons and update `adminpanel/views.py` status validation.

### Add More Fields

1. Update Supabase table schema
2. Add field to `ReportForm` in `reports/forms.py`
3. Update template files to display new field

### Customize Styling

Modify the `<style>` sections in template files or add a static CSS file.

## Troubleshooting

### Supabase Connection Error
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check internet connectivity
- Ensure Supabase project is active

### File Upload Not Working
- Check bucket name is `report_uploads`
- Verify bucket is public
- Ensure file size is under 5MB

### Admin Login Fails
- Confirm user is a Django superuser (`is_staff=True`)
- Use correct username and password
- Clear browser cookies and try again

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, refer to the documentation or create an issue in the repository.
