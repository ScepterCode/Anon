"""
Views for admin panel
"""

import csv
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from reports.supabase_client import get_supabase_client
from .decorators import admin_required

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def admin_login(request):
    """
    Admin login page using Django sessions
    """
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            logger.info(f"Admin user {username} logged in successfully")
            return redirect('admin_dashboard')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            error_message = 'Invalid credentials or insufficient permissions.'
    
    context = {
        'error_message': error_message,
    }
    return render(request, 'admin_login.html', context)

@require_http_methods(["GET"])
def admin_logout(request):
    """
    Log out admin user
    """
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} logged out")
        logout(request)
    return redirect('admin_login')

@admin_required
@require_http_methods(["GET"])
def admin_dashboard(request):
    """
    Display all reports in a table
    """
    try:
        supabase = get_supabase_client()
        reports = supabase.get_all_reports()
        
        # If reports is empty list, that's fine - just means no data yet
        # If reports is None or there's an error, it would have been caught
        
        context = {
            'reports': reports if reports else [],
            'total_count': len(reports) if reports else 0,
        }
        return render(request, 'admin_dashboard.html', context)
    except ValueError as e:
        # Configuration error (missing credentials)
        logger.error(f"Configuration error: {e}")
        return render(request, 'supabase_error.html')
    except Exception as e:
        # Connection or other errors
        logger.error(f"Dashboard error: {e}", exc_info=True)
        return render(request, 'supabase_error.html')

@admin_required
@require_http_methods(["GET"])
def report_detail(request, report_id):
    """
    Display details of a single report
    """
    supabase = get_supabase_client()
    report = supabase.get_report(report_id)
    
    if not report:
        return render(request, '404.html', {'message': 'Report not found'}, status=404)
    
    # Debug logging
    logger.info(f"Report {report_id} - image_url: {report.get('image_url')}")
    
    context = {
        'report': report,
    }
    return render(request, 'report_detail.html', context)

@admin_required
@require_http_methods(["POST"])
def update_report_status(request, report_id):
    """
    Update report status (AJAX endpoint)
    """
    status = request.POST.get('status', '').strip()
    
    if status not in ['new', 'reviewed', 'archived']:
        logger.warning(f"Invalid status update attempt: {status}")
        return HttpResponse('Invalid status', status=400)
    
    supabase = get_supabase_client()
    updated = supabase.update_report_status(report_id, status)
    
    if updated:
        logger.info(f"Report {report_id} status updated to {status} by {request.user.username}")
        return HttpResponse('OK', status=200)
    else:
        logger.error(f"Failed to update report {report_id} status")
        return HttpResponse('Failed to update', status=500)

@admin_required
@require_http_methods(["POST"])
def delete_report(request, report_id):
    """
    Delete a report (AJAX endpoint)
    """
    supabase = get_supabase_client()
    deleted = supabase.delete_report(report_id)
    
    if deleted:
        logger.info(f"Report {report_id} deleted by {request.user.username}")
        return HttpResponse('OK', status=200)
    else:
        logger.error(f"Failed to delete report {report_id}")
        return HttpResponse('Failed to delete', status=500)

@admin_required
@require_http_methods(["GET"])
def export_reports_csv(request):
    """
    Export all reports as CSV
    """
    supabase = get_supabase_client()
    reports = supabase.get_all_reports()
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Category', 'Location', 'Status', 'Created At', 'Description', 'Image URL'])
    
    for report in reports:
        writer.writerow([
            escape(str(report.get('id', ''))),
            escape(str(report.get('category', ''))),
            escape(str(report.get('location', ''))),
            escape(str(report.get('status', ''))),
            escape(str(report.get('created_at', ''))),
            escape(str(report.get('description', ''))),
            escape(str(report.get('image_url', ''))),
        ])
    
    logger.info(f"CSV export performed by {request.user.username}")
    return response
