-- Daily Summary Data Merge Query
-- This query appends newly generated daily summary data to the existing summary table.
-- It ensures that new data for the specific day is properly integrated into the historical data.
--
-- Parameters:
-- ${td.tmp_daily_summary_table} - The temporary table containing the newly generated summary data

SELECT *
FROM ${td.tmp_daily_summary_table}
