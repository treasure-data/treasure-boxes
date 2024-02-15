WITH tbl_cv_history AS
(
    SELECT time, cv_name, ${user_id}, ROW_NUMBER()OVER(ORDER BY time) AS cv_id
    FROM ${td.tables.conversion_journeys}
    WHERE cv_flg = 1
    AND TD_TIME_RANGE(time, ${time_from}, ${time_to})
), tbl_join_with_cv_history AS
(
    SELECT *
    FROM
    (
        SELECT
            cv_id
            ,ROW_NUMBER()OVER(PARTITION BY raw_data.cv_name, raw_data.${user_id}, raw_data.time, activation_step_id, type ORDER BY cv_id) AS cv_order
            ,cv_history.time AS cv_time
            ,(cv_history.time - raw_data.time)/3600 AS time_hour_to_cv
            , raw_data.*
        FROM ${td.tables.conversion_journeys} raw_data
        JOIN tbl_cv_history cv_history
        ON raw_data.${user_id} = cv_history.${user_id}
        AND raw_data.cv_name = cv_history.cv_name
        WHERE raw_data.time <= cv_history.time
        AND raw_data.${user_id} <= cv_history.${user_id}
        AND type <> 'Activation'
    )
    WHERE cv_order = 1
)
,tbl_mta_base AS
(
    SELECT *
        ,MAX(position)OVER(PARTITION BY cv_id)-1 AS size_journey
        ,SUM(is_within_cv_session)OVER(PARTITION BY cv_id RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS size_cv_session
        ,GREATEST(MAX(position)OVER(PARTITION BY cv_id)-3,0) AS size_middle_click
    FROM
    (
    SELECT
        time
        ,cv_time
        ,cv_name
        ,cv_id
        ,ROW_NUMBER()OVER(PARTITION BY cv_id ORDER BY time, type) AS position --Ensure that 'Conversion' comes after 'Click' when time is the same.
        ,time_hour_to_cv
        ,CASE
            WHEN type = 'Conversion' THEN 0
            WHEN time_hour_to_cv <= ${td.mta.session_model.allowable_time_to_cv} THEN 1
            ELSE 0
        END AS is_within_cv_session
        ,(LEAD(time)OVER(PARTITION BY cv_id ORDER BY time) - time)/3600 AS time_hour_to_next
        ,time_hour_from_activation
        ,CASE
            WHEN type = 'Conversion' THEN type
            WHEN LEAD(type)OVER(PARTITION BY cv_id ORDER BY time, type) = 'Conversion' THEN 'Last Click' --Ensure that 'Conversion' comes after 'Click' when time is the same.
            WHEN LAG(type)OVER(PARTITION BY cv_id ORDER BY time, type) IS NULL THEN 'First Click' --Ensure that 'Conversion' comes after 'Click' when time is the same.
            ELSE 'Middle Click'
        END AS click_type
        ,type
        ,${user_id}
        ,activation_step_id
        ,utm_source
        ,utm_medium
        ,utm_campaign
        ,utm_content
        ,utm_connector
        ,cv_flg
        ,val
        ,revenue
        ,FIRST_VALUE(revenue)OVER(PARTITION BY cv_id ORDER BY time DESC, type DESC) AS base_revenue --Ensure that 'Conversion' comes before 'Click' when time is the same.
    FROM tbl_join_with_cv_history
    )
)

SELECT
    time
    ,cv_time
    ,${user_id}
    ,TD_MD5( CONCAT(cv_name, CAST(cv_id AS VARCHAR),CAST(cv_time AS VARCHAR),${user_id}) ) AS cv_id
    ,position
    ,time_hour_to_cv
    ,time_hour_to_next
    ,time_hour_from_activation
    ,type
    ,click_type
    ,activation_step_id
    ,utm_source
    ,utm_medium
    ,utm_campaign
    ,utm_content
    ,utm_connector
    ,cv_name
    ,size_journey
    ,size_cv_session
    ,size_middle_click
    ,is_within_cv_session
    ,revenue
    -- Last Click Model
    ,IF(click_type='Last Click',1,0) AS acquired_person_last_click_model
    ,IF(click_type='Last Click',1,0) * base_revenue AS acquired_revenue_last_click_model

    -- First Click Model
    ,CASE
        WHEN click_type='First Click' THEN 1
        WHEN click_type='Last Click' AND size_journey = 1 THEN 1
        ELSE 0
    END AS acquired_person_first_click_model
    ,CASE
        WHEN click_type='First Click' THEN 1
        WHEN click_type='Last Click' AND size_journey = 1 THEN 1
        ELSE 0
    END * base_revenue AS acquired_revenue_first_click_model

    -- Session Model
    ,CASE size_cv_session
        WHEN 0 THEN 0
        ELSE 1 * is_within_cv_session * 1.0/size_cv_session
    END AS acquired_person_session_model
    ,CASE size_cv_session
        WHEN 0 THEN 0
        ELSE 1 * is_within_cv_session * 1.0/size_cv_session * base_revenue
    END AS acquired_revenue_session_model

FROM tbl_mta_base
WHERE size_journey > 0
-- ORDER BY ${user_id}, cv_id, position