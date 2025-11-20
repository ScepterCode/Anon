"""
API Documentation for Anonymous Reporting System
"""

# ============================================================================
# USER-FACING ENDPOINTS
# ============================================================================

"""
### 1. GET /reports/submit/
Display anonymous report submission form

Response: HTML form page
Status: 200 OK

No authentication required.
"""

"""
### 2. POST /reports/submit/
Submit a new anonymous report

Request Body (form-data):
  - description (required): Text description (max 5000 chars)
  - category (optional): 'safety', 'infrastructure', 'environmental', 'other'
  - location (optional): Location text (max 255 chars)
  - image (optional): Image file (JPEG, PNG, max 5MB)

Response: Redirect to /reports/submitted/
Status: 302 Found or 200 OK with form errors

No authentication required.

Process:
  1. Validate form data
  2. Upload image to Supabase Storage (if provided)
  3. Get public URL from Supabase
  4. Insert report metadata into Supabase database
  5. Redirect to success page
"""

"""
### 3. GET /reports/submitted/
Show confirmation page after successful submission

Response: HTML confirmation page
Status: 200 OK

No authentication required.
"""

# ============================================================================
# ADMIN ENDPOINTS (REQUIRE AUTHENTICATION)
# ============================================================================

"""
### 4. GET /admin/login/
Display admin login form

Response: HTML login form
Status: 200 OK

No authentication required. Redirects to dashboard if already logged in.
"""

"""
### 5. POST /admin/login/
Process admin login

Request Body (form-data):
  - username (required): Admin username
  - password (required): Admin password

Response: Redirect to /admin/dashboard/ on success, or back to login with error
Status: 302 Found or 200 OK

Authentication: None required for login attempt
Authorization: User must have is_staff=True to succeed
"""

"""
### 6. GET /admin/logout/
Log out the current admin user

Response: Redirect to /admin/login/
Status: 302 Found

Authentication: Django session (required)
Authorization: is_staff=True (required)
"""

"""
### 7. GET /admin/dashboard/
Display all reports in a table view

Query Parameters:
  - None

Response: HTML dashboard page with reports table
Status: 200 OK

Authentication: Django session (required)
Authorization: is_staff=True (required)

Returns:
  - List of all reports with: id, category, location, status, created_at
  - CSV export button
  - Link to view report details
"""

"""
### 8. GET /admin/report/<id>/
Display detailed view of a single report

URL Parameters:
  - id: Report UUID

Response: HTML detail page
Status: 200 OK or 404 Not Found

Authentication: Django session (required)
Authorization: is_staff=True (required)

Returns:
  - Full report data: id, description, image, category, location, status, created_at
  - Image preview (if uploaded)
  - Status update buttons
"""

"""
### 9. POST /admin/report/<id>/status/
Update the status of a report (AJAX endpoint)

URL Parameters:
  - id: Report UUID

Request Body (form-data):
  - status (required): 'new', 'reviewed', or 'archived'

Response: "OK" or error message
Status: 200 OK, 400 Bad Request, 500 Internal Server Error

Authentication: Django session (required)
Authorization: is_staff=True (required)

Valid statuses:
  - 'new': Initial status for new submissions
  - 'reviewed': Report has been examined
  - 'archived': Report is closed/resolved
"""

"""
### 10. GET /admin/export/csv/
Export all reports as CSV file

Query Parameters:
  - None

Response: CSV file (application/csv)
Status: 200 OK

Authentication: Django session (required)
Authorization: is_staff=True (required)

CSV Columns:
  - ID
  - Category
  - Location
  - Status
  - Created At
  - Description
  - Image URL

Filename: reports.csv
"""

# ============================================================================
# ERROR RESPONSES
# ============================================================================

"""
### 400 Bad Request
Invalid form data or invalid status value
Returns: Error message in form context or as text

Examples:
  - Missing required field
  - Invalid status value (not in ['new', 'reviewed', 'archived'])
  - File too large (>5MB)
  - Invalid image format
"""

"""
### 403 Forbidden
User is not authenticated or lacks required permissions
Returns: 403 status with "Unauthorized" message

Examples:
  - Not logged in when accessing admin endpoints
  - User is not staff when accessing admin endpoints
"""

"""
### 404 Not Found
Report ID does not exist
Returns: HTML 404 page with message

Examples:
  - Report ID not found in database
"""

"""
### 500 Internal Server Error
Server error (database error, file upload error, etc.)
Returns: Error message

Examples:
  - Supabase connection error
  - File upload to storage failed
  - Database query error
"""

# ============================================================================
# AUTHENTICATION & AUTHORIZATION
# ============================================================================

