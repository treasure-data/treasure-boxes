DROP TABLE IF EXISTS ${td.database}.${td.tbl_aaa};
CREATE TABLE ${td.database}.${td.tbl_aaa} AS
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/01/05'), 'aaa.jp','aaa_001','3rd_001')
      ,(TD_TIME_PARSE('2023/01/15'), 'aaa.jp','aaa_001','3rd_002')
      ,(TD_TIME_PARSE('2023/01/25'), 'aaa.jp','aaa_001','3rd_003')
      ,(TD_TIME_PARSE('2023/02/05'), 'aaa.jp','aaa_001','3rd_004')
      ,(TD_TIME_PARSE('2023/02/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/25'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/05'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/25'), 'aaa.jp','aaa_002','3rd_009')
      ,(TD_TIME_PARSE('2023/04/05'), 'aaa.jp','aaa_002','3rd_010')
      ,(TD_TIME_PARSE('2023/04/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/25'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/05'), 'aaa.jp','aaa_003','3rd_013')
      ,(TD_TIME_PARSE('2023/05/15'), 'aaa.jp','aaa_003','3rd_014')
      ,(TD_TIME_PARSE('2023/05/25'), 'aaa.jp','aaa_003','3rd_015')
      ,(TD_TIME_PARSE('2023/06/05'), 'aaa.jp','aaa_003','3rd_016')
      ,(TD_TIME_PARSE('2023/06/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/25'), 'aaa.jp',NULL,NULL)
  ) AS t(time, site, td_client_id, td_global_id);

DROP TABLE IF EXISTS ${td.database}.${td.tbl_xxx};
CREATE TABLE ${td.database}.${td.tbl_xxx} AS
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/01/05'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/01/15'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/01/25'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/05'),'xxx.jp','xxx_001','3rd_004')
      ,(TD_TIME_PARSE('2023/02/15'),'xxx.jp','xxx_001','3rd_005')
      ,(TD_TIME_PARSE('2023/02/25'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/05'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/15'),'xxx.jp','xxx_002','3rd_008')
      ,(TD_TIME_PARSE('2023/03/25'),'xxx.jp','xxx_002','3rd_009')
      ,(TD_TIME_PARSE('2023/04/05'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/15'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/25'),'xxx.jp','xxx_003','3rd_012')
      ,(TD_TIME_PARSE('2023/05/05'),'xxx.jp','xxx_003','3rd_013')
      ,(TD_TIME_PARSE('2023/05/15'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/25'),'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/05'),'xxx.jp','xxx_004','3rd_016')
      ,(TD_TIME_PARSE('2023/06/15'),'xxx.jp','xxx_004','3rd_017')
      ,(TD_TIME_PARSE('2023/06/25'),'xxx.jp',NULL,NULL)
  ) AS t(time, site, td_client_id, td_global_id);

DROP TABLE IF EXISTS ${td.database}.${td.tbl_yyy};
CREATE TABLE ${td.database}.${td.tbl_yyy} AS
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/01/05'),'yyy.jp','yyy_001','3rd_001')
      ,(TD_TIME_PARSE('2023/01/15'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/01/25'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/05'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/15'),'yyy.jp','yyy_002','3rd_005')
      ,(TD_TIME_PARSE('2023/02/25'),'yyy.jp','yyy_002','3rd_006')
      ,(TD_TIME_PARSE('2023/03/05'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/15'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/03/25'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/05'),'yyy.jp','yyy_003','3rd_010')
      ,(TD_TIME_PARSE('2023/04/15'),'yyy.jp','yyy_003','3rd_011')
      ,(TD_TIME_PARSE('2023/04/25'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/05'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/15'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/25'),'yyy.jp','yyy_004','3rd_015')
      ,(TD_TIME_PARSE('2023/06/05'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/15'),'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/25'),'yyy.jp','yyy_005','3rd_018')
  ) AS t(time, site, td_client_id, td_global_id);

DROP TABLE IF EXISTS ${td.database}.${td.tbl_zzz};
CREATE TABLE ${td.database}.${td.tbl_zzz} AS
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/01/05'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/01/15'),'zzz.jp','zzz_001','3rd_002')
      ,(TD_TIME_PARSE('2023/01/25'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/05'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/15'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/02/25'),'zzz.jp','zzz_003','3rd_006')
      ,(TD_TIME_PARSE('2023/03/05'),'zzz.jp','zzz_003','3rd_007')
      ,(TD_TIME_PARSE('2023/03/15'),'zzz.jp','zzz_003','3rd_008')
      ,(TD_TIME_PARSE('2023/03/25'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/05'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/04/15'),'zzz.jp','zzz_004','3rd_011')
      ,(TD_TIME_PARSE('2023/04/25'),'zzz.jp','zzz_004','3rd_012')
      ,(TD_TIME_PARSE('2023/05/05'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/15'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/05/25'),'zzz.jp','zzz_005','3rd_015')
      ,(TD_TIME_PARSE('2023/06/05'),'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/15'),'zzz.jp','zzz_005','3rd_017')
      ,(TD_TIME_PARSE('2023/06/25'),'zzz.jp','zzz_005','3rd_018')
  ) AS t(time, site, td_client_id, td_global_id);