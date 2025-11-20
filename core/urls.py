"""
Core URL configuration
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('submit_report'), name='home'),
    path('reports/', include('reports.urls')),
    path('admin/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
