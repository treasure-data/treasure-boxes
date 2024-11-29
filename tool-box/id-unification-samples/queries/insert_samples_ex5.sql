INSERT INTO ${td.database}.${td.tbl_aaa}
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/06/05'), 'aaa.jp','aaa_003','3rd_016')
      ,(TD_TIME_PARSE('2023/06/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/25'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/07/05'), 'aaa.jp','aaa_004','3rd_017')
      ,(TD_TIME_PARSE('2023/07/15'), 'aaa.jp','aaa_004','3rd_018')
      ,(TD_TIME_PARSE('2023/07/25'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/05'), 'aaa.jp','aaa_005','3rd_018')
      ,(TD_TIME_PARSE('2023/08/15'), 'aaa.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/25'), 'aaa.jp','aaa_005','3rd_019')
  ) AS t(time, site, td_client_id, td_global_id);

INSERT INTO ${td.database}.${td.tbl_xxx}
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/06/05'), 'xxx.jp','xxx_004','3rd_016')
      ,(TD_TIME_PARSE('2023/06/15'), 'xxx.jp','xxx_004','3rd_017')
      ,(TD_TIME_PARSE('2023/06/25'), 'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/07/05'), 'xxx.jp','xxx_005','3rd_018')
      ,(TD_TIME_PARSE('2023/07/15'), 'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/07/25'), 'xxx.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/05'), 'xxx.jp','xxx_005','3rd_018')
      ,(TD_TIME_PARSE('2023/08/15'), 'xxx.jp','xxx_006','3rd_019')
      ,(TD_TIME_PARSE('2023/08/25'), 'xxx.jp',NULL,NULL)
  ) AS t(time, site, td_client_id, td_global_id);

INSERT INTO ${td.database}.${td.tbl_yyy}
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/06/05'), 'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/15'), 'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/25'), 'yyy.jp','yyy_005','3rd_018')
      ,(TD_TIME_PARSE('2023/07/05'), 'yyy.jp','yyy_006','3rd_019')
      ,(TD_TIME_PARSE('2023/07/15'), 'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/07/25'), 'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/05'), 'yyy.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/15'), 'yyy.jp','yyy_006','3rd_019')
      ,(TD_TIME_PARSE('2023/08/25'), 'yyy.jp','yyy_007','3rd_019')
  ) AS t(time, site, td_client_id, td_global_id);

INSERT INTO ${td.database}.${td.tbl_zzz}
SELECT
  time, site, td_client_id, td_global_id
FROM
  ( VALUES
       (TD_TIME_PARSE('2023/06/05'), 'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/06/15'), 'zzz.jp','zzz_005','3rd_017')
      ,(TD_TIME_PARSE('2023/06/25'), 'zzz.jp','zzz_005','3rd_018')
      ,(TD_TIME_PARSE('2023/07/05'), 'zzz.jp','zzz_006','3rd_018')
      ,(TD_TIME_PARSE('2023/07/15'), 'zzz.jp','zzz_007','3rd_018')
      ,(TD_TIME_PARSE('2023/07/25'), 'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/05'), 'zzz.jp',NULL,NULL)
      ,(TD_TIME_PARSE('2023/08/15'), 'zzz.jp','zzz_008','3rd_019')
      ,(TD_TIME_PARSE('2023/08/25'), 'zzz.jp',NULL,NULL)
  ) AS t(time, site, td_client_id, td_global_id);