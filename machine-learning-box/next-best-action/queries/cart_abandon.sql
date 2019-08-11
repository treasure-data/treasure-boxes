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
                3600 * ${td.session_length_hours}
              ) OVER(
                PARTITION BY td_client_id,
                td_ip
              ORDER BY
                time
              ) AS session_id,
              time,
              (
                CASE
                  WHEN td_url = ${td.cart_url} THEN 1
                  ELSE 0
                END
              ) AS flag
            FROM
              pageviews A
            WHERE
              td_url IN(
                ${td.cart_url},
                ${td.purchase_url}
              )
          )
      )
    WHERE
      rnum = 1
      AND flag = 1.
