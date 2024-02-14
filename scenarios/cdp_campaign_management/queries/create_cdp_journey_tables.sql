CREATE TABLE IF NOT EXISTS ${cdp_audience_db}.${journey_jump_history_table}(
    LIKE ${cdp_audience_db}.${journey_table}
);
CREATE TABLE IF NOT EXISTS ${cdp_audience_db}.${journey_reentry_history_table}(
    LIKE ${cdp_audience_db}.${journey_table}
);