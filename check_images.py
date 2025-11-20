"""Check image URLs in reports"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from reports.supabase_client import get_supabase_client

client = get_supabase_client()
reports = client.get_all_reports()

print(f"Total reports: {len(reports)}\n")

for i, report in enumerate(reports[:5], 1):
    print(f"Report {i}:")
    print(f"  ID: {report.get('id')}")
    print(f"  Description: {report.get('description')[:50]}...")
    print(f"  Image URL: {report.get('image_url')}")
    print(f"  Has image: {'Yes' if report.get('image_url') else 'No'}")
    print()
