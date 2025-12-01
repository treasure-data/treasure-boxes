-- Join Parent Segment with specified target table using anonymous_id
-- Filter to include only records that exist in the target table
-- Parameters passed from Activation Actions:
--   - activation_actions_table: Parent Segment table name (fully qualified: database.table)
--   - integration_db: Database where target table is stored
--   - target_table_name: Target table name specified in String Builder

-- Returns all columns from Parent Segment (excluding target table columns)
SELECT
  ps.*
FROM
  ${activation_actions_table} ps
INNER JOIN
  ${integration_db}.${target_table_name} target
ON
  ps.anonymous_id = target.anonymous_id
WHERE
  ps.email IS NOT NULL  -- Only records with email
  AND ps.anonymous_id IS NOT NULL  -- Only records with anonymous_id
