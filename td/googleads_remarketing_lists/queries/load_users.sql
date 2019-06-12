SELECT 
  email
FROM (
  VALUES('demo1@example.com') ,
  ('demo2@example.com') ,
  ('demo3@example.com')
  ) tbl(email)