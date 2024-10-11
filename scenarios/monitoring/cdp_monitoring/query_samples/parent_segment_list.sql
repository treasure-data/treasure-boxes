select 
  id, name, 
  JSON_EXTRACT_SCALAR(JSON_PARSE(createdby), '$.name') as createdby, 
  JSON_EXTRACT_SCALAR(JSON_PARSE(updatedby), '$.name') as updatedby
from parent_segments_configuration