select 
  JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.audienceId') as parent_segment_id,
  id,
  JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.name') as name,
  type
from entities
order by 1, 2