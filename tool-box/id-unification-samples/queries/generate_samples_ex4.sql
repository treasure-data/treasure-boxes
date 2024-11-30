DROP TABLE IF EXISTS ${td.database}.${td.tbl_aaa};
CREATE TABLE ${td.database}.${td.tbl_aaa} AS
SELECT
  member_id, email, tel, name
FROM
  ( VALUES
     ('1', 'a@ex.com',1111,'Taka')
    ,('2', 'a@ex.com',2222,'Tatsuo')
    ,('3', 'b@ex.com',3333,'Naruse')
    ,('3', 'b@ex.com',4444,'Yuichiro')
    ,(NULL,'c@ex.com',5555,'Minero')
    ,(NULL,'c@ex.com',6666,'Kaz')
  ) AS t(member_id, email, tel, name);