WITH users AS (
  SELECT * FROM (
    VALUES
      (1, 'John', 'Doe', 'john.doe@example.com'),
      (2, 'Jane', 'Smith', 'jane.smith@example.com'),
      (3, 'Jean', 'Dupont', 'jean.dupont@example.com')
  ) AS t(user_id, first_name, last_name, email)
), login_frequency AS (
  SELECT user_id, COUNT(1) AS num_logins FROM (
    VALUES
      (1, '2022-07-06 12:00:34'),
      (2, '2022-07-06 13:20:22'),
      (1, '2022-07-16 02:12:17'),
      (3, '2022-07-17 00:00:19'),
      (1, '2022-07-26 19:10:39'),
      (3, '2022-07-28 11:58:01'),
      (1, '2022-07-28 21:07:27')
  ) AS t(user_id, login_at)
  GROUP BY user_id
)
SELECT
  u.email, u.last_name, u.first_name,
  CASE NTILE(4) OVER (ORDER BY lf.num_logins)
    WHEN 1 THEN 'bottom_25'
    WHEN 4 THEN 'top_25'
    ELSE 'middle_50'
  END AS usage_segment
FROM login_frequency lf JOIN users u ON lf.user_id = u.user_id
