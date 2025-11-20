"""
Quick test script to verify Supabase connection
Run with: venv\\Scripts\\python.exe test_supabase.py
"""
import os
import sys
import django

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from reports.supabase_client import get_supabase_client

print("=" * 60)
print("SUPABASE CONNECTION TEST")
print("=" * 60)

print(f"\n1. Configuration Check:")
print(f"   SUPABASE_URL: {settings.SUPABASE_URL}")
print(f"   SUPABASE_KEY: {settings.SUPABASE_KEY[:20]}..." if settings.SUPABASE_KEY else "   SUPABASE_KEY: Not set")
print(f"   SUPABASE_BUCKET: {settings.SUPABASE_BUCKET}")

print(f"\n2. Testing Connection...")
try:
    client = get_supabase_client()
    print("   ✓ Supabase client initialized successfully")
    
    print(f"\n3. Testing Database Query...")
    reports = client.get_all_reports()
    print(f"   ✓ Successfully fetched {len(reports)} reports")
    
    if len(reports) > 0:
        print(f"\n4. Sample Report:")
        report = reports[0]
        print(f"   ID: {report.get('id')}")
        print(f"   Status: {report.get('status')}")
        print(f"   Created: {report.get('created_at')}")
    else:
        print(f"\n4. No reports found in database")
        print(f"   This is normal if you haven't submitted any reports yet")
    
    print(f"\n" + "=" * 60)
    print("✓ ALL TESTS PASSED - Supabase is working correctly!")
    print("=" * 60)
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    print(f"\n" + "=" * 60)
    print("✗ TEST FAILED - Please check your configuration")
    print("=" * 60)
    print(f"\nTroubleshooting:")
    print(f"1. Verify your Supabase URL is correct")
    print(f"2. Verify your Supabase API key is correct")
    print(f"3. Check if the 'reports' table exists in your Supabase database")
    print(f"4. Ensure your internet connection is working")
    import traceback
    print(f"\nFull error details:")
    traceback.print_exc()
