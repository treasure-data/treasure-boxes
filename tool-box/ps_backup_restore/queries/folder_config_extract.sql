SELECT CAST(json_extract(relationships, '$.parentFolder.data.id') as int) parent_node_id,
       CAST(json_extract(relationships, '$.parentFolder.data.type') as VARCHAR) parent_node_type,
       CAST(id AS INT) current_node_id,
       CAST(type AS VARCHAR) current_node_type,
       CAST(json_extract(attributes, '$.name') AS VARCHAR) current_node_name,
       CAST(json_extract(attributes, '$.description') AS VARCHAR) current_node_desc
FROM ${td.database}.${backup.stg_folder_curr_config_tbl};