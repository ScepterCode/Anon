-- Add username column to reports table
-- Run this in your Supabase SQL Editor

ALTER TABLE public.reports 
ADD COLUMN IF NOT EXISTS username TEXT;

-- Verify the column was added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'reports' 
ORDER BY ordinal_position;
