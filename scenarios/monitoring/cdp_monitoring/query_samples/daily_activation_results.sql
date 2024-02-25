WITH tbl_jobs AS
(
    SELECT
        REGEXP_EXTRACT(query, 'attempt_id: ([\d]+)',1) AS workflow_attempt_id
        ,REGEXP_EXTRACT(query, 'project_name: cdp_journey_([\d]+)',1) AS journey_id
        , *
    FROM basic_monitoring.jobs
    WHERE REGEXP_LIKE(query, 'task_name: \+syndication_[\d]*\+syndicate\^sub(?!\+)')
)
,tbl_act_hst AS
(
    SELECT
        TD_TIME_PARSE(JSON_EXTRACT_SCALAR(exe, '$.createdAt'), 'UTC') AS time
        ,TD_TIME_PARSE(JSON_EXTRACT_SCALAR(exe, '$.finishedAt'), 'UTC') AS time_finished
        ,id AS syndication_id
        ,name AS activation_name
        ,JSON_EXTRACT_SCALAR(exe, '$.workflowId') AS workflow_id
        ,JSON_EXTRACT_SCALAR(exe, '$.workflowSessionId') AS workflow_session_id
        ,JSON_EXTRACT_SCALAR(exe, '$.workflowAttemptId') AS workflow_attempt_id
        ,JSON_EXTRACT_SCALAR(exe, '$.createdAt') AS created_at
        ,JSON_EXTRACT_SCALAR(exe, '$.finishedAt') AS finished_at
        ,JSON_EXTRACT_SCALAR(exe, '$.status') AS status
    FROM
        cdp_monitoring.activations
    CROSS JOIN UNNEST(CAST(JSON_PARSE(executions) AS ARRAY(JSON))) AS t(exe)
)

SELECT act_hst.*
    ,jobs.journey_id
    ,CAST(CAST(jobs.num_records AS DOUBLE) AS BIGINT) AS num_records
    ,IF(
        STARTS_WITH(jobs.result,'{')
        ,JSON_EXTRACT_SCALAR(JSON_PARSE(jobs.result), '$.type')
        ,SPLIT_PART(jobs.result, '://', 1)
    ) AS connector_type
FROM tbl_act_hst act_hst
LEFT OUTER JOIN tbl_jobs jobs
ON act_hst.workflow_attempt_id = jobs.workflow_attempt_id
ORDER BY time DESC