# Journey Table Readable Query

A Claude Code skill that transforms cryptic Treasure Data Customer Journey Orchestration (CJO) `journey_<id>` tables into human-readable queries by mapping UUID step columns to their actual step names and formatting epoch-second timestamps.

## What It Does

CJO journey tables store customer journey data with columns like:
- `intime_stage_0_b22aa9a7_50e1_4b28_9b7b_e0c3e78231b0` (cryptic UUID)
- `1698336000` (epoch seconds)

This skill generates a readable Trino `SELECT` query that aliases these to:
- `[Stage 1] First Wait - Enter` (descriptive name)
- `2023-10-26 12:00:00 UTC` (formatted timestamp)

## When to Use

Load this skill when you need to:
- Make a `journey_<id>` table readable for analysis
- Map step UUID columns to journey definition names
- Format epoch-second timestamps in journey tables
- Generate wide SELECT queries with all journey steps aliased

**Example requests:**
- "Make my journey table readable"
- "Generate a readable query for journey 12345"
- "Map the journey table columns to step names"

## Prerequisites

1. **Audience and Journey IDs**: Know the audience name/ID and journey name/ID you want to query
2. **tdx CLI**: Must have `tdx` installed and authenticated
3. **Profile access**: Need a tdx profile configured for the customer's region
4. **Table access**: Read access to `cdp_audience_<audience_id>.journey_<journey_id>`

## How It Works

1. **Discovery**: Uses `tdx journey columns` to get the journey structure and physical column mappings
2. **Verification**: Runs `tdx describe` to verify table schema and column types
3. **Mapping**: Applies column alias rules based on step type, stage, direction (enter/exit)
4. **Formatting**: Wraps timestamp columns with `TD_TIME_FORMAT()`
5. **Generation**: Creates a wide SELECT with all mapped columns

## Column Mapping Rules

### Direction Suffixes
- `direction=in` → **Enter**
- `direction=out` → **Exit**

### Stage Numbers
- Zero-based stage index converted to one-based: `stage_index + 1`
- Example: `stage_0` → `Stage 1`

### Step Types

#### Journey/Stage/Milestone (no stepType)
```
intime_journey          → Journey - Enter
intime_stage_0          → [Stage 1] Enter
intime_stage_0_milestone → [Stage 1] Milestone - Enter
```

#### General Steps
```
intime_stage_0_<uuid>   → [Stage 1] <stepType>: <stepName> - Enter
```

#### Wait and Merge Steps (no stepName)
```
intime_stage_0_<uuid>   → [Stage 1] 1st Wait - Enter
outtime_stage_1_<uuid>  → [Stage 2] 1st Merge - Exit
```
Counter restarts at 1 for each stage.

#### Decision Points
```
# Root
intime_stage_0_<uuid>              → [Stage 1] 1st Decision Point - Enter

# Branches (with detail)
intime_stage_0_<uuid>_<segment_id> → [Stage 1] 1st Decision Point: country is japan - Enter

# Branches (no detail)
intime_stage_0_<uuid>_<segment_id> → [Stage 1] 1st Decision Point: Excluded Path - Enter
```

#### A/B Tests
```
# Root
intime_stage_1_<uuid>                      → [Stage 2] ab test - Enter

# Variants
intime_stage_1_<uuid>_variant_<variant_id> → [Stage 2] ab test: Control - Enter
```

## Example Output

```sql
-- Journey Table Readable Query
-- Generated from journey definition: "Customer Onboarding Flow"
-- Maps physical UUID columns to human-readable step names

SELECT 
  cdp_customer_id,
  TD_TIME_FORMAT(time, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "Journey Time",
  TD_TIME_FORMAT(intime_journey, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "Journey - Enter",
  TD_TIME_FORMAT(outtime_journey, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "Journey - Exit",
  TD_TIME_FORMAT(intime_stage_0, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 1] Enter",
  TD_TIME_FORMAT(intime_stage_0_060866cc_d1c8_4900_8315_6be58a164429, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 1] Activation: td_japan_activate - Enter",
  TD_TIME_FORMAT(intime_stage_0_b22aa9a7_50e1_4b28_9b7b_e0c3e78231b0, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 1] 1st Wait - Enter",
  TD_TIME_FORMAT(intime_stage_0_4314162e_8c2c_4c43_b124_dcd3de3a39a6, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 1] 1st Decision Point - Enter",
  TD_TIME_FORMAT(intime_stage_0_4314162e_8c2c_4c43_b124_dcd3de3a39a6_2696623, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 1] 1st Decision Point: country is japan - Enter",
  TD_TIME_FORMAT(outtime_stage_1_cb9778c6_4d4c_48f0_bf60_52556e3b0f99, 'yyyy-MM-dd HH:mm:ss z', 'utc') AS "[Stage 2] End - Exit"
FROM cdp_audience_12345.journey_67890
LIMIT 100;
```

## Limitations

- **Read-only mapping**: Generates SELECT queries only; does not modify tables
- **Current state only**: Does not reconstruct journey history, snapshots, jumps, or re-entry
- **Unsupported tables**: Works only with `journey_<id>` system tables (unsupported, subject to change)
- **No execution by default**: Generates SQL; executes only when explicitly requested

## Usage

```bash
# In Claude Code CLI
/journey-table-readable-query

# Or natural language
"Make my journey 12345 table readable"
"Generate a readable query for audience abc123, journey xyz789"
```

The skill will:
1. Prompt for audience/journey IDs if not provided
2. Use `tdx` to fetch journey definition and table schema
3. Generate a commented SELECT query with all columns mapped
4. Display the query (execute only if requested)

## Related Skills

- **tdx-skills:journey**: Create and manage journey definitions
- **tdx-skills:tdx-basic**: Execute tdx commands and queries
- **tdx-skills:parent-segment**: Work with audience segments

## Technical Details

- **Query engine**: Trino SQL
- **Timestamp format**: `yyyy-MM-dd HH:mm:ss z` in UTC
- **Column discovery**: `tdx journey columns "<journey_name>"`
- **Schema verification**: `tdx describe cdp_audience_<id>.journey_<id>`

---

**Note**: Journey tables are internal system tables subject to change. This skill provides a convenience layer for analysis but should not be used as a customer-facing analytics interface.
