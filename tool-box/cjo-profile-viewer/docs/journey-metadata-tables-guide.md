# Journey Metadata Tables Guide: Profile Timeline Tracking

This comprehensive guide explains how to use the Treasure Data CDP journey metadata tables to create detailed timelines of customer profile movements through journeys.

## Overview

The TD-CDP-API uses a sophisticated system of dynamically generated tables and columns to track customer journeys with precise timestamps. Each journey creates multiple tables that track profile movements at different levels of granularity:

- **Journey-level**: Entry and exit from the entire journey
- **Stage-level**: Entry and exit from each stage within the journey
- **Step-level**: Entry and exit from individual steps within stages
- **Milestone/Exit-level**: When profiles satisfy specific criteria

## Core Table Structure

### Primary Journey Table
**Table Name Pattern**: `journey_{journey_id}`

This is the main table that tracks all profile movements for a specific journey. Each row represents a customer profile (identified by `cdp_customer_id`) and contains timestamps for their journey progression.

### Supporting Metadata Tables

1. **journeys**: Core journey definitions and configuration
2. **journey_stages**: Stage definitions within journeys
3. **journey_statistics**: Aggregated journey-level metrics
4. **journey_stage_statistics**: Aggregated stage-level metrics
5. **journey_active_windows**: Journey execution periods

### Dynamically Generated Tables

These tables are created during journey execution:

1. **journey_{journey_id}_standby**: Profiles waiting to enter from other journeys
2. **journey_{journey_id}_jump_history**: Historical record of profiles jumping between journeys
3. **journey_{journey_id}_reentry_history**: Historical record of profiles re-entering journeys

## Column Naming Convention

The journey system uses a consistent naming pattern for tracking profile movements:

### Intime Columns (Entry Timestamps)
- `intime_journey`: When profile entered the journey
- `intime_stage_{stage_index}`: When profile entered a specific stage
- `intime_stage_{stage_index}_milestone`: When profile reached stage milestone
- `intime_stage_{stage_index}_exit_{exit_index}`: When profile met exit criteria
- `intime_stage_{stage_index}_{step_uuid}`: When profile entered a specific step
- `intime_goal`: When profile reached the journey goal

### Outtime Columns (Exit Timestamps)
- `outtime_journey`: When profile exited the journey
- `outtime_stage_{stage_index}`: When profile exited a specific stage
- `outtime_stage_{stage_index}_{step_uuid}`: When profile exited a specific step

### Special Column Types
For complex steps like decision points and A/B tests:
- `intime_stage_{stage_index}_{step_uuid}_{segment_id}`: Decision point branch entry
- `intime_stage_{stage_index}_{step_uuid}_variant_{variant_id}`: A/B test variant entry

## Creating Profile Timelines

To create a comprehensive timeline for a customer profile, you'll need to query multiple tables and columns. Here's the approach:

### 1. Basic Profile Timeline Query

```sql
SELECT
    cdp_customer_id,
    intime_journey,
    outtime_journey,
    intime_goal,
    intime_stage_0,
    outtime_stage_0,
    intime_stage_1,
    outtime_stage_1,
    -- Add more stage columns based on journey structure
    intime_stage_0_milestone,
    intime_stage_0_exit_0
FROM journey_{journey_id}
WHERE cdp_customer_id = '{target_customer_id}'
```

### 2. Complete Journey Analysis Query

```sql
-- Get journey structure first
SELECT
    j.id as journey_id,
    j.name as journey_name,
    js.id as stage_id,
    js.name as stage_name,
    js.order_index,
    js.steps,
    js.milestone,
    js.exit_criterias
FROM journeys j
JOIN journey_stages js ON j.id = js.journey_id
WHERE j.id = {journey_id}
ORDER BY js.order_index;

-- Then get profile timeline
SELECT
    cdp_customer_id,
    -- Journey level
    intime_journey as journey_entry_time,
    outtime_journey as journey_exit_time,
    intime_goal as goal_reached_time,

    -- Stage level (expand based on actual stages)
    intime_stage_0 as stage_0_entry,
    outtime_stage_0 as stage_0_exit,
    intime_stage_0_milestone as stage_0_milestone,

    -- Convert Unix timestamps to readable format
    FROM_UNIXTIME(intime_journey) as journey_entry_readable,
    FROM_UNIXTIME(outtime_journey) as journey_exit_readable
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}';
```

### 3. Historical Movement Query

```sql
-- Check jump history
SELECT
    cdp_customer_id,
    source_journey_id,
    target_journey_id,
    target_journey_stage_id,
    reason
FROM journey_{journey_id}_standby
WHERE cdp_customer_id = '{customer_id}';

-- Check reentry history
SELECT *
FROM journey_{journey_id}_reentry_history
WHERE cdp_customer_id = '{customer_id}';

-- Check jump history
SELECT *
FROM journey_{journey_id}_jump_history
WHERE cdp_customer_id = '{customer_id}';
```

