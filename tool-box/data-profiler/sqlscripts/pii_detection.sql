SELECT 
 '${source_database}.${source_table}' as  schema 
,'${column}' as  column 
,case 
 when cast(count_if(REGEXP_LIKE(${column},'^\d{3}-\d{2}-\d{4}$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ssn
,case 
 when cast(count_if(REGEXP_LIKE(${column},'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ipaddress 
,case 
 when cast(count_if(REGEXP_LIKE(${column}, '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ipv6_address 
 ,case 
 when cast(count_if(REGEXP_LIKE(${column}, '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_email
 ,case 
 when cast(count_if(REGEXP_LIKE(${column}, '^(?:\(?([0-9]{3})\)?[-.●]?)?([0-9]{3})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 when cast(count_if(REGEXP_LIKE(${column}, '^(?:\+?1[-.●]?)?\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 when cast(count_if(REGEXP_LIKE(${column}, '^\(?([2-9][0-8][0-9])\)?[-.●]?([2-9][0-9]{2})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)> ${data_threshold} then 'Yes' 
else 'No' end as is_phone_usa
FROM ${source_database}.${source_table} TABLESAMPLE BERNOULLI(${sample_size})