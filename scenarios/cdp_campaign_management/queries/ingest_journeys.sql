SELECT
    TD_TIME_PARSE(JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt'),'${user_timezone}') AS time
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.audienceId') AS audience_id
    ,id
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.name') AS name
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.state') AS state
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt') AS created_at
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.updatedAt') AS updated_at
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.launchedAt') AS launched_at
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.allowReentry') AS allow_reentry
    ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.paused') AS paused
    ,JSON_ARRAY_LENGTH(JSON_EXTRACT(JSON_PARSE(attributes), '$.journeyStages')) AS num_stages
FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.entities}
WHERE type = 'journey'
AND JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.audienceId') = '${ps_id}'
AND TD_TIME_RANGE(
    TD_TIME_PARSE(JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt'),'${user_timezone}')
    ,${time_from}
    ,${time_to}
)