## Understanding Timestamps

All timestamps are stored as Unix timestamps (seconds since epoch). Key points:

- **NULL values**: Indicate the profile never reached that state
- **Non-null intime + NULL outtime**: Profile is currently in that state
- **Non-null both**: Profile entered and exited that state
- **Session time**: All timestamps for a single execution use the same session time

## Journey States and Profile Flow

### Journey Entry Process
1. Profile meets entry criteria for first stage
2. `intime_journey` and `intime_stage_0` are set
3. Profile progresses through steps within the stage
4. Each step entry/exit is tracked with specific timestamps

### Stage Progression
1. Profile completes current stage (outtime_stage_X set)
2. If milestone exists, intime_stage_X_milestone is set
3. Profile enters next stage (intime_stage_Y set)
4. Process repeats

### Journey Exit Scenarios
1. **Goal Achievement**: `intime_goal` set, journey completes
2. **Exit Criteria**: `intime_stage_X_exit_Y` set, profile exits
3. **Jump to Another Journey**: Record created in standby table
4. **Natural Completion**: Profile reaches final stage

## Querying Examples

### Example 1: Customer Journey Timeline

```sql
-- For journey ID 12345 and customer 'CUST001'
SELECT
    cdp_customer_id,
    FROM_UNIXTIME(intime_journey) as journey_started,
    FROM_UNIXTIME(intime_stage_0) as entered_welcome_stage,
    FROM_UNIXTIME(intime_stage_0_milestone) as completed_welcome,
    FROM_UNIXTIME(outtime_stage_0) as exited_welcome_stage,
    FROM_UNIXTIME(intime_stage_1) as entered_engagement_stage,
    FROM_UNIXTIME(intime_goal) as reached_goal,
    FROM_UNIXTIME(outtime_journey) as journey_completed,

    -- Calculate stage duration
    (outtime_stage_0 - intime_stage_0) as welcome_stage_duration_seconds,

    -- Check current status
    CASE
        WHEN intime_goal IS NOT NULL THEN 'Goal Achieved'
        WHEN outtime_journey IS NOT NULL THEN 'Journey Completed'
        WHEN intime_stage_1 IS NOT NULL AND outtime_stage_1 IS NULL THEN 'In Engagement Stage'
        WHEN intime_stage_0 IS NOT NULL AND outtime_stage_0 IS NULL THEN 'In Welcome Stage'
        ELSE 'Unknown Status'
    END as current_status

FROM journey_12345
WHERE cdp_customer_id = 'CUST001';
```

### Example 2: Stage Performance Analysis

```sql
-- Analyze how customers progress through stages
SELECT
    'Stage 0 -> Stage 1' as transition,
    COUNT(*) as profiles_count,
    AVG(intime_stage_1 - outtime_stage_0) as avg_transition_time_seconds,

    COUNT(CASE WHEN intime_stage_1 IS NOT NULL THEN 1 END) as completed_transition,
    COUNT(CASE WHEN intime_stage_0 IS NOT NULL THEN 1 END) as entered_stage_0,

    ROUND(
        COUNT(CASE WHEN intime_stage_1 IS NOT NULL THEN 1 END) * 100.0 /
        COUNT(CASE WHEN intime_stage_0 IS NOT NULL THEN 1 END), 2
    ) as conversion_rate_percent

FROM journey_12345
WHERE intime_stage_0 IS NOT NULL;
```

### Example 3: Step-Level Analysis

```sql
-- Assuming step UUID 'abc123' in stage 0
SELECT
    cdp_customer_id,
    FROM_UNIXTIME(intime_stage_0) as stage_entry,
    FROM_UNIXTIME(intime_stage_0_abc123) as step_entry,
    FROM_UNIXTIME(outtime_stage_0_abc123) as step_exit,

    -- Time spent in step
    (outtime_stage_0_abc123 - intime_stage_0_abc123) as step_duration_seconds,

    -- Time from stage entry to step entry
    (intime_stage_0_abc123 - intime_stage_0) as time_to_reach_step_seconds

FROM journey_12345
WHERE intime_stage_0_abc123 IS NOT NULL
  AND cdp_customer_id = 'CUST001';
```

## Working with Journey Metadata

### Getting Journey Structure
```sql
-- First, understand the journey structure
SELECT
    j.id,
    j.name,
    j.description,
    j.state,
    j.goal,
    j.allow_reentry,
    js.order_index,
    js.name as stage_name,
    js.steps,
    js.entry_criteria,
    js.milestone,
    js.exit_criterias
FROM journeys j
JOIN journey_stages js ON j.id = js.journey_id
WHERE j.id = {journey_id}
ORDER BY js.order_index;
```

