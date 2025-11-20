"""
URLs for admin panel
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('report/<str:report_id>/', views.report_detail, name='report_detail'),
    path('report/<str:report_id>/status/', views.update_report_status, name='update_report_status'),
    path('report/<str:report_id>/delete/', views.delete_report, name='delete_report'),
    path('export/csv/', views.export_reports_csv, name='export_reports_csv'),
]
