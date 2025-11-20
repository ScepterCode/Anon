-- Fix Row Level Security Policies for Reports Table
-- Run this in your Supabase SQL Editor

-- First, drop any existing policies
DROP POLICY IF EXISTS "Allow anonymous inserts" ON public.reports;
DROP POLICY IF EXISTS "Allow authenticated reads" ON public.reports;
DROP POLICY IF EXISTS "Allow authenticated updates" ON public.reports;
DROP POLICY IF EXISTS "Enable insert for anon users" ON public.reports;
DROP POLICY IF EXISTS "Enable read for authenticated users" ON public.reports;
DROP POLICY IF EXISTS "Enable update for authenticated users" ON public.reports;

-- Disable RLS temporarily to test (OPTIONAL - for testing only)
-- ALTER TABLE public.reports DISABLE ROW LEVEL SECURITY;

-- OR keep RLS enabled and create proper policies:

-- Policy 1: Allow anonymous users to INSERT reports
CREATE POLICY "Enable insert for anon users" 
ON public.reports
FOR INSERT 
TO anon
WITH CHECK (true);

-- Policy 2: Allow authenticated users to SELECT (read) all reports
CREATE POLICY "Enable read for authenticated users" 
ON public.reports
FOR SELECT 
TO authenticated
USING (true);

-- Policy 3: Allow authenticated users to UPDATE reports
CREATE POLICY "Enable update for authenticated users" 
ON public.reports
FOR UPDATE 
TO authenticated
USING (true)
WITH CHECK (true);

-- Policy 4: Allow public to SELECT (optional - for public viewing)
CREATE POLICY "Enable read for public" 
ON public.reports
FOR SELECT 
TO public
USING (true);

-- Verify policies were created
SELECT schemaname, tablename, policyname, roles, cmd 
FROM pg_policies 
WHERE tablename = 'reports';
