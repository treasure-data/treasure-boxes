---Code below creates the union of pageviews and formfills tables and adds conversion event column and channel/source columns
WITH T1 as (
select 
${time_column},
${unique_id},
td_url,
td_referrer ,
channel_id_rec ,
--Extract sources from utm_medium params and td_referrer of formfills table below. Note this need to be customized to match client specific use cases and marketing channels.
(CASE
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'affiliate' THEN 'Affiliates'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'cpm' THEN 'Display'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'email' THEN 'Email'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'organic' THEN 'Organic Search'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'cpv' THEN 'Other Advertising'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'cpc' THEN 'Paid Search'
WHEN lower(url_extract_parameter(td_url,'utm_medium'))   = 'referral' THEN 'Referral'
WHEN (lower(url_extract_parameter(td_url,'utm_source'))   = 'instagram' 
OR lower(url_extract_parameter(td_url,'utm_source'))= 'facebook' 
OR lower(url_extract_parameter(td_url,'utm_source')) = 'youtube'
OR lower(url_extract_parameter(td_url,'utm_source')) = 'twitter'
OR lower(url_extract_parameter(td_url,'utm_source')) = 'linkedin' 
OR lower(url_extract_parameter(td_url,'utm_source')) = 'pinterest'
OR lower(url_extract_parameter(td_url,'utm_source')) = 'slideshare' 
OR lower(url_extract_parameter(td_url,'utm_source')) = 'quora' ) THEN 'Social'
ELSE 'Direct'
END  ) AS ${channel_col},
(CASE WHEN url_extract_parameter(td_url,'utm_source') IS NULL THEN
 (CASE WHEN regexp_like(td_referrer,'google.co') THEN 'google'
  WHEN regexp_like(td_referrer,'instagram') THEN 'instagram'
  WHEN regexp_like(td_referrer,'facebook') THEN 'facebook'
  WHEN regexp_like(td_referrer,'youtube') THEN 'youtube'
  WHEN regexp_like(td_referrer,'twitter') THEN 'twitter'
  WHEN regexp_like(td_referrer,'linkedin') THEN 'linkedin'
  WHEN regexp_like(td_referrer,'pinterest') THEN 'pinterest'
  WHEN regexp_like(td_referrer,'slideshare') THEN 'slideshare'
  WHEN regexp_like(td_referrer,'quora') THEN 'quora'
  WHEN regexp_like(td_referrer,'yahoo') THEN 'Yahoo'
  WHEN regexp_like(td_referrer,'wikipedia') THEN 'Wikipedia'
  WHEN regexp_like(td_referrer,'duckduckgo') THEN 'DuckDuckGo'
  WHEN regexp_like(td_referrer,'bing') THEN 'Bing'
  ELSE 'DIRECT & OTHERS'
END)
  ELSE url_extract_parameter(td_url,'utm_source')
  END ) AS ${source_col} ,
    1 as ${conversion_column}
from 
${enriched_formfills}
WHERE TD_INTERVAL(${time_column}, '${time_interval}') 
--Lists which formfills we are counting as conversion. Please note that this might not be applicable to all client use cases and conversion events might need to be identified by looking at specific td_url regexp such as 'order-confirmation' etc.
AND form_id in  
(
'FORM A',
'FORM B',
'FORM C',
'FORM D',
'FORM E'
)

UNION ALL 

Select
${time_column},
${unique_id},
td_url,
td_referrer ,
channel_id_rec,
${channel_col},
${source_col},
0 as ${conversion_column}
from ${enriched_pageviews}
WHERE TD_INTERVAL(${time_column}, '${time_interval}')
)

select ${time_column}, ${unique_id}, ${channel_col}, ${source_col},
--Extract channels and sources from pageviews table
CASE
--Break down Direct sources below
WHEN ${channel_col} = 'Direct' and regexp_like(${source_col},'google') THEN 'Direct Google'
WHEN ${channel_col} = 'Direct' and regexp_like(${source_col},'facebook') THEN 'Direct Facebook'
WHEN ${channel_col} = 'Direct' and regexp_like(${source_col},'youtube') THEN 'Direct Youtube'

--Break down Display sources below
WHEN ${channel_col} = 'Display' and ${source_col} = 'dbm' THEN 'Display DBM'
WHEN ${channel_col} = 'Display' and ${source_col} = 'direct' THEN 'Display Direct'

--Break down Other Advertising sources below
WHEN ${channel_col} = 'Other Advertising' and ${source_col} = 'youtube' or ${source_col} = 'yt'  THEN 'Other Advertising YouTube'

--Break down Paid Search sources below
WHEN ${channel_col} = 'Paid Search' and regexp_like(${source_col},'google') THEN 'Paid Search Google'
WHEN ${channel_col} = 'Paid Search' and regexp_like(${source_col},'youtube') THEN 'Paid Search YouTube'
WHEN ${channel_col} = 'Paid Search' and regexp_like(${source_col},'discovery') THEN 'Paid Search Discovery'

--Break down Social sources below
WHEN ${channel_col} = 'Social' and regexp_like(${source_col},'facebook') THEN 'Social Facebook'
ELSE ${channel_col}

END as ${channel_source_col},
${conversion_column}, td_url, td_referrer, channel_id_rec
from T1