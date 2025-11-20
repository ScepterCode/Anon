"""
Decorators for admin panel authentication
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    """
    Decorator to require admin authentication
    """
    @wraps(view_func)
    @login_required(login_url='admin_login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper
