-- Create Target List table and insert sample data
CREATE TABLE IF NOT EXISTS integration_db.campaign_target_list AS
SELECT
  anonymous_id,
  campaign_id,
  campaign_name,
  priority
FROM (
  VALUES
    ('anon_001', 'campaign_2024_winter', 'Winter Sale 2024', 1),
    ('anon_003', 'campaign_2024_winter', 'Winter Sale 2024', 2),
    ('anon_005', 'campaign_2024_winter', 'Winter Sale 2024', 3)
) AS t(anonymous_id, campaign_id, campaign_name, priority);
