# Anonymous Reporting System

A privacy-focused anonymous reporting system built with Django and Supabase. Allows users to submit reports anonymously with optional image uploads, while providing administrators with a clean dashboard to manage and review submissions.

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Supabase](https://img.shields.io/badge/Supabase-Enabled-orange)

## ✨ Features

- 🔒 **Fully Anonymous Submissions** - No login or account required
- 📸 **Image Upload Support** - Optional image attachments via Supabase Storage
- 👤 **Optional Identity** - Users can choose to provide their name for follow-up
- 🎨 **Modern UI** - Clean, responsive design with Bootstrap
- 🔐 **Secure Admin Panel** - Django session-based authentication
- 📊 **Report Management** - View, update status, and delete reports
- 📥 **CSV Export** - Export all reports for analysis
- 🏷️ **Categorization** - Safety, Infrastructure, Environmental, Misconduct, and Other
- 📍 **Location Tracking** - Optional location field for reports
- 🔄 **Status Management** - New, Reviewed, and Archived states

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Supabase account ([Sign up free](https://supabase.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd project
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update with your values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_BUCKET=report_uploads
   ```

5. **Set up Supabase**

   Run this SQL in your Supabase SQL Editor:
   ```sql
   -- Create reports table
   CREATE TABLE IF NOT EXISTS public.reports (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     description TEXT NOT NULL,
     image_url TEXT,
     category TEXT,
     location TEXT,
     username TEXT,
     status TEXT DEFAULT 'new',
     created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
   );

   -- Disable RLS for simplicity (or configure proper policies)
   ALTER TABLE public.reports DISABLE ROW LEVEL SECURITY;
   ```

   Create a storage bucket:
   - Go to Storage → New bucket
   - Name: `report_uploads`
   - Make it **Public**

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Report submission: http://localhost:8000/reports/submit/
   - Admin panel: http://localhost:8000/admin/login/

## 📁 Project Structure

```
project/
├── core/                      # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # Root URL routing
│   └── wsgi.py               # WSGI application
├── reports/                   # Report submission app
│   ├── views.py              # Submission views
│   ├── forms.py              # Report form
│   ├── supabase_client.py    # Supabase integration
│   └── templates/            # Report templates
├── adminpanel/               # Admin dashboard app
│   ├── views.py              # Admin views
│   ├── decorators.py         # Auth decorators
│   └── templates/            # Admin templates
├── static/                    # Static files
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `ALLOWED_HOSTS` | Comma-separated hosts | Yes |
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anon key | Yes |
| `SUPABASE_BUCKET` | Storage bucket name | Yes |

### Report Categories

- Safety Concern
- Infrastructure Issue
- Environmental Issue
- Misconduct Report
- Other

### Report Statuses

- **New** - Initial status for all submissions
- **Reviewed** - Admin has examined the report
- **Archived** - Report is closed/resolved

## 🛡️ Security

### Production Deployment

1. **Generate a secure SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set DEBUG=False** in production

3. **Configure ALLOWED_HOSTS** with your domain

4. **Use HTTPS** (SSL certificate required)

5. **Set up Supabase RLS policies** for better security

6. **Use environment variables** for all sensitive data

## 📊 Admin Features

### Dashboard
- View all reports in a table
- Filter by status
- See submission dates and categories
- Export to CSV

### Report Detail
- View full report description
- See attached images
- Update report status
- Delete reports (with confirmation)
- Track submitter name (if provided)

## 🚢 Deployment

### Using Gunicorn

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Supabase Connection Error
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check internet connectivity
- Ensure Supabase project is active

### Image Upload Not Working
- Verify bucket name is `report_uploads`
- Ensure bucket is set to public
- Check file size is under 5MB

### Admin Login Fails
- Confirm user has `is_staff=True`
- Use correct username and password
- Clear browser cookies

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using Django and Supabase
