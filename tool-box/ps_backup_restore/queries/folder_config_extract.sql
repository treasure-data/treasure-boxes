WITH records AS (
  select CAST(json_extract(config, '$.data') as ARRAY<JSON>) records from ${td.database}.${backup.stg_folder_curr_config_tbl}
)
SELECT CAST(json_extract(record, '$.relationships.parentFolder.data.id') as int) parent_node_id,
       CAST(json_extract(record, '$.relationships.parentFolder.data.type') as VARCHAR) parent_node_type,
       CAST(json_extract(record, '$.id') AS INT) current_node_id,
       CAST(json_extract(record, '$.type') AS VARCHAR) current_node_type,
       CAST(json_extract(record, '$.attributes.name') AS VARCHAR) current_node_name,
       CAST(json_extract(record, '$.attributes.description') AS VARCHAR) current_node_desc
       FROM records CROSS JOIN UNNEST(records) AS t(record);