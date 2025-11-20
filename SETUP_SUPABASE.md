# Supabase Setup Guide

## ✅ Connection Status: WORKING
Your Supabase credentials are correct and the connection is successful!

## ❌ Missing: Database Table

You need to create the `reports` table in your Supabase database.

### Step-by-Step Instructions:

#### 1. Go to Supabase SQL Editor
1. Open your Supabase project: https://supabase.com/dashboard/project/dxggngekixmxghldgwpq
2. Click on "SQL Editor" in the left sidebar
3. Click "New Query"

#### 2. Run This SQL Command

Copy and paste this SQL into the editor and click "Run":

```sql
-- Create the reports table
CREATE TABLE IF NOT EXISTS public.reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  description TEXT NOT NULL,
  image_url TEXT,
  category TEXT,
  location TEXT,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow anonymous inserts (for report submission)
CREATE POLICY "Allow anonymous inserts" ON public.reports
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Create a policy to allow authenticated reads (for admin dashboard)
CREATE POLICY "Allow authenticated reads" ON public.reports
  FOR SELECT
  TO authenticated
  USING (true);

-- Create a policy to allow authenticated updates (for status changes)
CREATE POLICY "Allow authenticated updates" ON public.reports
  FOR UPDATE
  TO authenticated
  USING (true);
```

#### 3. Create Storage Bucket

1. Click on "Storage" in the left sidebar
2. Click "New bucket"
3. Name it: `report_uploads`
4. Make it **Public** (toggle the public option)
5. Click "Create bucket"

#### 4. Configure Storage Bucket Policies

After creating the bucket, click on it and go to "Policies":

```sql
-- Allow anonymous uploads
CREATE POLICY "Allow anonymous uploads" ON storage.objects
  FOR INSERT
  TO anon
  WITH CHECK (bucket_id = 'report_uploads');

-- Allow public reads
CREATE POLICY "Allow public reads" ON storage.objects
  FOR SELECT
  TO public
  USING (bucket_id = 'report_uploads');
```

#### 5. Verify Setup

Run the test script again:
```bash
venv\Scripts\python.exe test_supabase.py
```

You should see:
```
✓ ALL TESTS PASSED - Supabase is working correctly!
```

#### 6. Restart Your Server

After creating the table, refresh your admin dashboard and it should work!

---

## Quick Reference

**Your Supabase Project URL:** https://dxggngekixmxghldgwpq.supabase.co

**Table Name:** `reports`

**Bucket Name:** `report_uploads`

---

## Troubleshooting

If you still see errors after creating the table:

1. **Check table exists:**
   - Go to "Table Editor" in Supabase
   - You should see "reports" table listed

2. **Check RLS policies:**
   - Click on the reports table
   - Go to "Policies" tab
   - Ensure the policies are created

3. **Check storage bucket:**
   - Go to "Storage"
   - Ensure "report_uploads" bucket exists and is public

4. **Clear cache:**
   - Restart your Django server
   - Clear your browser cache
   - Try again
