select
  mail as "Emal Address"
  ,mail as "Subscriber Key"
  ,name as "Full Name"
from (
  VALUES
      ('foo@example.com', 'John Doe'),
      ('bar@example.com', 'Jane Smith'),
      ('baz@example.com', 'Taro Yamada')
) AS t(mail, name)
