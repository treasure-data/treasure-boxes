SELECT
      DISTINCT td_client_id,
      4 AS code
    FROM (
        SELECT
          td_client_id,
          session_id,
          row_number(
          ) over(
            partition BY session_id,
            td_client_id
          ORDER BY
            time DESC
          ) AS rnum,
          flag
        FROM (
            SELECT
              td_client_id,
              TD_SESSIONIZE_WINDOW(
                time,
                3600 * 24
              ) OVER(
                PARTITION BY td_client_id,
                td_ip
              ORDER BY
                time
              ) AS session_id,
              time,
              (
                CASE
                  WHEN td_url = 'https://www.varidesk.com/cart' THEN 1
                  ELSE 0
                END
              ) AS flag
            FROM
              pageviews A
            WHERE
              td_url IN(
                'https://www.varidesk.com/cart',
                'https://www.varidesk.com/order-confirmation'
              )
          )
      )
    WHERE
      rnum = 1
      AND flag = 1.