### Understanding Journey Statistics
```sql
-- Get aggregated journey metrics
SELECT
    journey_id,
    size as current_profiles_in_journey,
    goal_size as profiles_reached_goal,
    entry_influx as profiles_entered_this_period,
    goal_influx as profiles_reached_goal_this_period,
    exit_influx as profiles_exited_this_period,
    jump_influx as profiles_jumped_this_period
FROM journey_statistics
WHERE journey_id = {journey_id}
ORDER BY created_at DESC
LIMIT 1;
```

### Stage-Level Statistics
```sql
-- Get stage-specific metrics
SELECT
    jss.journey_stage_id,
    js.name as stage_name,
    js.order_index,
    jss.size as profiles_in_stage,
    jss.entry_influx,
    jss.exit_influx,
    jss.jump_influx,
    jss.step_sizes,
    jss.step_influxes
FROM journey_stage_statistics jss
JOIN journey_stages js ON jss.journey_stage_id = js.id
WHERE jss.journey_id = {journey_id}
ORDER BY js.order_index;
```

## Advanced Scenarios

### Reentry Tracking
When `allow_reentry` is enabled, profiles can re-enter journeys:

```sql
-- Track reentry patterns
SELECT
    cdp_customer_id,
    COUNT(*) as reentry_count,
    MIN(FROM_UNIXTIME(intime_journey)) as first_entry,
    MAX(FROM_UNIXTIME(intime_journey)) as latest_entry
FROM journey_{journey_id}_reentry_history
GROUP BY cdp_customer_id
HAVING COUNT(*) > 1;
```

### Cross-Journey Movement
```sql
-- Track profiles jumping between journeys
SELECT
    s.cdp_customer_id,
    s.source_journey_id,
    s.target_journey_id,
    s.target_journey_stage_id,
    s.reason,
    j1.name as source_journey_name,
    j2.name as target_journey_name,
    js.name as target_stage_name
FROM journey_{journey_id}_standby s
JOIN journeys j1 ON s.source_journey_id = j1.id
JOIN journeys j2 ON s.target_journey_id = j2.id
JOIN journey_stages js ON s.target_journey_stage_id = js.id
WHERE s.cdp_customer_id = '{customer_id}';
```

### Journey Active Periods
```sql
-- Understand when journey was active
SELECT
    journey_id,
    begin as start_date,
    end as end_date,
    closed,
    DATEDIFF(end, begin) as active_days
FROM journey_active_windows
WHERE journey_id = {journey_id}
ORDER BY begin;
```

## Best Practices

1. **Always check journey structure first** before querying profile data
2. **Use Unix timestamp conversion** for readable dates: `FROM_UNIXTIME(timestamp)`
3. **Handle NULL values appropriately** - they indicate states never reached
4. **Consider journey versions** - sibling journeys may affect profile flow
5. **Check reentry settings** - affects how profiles can re-enter journeys
6. **Monitor jump history** for cross-journey movements
7. **Use statistics tables** for aggregated insights before detailed queries

## Column Discovery Helper

To dynamically discover available columns for a journey:

```sql
-- Get column information for a journey table
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'journey_{journey_id}'
  AND COLUMN_NAME LIKE '%intime%'
   OR COLUMN_NAME LIKE '%outtime%'
ORDER BY COLUMN_NAME;
```

## Creating Complete Profile Timelines

Here's a comprehensive approach to create a complete timeline:

### Step 1: Get Journey Metadata
```sql
SELECT j.*, js.order_index, js.name as stage_name, js.steps
FROM journeys j
JOIN journey_stages js ON j.id = js.journey_id
WHERE j.id = {journey_id}
ORDER BY js.order_index;
```

### Step 2: Build Dynamic Column Query
Based on the journey structure, construct a query with all relevant columns:
- `intime_journey`, `outtime_journey`
- `intime_stage_{i}`, `outtime_stage_{i}` for each stage
- `intime_stage_{i}_milestone` if milestone exists
- `intime_stage_{i}_exit_{j}` for each exit criteria
- Step-specific columns based on step UUIDs
- `intime_goal` if goal exists

### Step 3: Execute Timeline Query
```sql
SELECT
    cdp_customer_id,
    -- Add all discovered timestamp columns
    -- Convert to readable format where needed
FROM journey_{journey_id}
WHERE cdp_customer_id = '{customer_id}';
```

### Step 4: Check Supporting Tables
Query jump_history, reentry_history, and standby tables for complete picture.

This comprehensive system allows precise tracking of customer journeys with full temporal granularity, enabling detailed analysis of customer behavior patterns and journey optimization opportunities.