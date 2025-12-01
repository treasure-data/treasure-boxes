-- Sample data setup queries
-- This file provides reference examples for setting up test data
--
-- Database structure:
--   - sample_db: Database where Parent Segment is stored
--   - integration_db: Database where target table is stored

-- ============================================
-- 1. Parent Segment Table
-- ============================================
-- Database: sample_db
-- Table: parent_segment
-- In Activation Actions, this is passed as activation_actions_table parameter
-- with fully qualified name (sample_db.parent_segment)

-- Parent Segment table sample structure:
/*
CREATE TABLE IF NOT EXISTS sample_db.parent_segment (
  anonymous_id VARCHAR,
  email VARCHAR,
  first_name VARCHAR,
  last_name VARCHAR,
  signup_date VARCHAR,
  created_at BIGINT,
  updated_at BIGINT
);
*/

-- Parent Segment sample data:
/*
INSERT INTO sample_db.parent_segment VALUES
  ('anon_001', 'user1@example.com', 'John', 'Doe', '2024-01-15', 1701388800, 1701388800),
  ('anon_002', 'user2@example.com', 'Jane', 'Smith', '2024-02-20', 1701388800, 1701388800),
  ('anon_003', 'user3@example.com', 'Bob', 'Johnson', '2024-03-10', 1701388800, 1701388800),
  ('anon_004', 'user4@example.com', 'Alice', 'Williams', '2024-04-05', 1701388800, 1701388800),
  ('anon_005', 'user5@example.com', 'Charlie', 'Brown', '2024-05-12', 1701388800, 1701388800);
*/

-- ============================================
-- 2. Target List Table
-- ============================================
-- Database: integration_db (different from Parent Segment database)
-- Table: campaign_target_list
-- Specified as target_table_name parameter in String Builder

-- Target list table sample structure:
/*
CREATE TABLE IF NOT EXISTS integration_db.campaign_target_list (
  anonymous_id VARCHAR,
  campaign_id VARCHAR,
  campaign_name VARCHAR,
  priority INT
);
*/

-- Target list sample data:
-- Only anonymous_ids in this table will be included in the filtered result
/*
INSERT INTO integration_db.campaign_target_list VALUES
  ('anon_001', 'campaign_2024_winter', 'Winter Sale 2024', 1),
  ('anon_003', 'campaign_2024_winter', 'Winter Sale 2024', 2),
  ('anon_005', 'campaign_2024_winter', 'Winter Sale 2024', 3);
*/

-- ============================================
-- Expected Result
-- ============================================
-- Out of 5 records in Parent Segment, only 3 records (anon_001, anon_003, anon_005)
-- that exist in the target list (integration_db.campaign_target_list) will be included
-- in the filtered result.
--
-- Output columns include all columns from Parent Segment only:
--   - anonymous_id
--   - email
--   - first_name
--   - last_name
--   - signup_date
--   - created_at
--   - updated_at
--
-- Target table columns (campaign_id, campaign_name, priority) are NOT included.

-- ============================================
-- Test Execution Command
-- ============================================
-- td wf run filter_by_target_list.dig \
--   -p activation_actions_db=sample_db \
--   -p activation_actions_table=sample_db.parent_segment \
--   -p integration_db=integration_db \
--   -p target_table_name=campaign_target_list
