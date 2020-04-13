-- Create a destination table based on a staging table.
CREATE
  TABLE
    IF NOT EXISTS ${table} AS SELECT
       *
    FROM
      ${table}_stg
;

-- Deduplication (Delete records from the destination if delivery_id is in the staging.)
DELETE
FROM
  ${table}
WHERE
  TD_TIME_RANGE(time,
    DATE_FORMAT(DATE_ADD('day',
        -14,
        NOW()),
      '%Y-%m-%d %H:%i:%s'),
    NULL,
    'JST')
  AND delivery_id IN(
    SELECT
      DISTINCT delivery_id
    FROM
      ${table}_stg
  )
;

-- Merge records in the staging into the destination.
INSERT
  INTO
    ${table} SELECT
       *
    FROM
      ${table}_stg
;

-- Drop the staging table.
DROP
  TABLE
    IF EXISTS ${table}_stg
;
