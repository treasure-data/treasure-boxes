WITH login_frequency AS (
  SELECT user_id, COUNT(1) AS num_logins FROM login GROUP BY user_id
)
SELECT
  u.email, u.last_name, u.first_name,
  CASE NTILE(4) OVER (ORDER BY lf.num_logins)
    WHEN 1 THEN 'bottom_25'
    WHEN 4 THEN 'top_25'
    ELSE 'middle_50'
  END AS usage_segment
FROM login_frequency lf JOIN users u ON lf.user_id = u.user_id