"""
Authentication Method: Django Sessions (Cookies)

Login Process:
  1. User POSTs username and password to /admin/login/
  2. Django authenticates against local database
  3. If successful, session cookie is created
  4. User is redirected to /admin/dashboard/

Session Details:
  - Cookie Name: sessionid
  - Expires: 7 days (configurable)
  - Secure: Yes (in production)
  - HttpOnly: Yes
  
Authorization:
  - Admin endpoints require: login_required
  - Additional check: user.is_staff == True
  
Logout:
  - User clicks logout link
  - Session is destroyed
  - Redirect to login page
"""

# ============================================================================
# RATE LIMITING (RECOMMENDED FOR PRODUCTION)
# ============================================================================

"""
Not implemented by default, but recommended:

For submission endpoint (/reports/submit/):
  - Rate limit to prevent spam
  - Suggestion: 10 reports per IP per hour
  
For login endpoint (/admin/login/):
  - Rate limit to prevent brute force
  - Suggestion: 5 attempts per IP per 15 minutes
  
Implementation: Use django-ratelimit or similar package
"""

# ============================================================================
# DATA VALIDATION
# ============================================================================

"""
Report Description:
  - Required: Yes
  - Type: String (max 5000 characters)
  - Validation: Must not be empty after stripping whitespace

Category:
  - Required: No
  - Type: String (choice field)
  - Valid values: 'safety', 'infrastructure', 'environmental', 'other'
  - Default: None (can be null in database)

Location:
  - Required: No
  - Type: String (max 255 characters)
  - Validation: No special validation
  - Default: None (can be null in database)

Image:
  - Required: No
  - Type: File
  - Valid formats: JPG, JPEG, PNG, GIF, WEBP
  - Max size: 5 MB (5242880 bytes)
  - MIME types: image/jpeg, image/png, image/gif, image/webp
"""

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

"""
Table: reports

Columns:
  - id (UUID, Primary Key, Auto-generated)
    Type: UUID
    Default: gen_random_uuid()
    Description: Unique identifier for report
  
  - description (TEXT, Not Null)
    Type: Text
    Description: Full report description
  
  - image_url (TEXT, Nullable)
    Type: Text (URL)
    Description: Public URL to image in Supabase Storage
    Default: NULL
  
  - category (TEXT, Nullable)
    Type: Text
    Valid values: 'safety', 'infrastructure', 'environmental', 'other'
    Default: NULL
  
  - location (TEXT, Nullable)
    Type: Text
    Default: NULL
  
  - status (TEXT, Not Null)
    Type: Text
    Valid values: 'new', 'reviewed', 'archived'
    Default: 'new'
  
  - created_at (TIMESTAMP, Not Null)
    Type: Timestamp
    Default: now()
    Description: When the report was submitted
"""

# ============================================================================
# SUPABASE STORAGE
# ============================================================================

"""
Bucket: report_uploads
Access: Public

File Organization:
  - Files: /report_uploads/{uuid}.{extension}
  - Example: /report_uploads/f47ac10b-58cc-4372-a567-0e02b2c3d479.jpg

Public URL Format:
  https://{project-id}.supabase.co/storage/v1/object/public/report_uploads/{filename}

File Upload Process:
  1. Generate random UUID
  2. Determine file extension from original filename
  3. Create filename: {uuid}.{extension}
  4. Upload to Supabase Storage
  5. Retrieve and store public URL in database
"""

# ============================================================================
# EXAMPLE REQUESTS
# ============================================================================

"""
Example 1: Submit Report with Image (cURL)

curl -X POST http://localhost:8000/reports/submit/ \\
  -F "description=Pothole on Main Street needs repair" \\
  -F "category=infrastructure" \\
  -F "location=Main Street, Downtown" \\
  -F "image=@/path/to/image.jpg"
"""

"""
Example 2: Admin Login (cURL)

curl -X POST http://localhost:8000/admin/login/ \\
  -d "username=admin&password=mypassword" \\
  -c cookies.txt
"""

"""
Example 3: Get Dashboard (with session)

curl -X GET http://localhost:8000/admin/dashboard/ \\
  -b cookies.txt
"""

"""
Example 4: Update Report Status (JavaScript/Fetch)

fetch('/admin/report/f47ac10b-58cc-4372-a567-0e02b2c3d479/status/', {
  method: 'POST',
  body: new FormData(document.querySelector('form')),
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
  }
})
.then(response => response.ok ? location.reload() : alert('Error'))
.catch(error => console.error('Error:', error));
"""

"""
Example 5: Export Reports as CSV (cURL)

curl -X GET http://localhost:8000/admin/export/csv/ \\
  -b cookies.txt \\
  -o reports.csv
"""

# ============================================================================
