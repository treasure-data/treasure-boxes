WITH tbl_act AS (
    SELECT
        TD_TIME_PARSE(createdat,'${td.timezone}') AS time
        ,audienceid AS ps_id
        ,IF(j_act.syndication_id IS NULL, segmentid, activation_step_id ) AS activation_id
        ,segmentid AS segment_id
        ,name AS activation_name
        ,id AS syndication_id
        ,activation_step_id
        ,IF(j_act.syndication_id IS NULL, 'segment', 'journeyActivationStep' ) AS activation_type
        ,scheduletype AS schedule_type
        ,scheduleoption AS schedule_option
        ,timezone
        ,createdat
        ,updatedat
        ,journey_id
        ,connectionid AS connection_id
    FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.activations} act
    LEFT OUTER JOIN
    (
        SELECT
            id AS activation_step_id
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes),'$.syndicationId') AS syndication_id
            ,journey_id
        FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.journey_activation}
    ) j_act
    ON act.id = j_act.syndication_id
    WHERE ps_id = '${ps_id}'
    AND TD_TIME_RANGE(TD_TIME_PARSE(createdat,'${td.timezone}'), ${time_from}, ${time_to})
)
, tbl_step_ids AS(
    SELECT
        -- time
        REPLACE(step_id, '-', '_') AS step_id
        ,JSON_EXTRACT_SCALAR(jsn, '$.journeyActivationStepId') AS activation_step_id
        ,JSON_EXTRACT_SCALAR(jsn, '$.type') AS type
        ,stage_name
        ,stage_no
        -- ,ps_id
        ,state
        -- ,created_at
        -- ,updated_at
        ,journey_name
    FROM
    (
        SELECT
            elm
            ,CAST(idx-1 AS INTEGER) AS stage_no
            ,TD_TIME_PARSE(
                JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt')
                ,'${td.timezone}'
            ) AS time
            ,JSON_EXTRACT_SCALAR(elm, '$.name') AS stage_name
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.audienceId') AS ps_id
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.state') AS state
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt') AS created_at
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.updatedAt') AS updated_at
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.name') AS journey_name
        FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.journey_summary}
        CROSS JOIN UNNEST(CAST(JSON_EXTRACT(JSON_PARSE(attributes), '$.journeyStages') AS ARRAY(JSON))) WITH ORDINALITY AS t(elm, idx)
    )
    CROSS JOIN UNNEST(
        MAP_KEYS(CAST(JSON_EXTRACT(elm, '$.steps') AS MAP(VARCHAR, JSON)))
        , MAP_VALUES(CAST(JSON_EXTRACT(elm, '$.steps') AS MAP(VARCHAR, JSON)))
    ) AS t(step_id, jsn)
    WHERE JSON_EXTRACT_SCALAR(jsn, '$.type') = 'Activation'
)
,tbl_conn AS (
    SELECT
        id AS connection_id
        ,IF(
            STARTS_WITH(conn.url,'{')
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(conn.url), '$.type')
            ,SPLIT_PART(conn.url, '://', 1)
        ) AS connector_type
    FROM ${td.monitoring.db.basic_monitoring}.${td.monitoring.tables.connections_details} conn_d
    JOIN ${td.monitoring.db.basic_monitoring}.${td.monitoring.tables.connections} conn
    ON conn_d.name = conn.name
)

SELECT
    act.*
    ,conn.connector_type
    ,step_ids.step_id
    ,step_ids.stage_name
    ,step_ids.stage_no
    ,step_ids.state
    -- ,step_ids.created_at
    -- ,step_ids.updated_at
    ,step_ids.journey_name
FROM tbl_act act
LEFT OUTER JOIN tbl_conn conn
ON CAST(act.connection_id AS VARCHAR) = CAST(conn.connection_id AS VARCHAR)
LEFT OUTER JOIN tbl_step_ids step_ids
ON act.activation_step_id = step_ids.activation_step_id


-- WITH tbl_act AS (
--     SELECT
--         journey_id
--         ,id AS activation_step_id
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.syndicationId') AS syndication_id
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.name') AS activation_name
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.scheduleType') AS schedule_type
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.scheduleOption') AS schedule_option
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.timezone') AS timezone
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.connectionId') AS connection_id
--         ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.activationParams.allColumns') AS all_columns
--     FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.journey_activation}
-- )
-- , tbl_step_ids AS(
--     SELECT
--         time
--         ,REPLACE(step_id, '-', '_') AS step_id
--         ,JSON_EXTRACT_SCALAR(jsn, '$.journeyActivationStepId') AS activation_step_id
--         ,JSON_EXTRACT_SCALAR(jsn, '$.type') AS type
--         ,stage_name
--         ,stage_no
--         ,ps_id
--         ,state
--         ,created_at
--         ,updated_at
--         ,journey_name
--     FROM
--     (
--         SELECT
--             elm
--             ,idx-1 AS stage_no
--             ,TD_TIME_PARSE(
--                 JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt')
--                 ,'${td.timezone}'
--             ) AS time
--             ,JSON_EXTRACT_SCALAR(elm, '$.name') AS stage_name
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.audienceId') AS ps_id
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.state') AS state
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.createdAt') AS created_at
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.updatedAt') AS updated_at
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.name') AS journey_name
--         FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.journey_summary}
--         CROSS JOIN UNNEST(CAST(JSON_EXTRACT(JSON_PARSE(attributes), '$.journeyStages') AS ARRAY(JSON))) WITH ORDINALITY AS t(elm, idx)
--     )
--     CROSS JOIN UNNEST(
--         MAP_KEYS(CAST(JSON_EXTRACT(elm, '$.steps') AS MAP(VARCHAR, JSON)))
--         , MAP_VALUES(CAST(JSON_EXTRACT(elm, '$.steps') AS MAP(VARCHAR, JSON)))
--     ) AS t(step_id, jsn)
--     WHERE JSON_EXTRACT_SCALAR(jsn, '$.type') = 'Activation'
-- )
-- ,tbl_conn AS (
--     SELECT
--         id AS connection_id
--         ,IF(
--             STARTS_WITH(conn.url,'{')
--             ,JSON_EXTRACT_SCALAR(JSON_PARSE(conn.url), '$.type')
--             ,SPLIT_PART(conn.url, '://', 1)
--         ) AS connector_type
--     FROM ${td.monitoring.db.basic_monitoring}.${td.monitoring.tables.connections_details} conn_d
--     JOIN ${td.monitoring.db.basic_monitoring}.${td.monitoring.tables.connections} conn
--     ON conn_d.name = conn.name
-- )


-- SELECT
--     step_ids.time
--     ,act.*
--     ,step_ids.step_id
--     ,step_ids.stage_name
--     ,step_ids.stage_no
--     ,step_ids.state
--     ,step_ids.created_at
--     ,step_ids.updated_at
--     ,step_ids.journey_name
--     ,conn.connector_type
--     FROM tbl_act act
-- LEFT OUTER JOIN tbl_step_ids step_ids
-- ON act.activation_step_id = step_ids.activation_step_id
-- AND step_ids.ps_id = '${ps_id}'
-- LEFT OUTER JOIN tbl_conn conn
-- ON CAST(act.connection_id AS VARCHAR) = CAST(conn.connection_id AS VARCHAR)
-- WHERE TD_TIME_RANGE(step_ids.time, ${time_from}, ${time_to})
