SELECT ${distinct}
    t1.time
    ,${user_column}
    ,val
    ,revenue
    ,cv_name
    ,'${input_db}' AS db_name
    ,'${input_table}' AS table_name
FROM (
    SELECT
        ${time_column} AS time
        ,${inner_user_column}
        ,CAST(${val_col} AS DOUBLE) AS val
        ,CAST(${acquired_revenue_per_person} AS DOUBLE) * CAST(${val_col} AS DOUBLE) AS revenue
        ,'${cv_name}' AS cv_name
    FROM ${input_db}.${input_table}
    WHERE ${filter}
    AND TD_TIME_RANGE(${time_column}, ${time_from}, ${time_to})
) t1
${join_part}
