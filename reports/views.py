"""
Views for reports app - Anonymous report submission
"""

import logging
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import ReportForm
from .supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def submit_report(request):
    """
    Handle anonymous report submission
    """
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                supabase = get_supabase_client()
                
                # Upload image if provided
                image_url = None
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    image_url = supabase.upload_file(image_file)
                
                # Create report in database
                description = form.cleaned_data['description']
                category = form.cleaned_data.get('category') or None
                location = form.cleaned_data.get('location') or None
                username = form.cleaned_data.get('username') or None
                
                report = supabase.create_report(
                    description=description,
                    category=category,
                    location=location,
                    image_url=image_url,
                    username=username
                )
                
                if report:
                    return redirect('report_submitted')
                else:
                    form.add_error(None, 'Failed to submit report. Please try again.')
            
            except ValueError as e:
                # Configuration error (missing credentials)
                logger.error(f"Configuration error: {e}")
                form.add_error(None, 'The reporting system is not configured. Please contact the administrator.')
            except Exception as e:
                # Other errors (connection, table not found, etc.)
                logger.error(f"Report submission error: {e}", exc_info=True)
                error_msg = str(e)
                if 'Could not find the table' in error_msg or 'PGRST205' in error_msg:
                    form.add_error(None, 'The reporting system database is not set up. Please contact the administrator.')
                else:
                    form.add_error(None, 'An error occurred while submitting your report. Please try again later.')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'report_form.html', context)

@require_http_methods(["GET"])
def report_submitted(request):
    """
    Show confirmation page after successful submission
    """
    return render(request, 'report_submitted.html')
