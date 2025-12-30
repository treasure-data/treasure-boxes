# Journey System-Generated Tables Guide

This guide provides comprehensive documentation for the system-generated journey tables within the CDP Audience framework (`cdp_audience_{audienceid}` databases) and how to use them to trace profile movement through customer journeys.

## Table of Contents
- [Overview](#overview)
- [Journey Table Structure](#journey-table-structure)
- [Auxiliary Journey Tables](#auxiliary-journey-tables)
- [Column Naming Conventions](#column-naming-conventions)
- [Tracing Profile Movement](#tracing-profile-movement)
- [SQL Query Examples](#sql-query-examples)
- [Common Use Cases](#common-use-cases)

## Overview

The Journey system in TD-CDP-API creates a set of dynamically generated tables to track customer profiles as they move through defined journey stages. These tables are created within each audience's database (`cdp_audience_{audienceid}`) and provide detailed tracking of profile progression, timestamps, and state transitions.

### Core Architecture
- **Main Journey Table**: Tracks profile progression through stages and steps
- **Auxiliary Tables**: Support reentry, jump history, and workflow management
- **Temporal Tracking**: Precise timestamping of all profile state changes
- **Multi-Version Support**: Handles journey versioning and sibling journeys

## Journey Table Structure

### Main Journey Table: `journey_{journeyid}`

This is the primary table that tracks profiles as they move through a journey. The table structure is dynamically generated based on the journey definition.

#### Core Columns
- `cdp_customer_id`: Unique customer identifier
- `intime_journey`: Timestamp when profile enters the journey
- `outtime_journey`: Timestamp when profile exits the journey (NULL while in journey)
- `intime_goal`: Timestamp when profile reaches the journey goal

#### Dynamic Stage Columns
For each stage in the journey, the following columns are created:

- `intime_stage_{order_index}`: Entry time into stage N
- `outtime_stage_{order_index}`: Exit time from stage N
- `intime_stage_{order_index}_milestone`: Milestone achievement time

#### Exit Criteria Columns
For each exit criteria defined in a stage:

- `intime_stage_{order_index}_exit_{exit_index}`: Time when exit criteria was met

#### Step Columns
For each step within stages:

- `intime_stage_{order_index}_{step_uuid}`: Entry time into specific step
- `outtime_stage_{order_index}_{step_uuid}`: Exit time from specific step

#### Decision Point Columns
For decision point steps:

- `intime_stage_{order_index}_{step_uuid}_{segment_id}`: Entry time into specific branch
- `outtime_stage_{order_index}_{step_uuid}_{segment_id}`: Exit time from specific branch

#### A/B Test Columns
For A/B test steps:

- `intime_stage_{order_index}_{step_uuid}_variant_{variant_id}`: Entry time into specific variant
- `outtime_stage_{order_index}_{step_uuid}_variant_{variant_id}`: Exit time from specific variant

## Auxiliary Journey Tables

### 1. Standby Table: `journey_{journeyid}_standby`

Manages profiles waiting to enter other journeys via jump actions.

#### Columns:
- `session_unixtime`: Processing session timestamp
- `cdp_customer_id`: Customer identifier
- `source_journey_id`: ID of the journey the profile is jumping from
- `target_journey_id`: ID of the destination journey
- `target_journey_stage_id`: Specific stage in target journey
- `reason`: Reason for jump ('goal', 'exit', 'jump_step')

#### Usage:
```sql
-- Check profiles ready to jump to other journeys
SELECT
    cdp_customer_id,
    source_journey_id,
    target_journey_id,
    reason
FROM journey_{journey_id}_standby
WHERE target_journey_id = '{target_journey_id}'
```

### 2. Jump History Table: `journey_{journeyid}_jump_history`

Archives the historical state of profiles when they jump out of the journey.

#### Columns:
Contains all columns from the main journey table, preserving the state at jump time.

#### Usage:
```sql
-- View historical journey state for jumped profiles
SELECT
    cdp_customer_id,
    intime_journey,
    intime_stage_0,
    intime_stage_1
FROM journey_{journey_id}_jump_history
WHERE cdp_customer_id = '{customer_id}'
```

### 3. Reentry History Table: `journey_{journeyid}_reentry_history`

Tracks profiles that have re-entered the journey.

#### Stage-Specific Reentry Tables: `journey_{journeyid}_reentry_stage_{stage_order_index}`

Manages reentry at specific stages based on journey reentry mode settings.

#### Usage:
```sql
-- Check reentry history for a profile
SELECT
    cdp_customer_id,
    intime_journey,
    outtime_journey
FROM journey_{journey_id}_reentry_history
WHERE cdp_customer_id = '{customer_id}'
ORDER BY intime_journey DESC
```

### 4. Last Import Table: `journey_{journeyid}_last_import`

Tracks the last successful data import for workflow synchronization.

#### Columns:
- `time`: Import timestamp
- `last_commit_id`: Last processed commit ID

#### Usage:
```sql
-- Get latest import status
SELECT
    MAX_BY(last_commit_id, time) AS last_commit_id
FROM journey_{journey_id}_last_import
```

## Column Naming Conventions

Understanding the column naming pattern is crucial for querying journey data:

### Pattern Structure:
- **Journey Level**: `intime_journey`, `outtime_journey`, `intime_goal`
- **Stage Level**: `intime_stage_{N}`, `outtime_stage_{N}`, `intime_stage_{N}_milestone`
- **Exit Level**: `intime_stage_{N}_exit_{M}`
- **Step Level**: `intime_stage_{N}_{step_uuid}`, `outtime_stage_{N}_{step_uuid}`
- **Decision Point**: `intime_stage_{N}_{step_uuid}_{segment_id}`
- **A/B Test**: `intime_stage_{N}_{step_uuid}_variant_{variant_id}`

### Time Values:
- **Non-NULL**: Profile has reached this state
- **NULL**: Profile has not reached this state
- **Unix Timestamp**: Actual time when state was reached

## Tracing Profile Movement

### Profile States

A profile can be in one of these states:
- **Not in Journey**: `intime_journey IS NULL`
- **Active in Journey**: `intime_journey IS NOT NULL AND outtime_journey IS NULL`
- **Completed Journey**: `intime_journey IS NOT NULL AND intime_goal IS NOT NULL`
- **Exited Journey**: `intime_journey IS NOT NULL AND outtime_journey IS NOT NULL`

### Stage Progression

Profiles move through stages sequentially. Current stage can be determined by:
1. Latest non-NULL `intime_stage_N` where `outtime_stage_N IS NULL`
2. Check outside journey conditions (goal/exit criteria met)

## SQL Query Examples

### 1. Find Current Journey Status for a Profile

```sql
-- Get comprehensive journey status for a specific customer
SELECT
    cdp_customer_id,
    CASE
        WHEN intime_journey IS NULL THEN 'Not in Journey'
        WHEN outtime_journey IS NOT NULL THEN 'Exited Journey'
        WHEN intime_goal IS NOT NULL THEN 'Reached Goal'
        ELSE 'Active in Journey'
    END AS journey_status,
    intime_journey,
    outtime_journey,
    intime_goal
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}'
```

### 2. Determine Current Stage for Active Profiles

```sql
-- Find current stage for all active profiles
SELECT
    cdp_customer_id,
    CASE
        -- Check each stage in reverse order (latest first)
        WHEN intime_stage_2 IS NOT NULL AND outtime_stage_2 IS NULL THEN 'Stage 2'
        WHEN intime_stage_1 IS NOT NULL AND outtime_stage_1 IS NULL THEN 'Stage 1'
        WHEN intime_stage_0 IS NOT NULL AND outtime_stage_0 IS NULL THEN 'Stage 0'
        ELSE 'Unknown'
    END AS current_stage,
    intime_journey
FROM journey_{journey_id}
WHERE intime_journey IS NOT NULL
    AND outtime_journey IS NULL
    AND intime_goal IS NULL
```

### 3. Profile Journey Timeline

```sql
-- Create timeline of profile movement through journey
SELECT
    cdp_customer_id,
    'Journey Entry' AS event_type,
    intime_journey AS event_time
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}' AND intime_journey IS NOT NULL

UNION ALL

SELECT
    cdp_customer_id,
    'Stage 0 Entry' AS event_type,
    intime_stage_0 AS event_time
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}' AND intime_stage_0 IS NOT NULL

UNION ALL

SELECT
    cdp_customer_id,
    'Stage 0 Milestone' AS event_type,
    intime_stage_0_milestone AS event_time
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}' AND intime_stage_0_milestone IS NOT NULL

UNION ALL

SELECT
    cdp_customer_id,
    'Stage 1 Entry' AS event_type,
    intime_stage_1 AS event_time
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}' AND intime_stage_1 IS NOT NULL

-- Continue for all stages...

UNION ALL

SELECT
    cdp_customer_id,
    'Goal Reached' AS event_type,
    intime_goal AS event_time
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}' AND intime_goal IS NOT NULL

ORDER BY event_time ASC
```

### 4. Stage Conversion Rates

```sql
-- Calculate conversion rates between stages
WITH stage_counts AS (
    SELECT
        COUNT(CASE WHEN intime_stage_0 IS NOT NULL THEN 1 END) AS stage_0_entries,
        COUNT(CASE WHEN intime_stage_1 IS NOT NULL THEN 1 END) AS stage_1_entries,
        COUNT(CASE WHEN intime_stage_2 IS NOT NULL THEN 1 END) AS stage_2_entries,
        COUNT(CASE WHEN intime_goal IS NOT NULL THEN 1 END) AS goal_completions
    FROM journey_{journey_id}
    WHERE intime_journey IS NOT NULL
)
SELECT
    stage_0_entries,
    stage_1_entries,
    stage_2_entries,
    goal_completions,
    ROUND(100.0 * stage_1_entries / NULLIF(stage_0_entries, 0), 2) AS stage_0_to_1_conversion,
    ROUND(100.0 * stage_2_entries / NULLIF(stage_1_entries, 0), 2) AS stage_1_to_2_conversion,
    ROUND(100.0 * goal_completions / NULLIF(stage_0_entries, 0), 2) AS overall_conversion
FROM stage_counts
```

### 5. Exit Analysis

```sql
-- Analyze how profiles exit the journey
SELECT
    cdp_customer_id,
    CASE
        WHEN intime_goal IS NOT NULL THEN 'Completed Goal'
        WHEN intime_stage_0_exit_0 IS NOT NULL THEN 'Stage 0 Exit Criteria'
        WHEN intime_stage_1_exit_0 IS NOT NULL THEN 'Stage 1 Exit Criteria'
        WHEN outtime_journey IS NOT NULL THEN 'Other Exit'
        ELSE 'Still Active'
    END AS exit_reason,
    COALESCE(
        intime_goal,
        intime_stage_0_exit_0,
        intime_stage_1_exit_0,
        outtime_journey
    ) AS exit_time
FROM journey_{journey_id}
WHERE intime_journey IS NOT NULL
```

### 6. Time in Stage Analysis

```sql
-- Calculate time spent in each stage
SELECT
    cdp_customer_id,
    -- Time in Stage 0
    CASE
        WHEN intime_stage_0 IS NOT NULL AND outtime_stage_0 IS NOT NULL
        THEN outtime_stage_0 - intime_stage_0
        WHEN intime_stage_0 IS NOT NULL AND outtime_stage_0 IS NULL
            AND (intime_goal IS NOT NULL OR outtime_journey IS NOT NULL)
        THEN COALESCE(intime_goal, outtime_journey) - intime_stage_0
    END AS stage_0_duration_seconds,

    -- Time in Stage 1
    CASE
        WHEN intime_stage_1 IS NOT NULL AND outtime_stage_1 IS NOT NULL
        THEN outtime_stage_1 - intime_stage_1
        WHEN intime_stage_1 IS NOT NULL AND outtime_stage_1 IS NULL
            AND (intime_goal IS NOT NULL OR outtime_journey IS NOT NULL)
        THEN COALESCE(intime_goal, outtime_journey) - intime_stage_1
    END AS stage_1_duration_seconds

FROM journey_{journey_id}
WHERE intime_journey IS NOT NULL
    AND cdp_customer_id = '{customer_id}'
```

### 7. Step-Level Tracking

```sql
-- Track profile movement through specific steps in a stage
SELECT
    cdp_customer_id,
    intime_stage_0_{step_uuid_1} AS step_1_entry,
    outtime_stage_0_{step_uuid_1} AS step_1_exit,
    intime_stage_0_{step_uuid_2} AS step_2_entry,
    outtime_stage_0_{step_uuid_2} AS step_2_exit,
    CASE
        WHEN outtime_stage_0_{step_uuid_1} IS NOT NULL AND intime_stage_0_{step_uuid_2} IS NOT NULL
        THEN intime_stage_0_{step_uuid_2} - outtime_stage_0_{step_uuid_1}
    END AS step_transition_time_seconds
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}'
    AND intime_stage_0 IS NOT NULL
```

### 8. Jump and Reentry Tracking

```sql
-- Find profiles that have jumped or re-entered
SELECT
    j.cdp_customer_id,
    'Jump' AS movement_type,
    jh.intime_journey AS original_entry,
    j.intime_journey AS new_entry,
    s.target_journey_id,
    s.reason
FROM journey_{journey_id} j
LEFT JOIN journey_{journey_id}_jump_history jh
    ON j.cdp_customer_id = jh.cdp_customer_id
LEFT JOIN journey_{journey_id}_standby s
    ON j.cdp_customer_id = s.cdp_customer_id
WHERE jh.cdp_customer_id IS NOT NULL OR s.cdp_customer_id IS NOT NULL

UNION ALL

SELECT
    r.cdp_customer_id,
    'Reentry' AS movement_type,
    r.intime_journey AS original_entry,
    j.intime_journey AS new_entry,
    NULL AS target_journey_id,
    'Reentry' AS reason
FROM journey_{journey_id}_reentry_history r
JOIN journey_{journey_id} j
    ON r.cdp_customer_id = j.cdp_customer_id
WHERE r.intime_journey < j.intime_journey
```

## Common Use Cases

### 1. Journey Performance Analysis
- Track conversion rates at each stage
- Identify bottlenecks and drop-off points
- Measure time to completion
- Compare performance across different journey versions

### 2. Customer Behavior Analysis
- Understand profile progression patterns
- Identify common exit points
- Analyze reentry behavior
- Track engagement over time

### 3. A/B Testing Analysis
- Compare variant performance in A/B test steps
- Measure impact of different journey paths
- Track decision point branch selection

### 4. Operational Monitoring
- Monitor active profile counts
- Track system performance and data flow
- Identify processing issues
- Manage jump and reentry scenarios

### 5. Personalization
- Use journey state for real-time personalization
- Trigger actions based on stage progression
- Customize experiences based on journey history

## Best Practices

1. **Column Existence**: Always check if columns exist before querying, as journey structure can vary
2. **NULL Handling**: Use proper NULL checks when determining profile states
3. **Time Calculations**: Remember timestamps are in Unix format (seconds since epoch)
4. **Performance**: Use appropriate indexes on `cdp_customer_id` and time columns
5. **Version Awareness**: Consider journey versioning when analyzing historical data
6. **Reentry Logic**: Account for reentry modes when analyzing profile behavior

## Performance Considerations

- **Indexing**: Ensure proper indexes on frequently queried columns
- **Query Optimization**: Use specific column selection rather than SELECT *
- **Time Ranges**: Add time range filters to improve query performance
- **Join Strategies**: Be mindful of join performance with large customer tables
- **Caching**: Consider caching frequently accessed journey metadata

---

This documentation provides the foundation for effectively querying and analyzing journey data within the TD-CDP-API system. For specific implementation details or advanced use cases, refer to the source code in `app/models/journey/` and related journey modules.