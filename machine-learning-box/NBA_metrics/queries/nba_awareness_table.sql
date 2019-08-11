SELECT td_client_id, count(td_url) as num_visits from ${td.original_pageviews}
            WHERE (
                td_url NOT LIKE '%utm_campaign%'
                OR td_url NOT LIKE '%utm_source%'
                OR td_url NOT LIKE '%utm_medium%'
              )
              group by td_client_id
              having count(td_url) <= 1
