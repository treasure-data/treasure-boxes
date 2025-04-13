SELECT t2.email, t1.* FROM 
(SELECT * FROM ${activation_actions_table}) t1
LEFT JOIN
(SELECT ${raw_email_column} as email FROM ${raw_email_db_table}) t2
ON t1.hashed_email = TO_HEX(SHA256(TO_UTF8(lower(email))))

