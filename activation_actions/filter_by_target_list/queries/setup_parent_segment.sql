-- Create Parent Segment table and insert sample data
CREATE TABLE sample_db.parent_segment AS
SELECT
  anonymous_id,
  email,
  first_name,
  last_name,
  signup_date,
  created_at,
  updated_at
FROM (
  VALUES
    ('anon_001', 'user1@example.com', 'John', 'Doe', '2024-01-15', CAST(1701388800 AS BIGINT), CAST(1701388800 AS BIGINT)),
    ('anon_002', 'user2@example.com', 'Jane', 'Smith', '2024-02-20', CAST(1701388800 AS BIGINT), CAST(1701388800 AS BIGINT)),
    ('anon_003', 'user3@example.com', 'Bob', 'Johnson', '2024-03-10', CAST(1701388800 AS BIGINT), CAST(1701388800 AS BIGINT)),
    ('anon_004', 'user4@example.com', 'Alice', 'Williams', '2024-04-05', CAST(1701388800 AS BIGINT), CAST(1701388800 AS BIGINT)),
    ('anon_005', 'user5@example.com', 'Charlie', 'Brown', '2024-05-12', CAST(1701388800 AS BIGINT), CAST(1701388800 AS BIGINT))
) AS t(anonymous_id, email, first_name, last_name, signup_date, created_at, updated_at);
