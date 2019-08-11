select distinct cast(LOWER(COALESCE(URL_EXTRACT_PARAMETER(td_url, '${utm_param}'), 'organic')) as varchar(20)) AS ad_response,
concat(LOWER(COALESCE(URL_EXTRACT_PARAMETER(td_url, '${utm_param}'), 'organic')), '_ad_response_percentile') as var_name
from  ${td.activity_table}
