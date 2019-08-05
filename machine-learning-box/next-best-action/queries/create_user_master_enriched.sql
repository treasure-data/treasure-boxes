select A.*, (
            CASE
              WHEN B.code IS NULL THEN 0
              ELSE 1
            END
          ) AS cart_abandon,
          (
            CASE
              WHEN C.num_visits IS NULL THEN 0
              ELSE 1
            END
          ) AS new_visitor_no_ads
from ${td.user_master_table} A
LEFT join ${td.nba_retarget_table} B
on A.td_client_id = B.td_client_id
LEFT join ${td.nba_awareness_table} C
on A.td_client_id = C.td_client_id
