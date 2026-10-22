---
name: journey-table-readable-query
description: Use when a user wants a CJO `journey_<id>` table made readable — map step UUID columns to step names, format epoch-second timestamps, and generate a wide Trino SELECT with formatted timestamps. Covers normal steps, decision branches, A/B variants, and wait/merge steps.
---

# Readable Journey Table Query

Generate a read-only Trino `SELECT` over the `cdp_audience_<audience_id>.journey_<journey_id>` table. Alias each step column with its journey-definition name, and format epoch-second timestamps. Generate SQL by default; execute only when asked.

**Example Request:** “Make my journey table readable.”

## Prerequisites

1. Get the **Audience Name/ID** and **Journey Name/ID** from the user. 
2. Invoke `tdx-skills:tdx-basic` and use the profile matching the customer's region. Never ask for API keys; if auth fails, ask the user to re-authenticate the profile.
3. Run all SQL through `tdx`. Keep SQL and results inline.

## Boundaries

- This skill maps and formats the journey table; it does not reconstruct past snapshots, jumps, re-entry, or journey history.
- Do not claim that this unsupported, changeable system table is a supported customer analytics interface.
- If the journey definition, profile, target table, column type, or mapping is ambiguous, ask for the missing information rather than guessing.

## Discovery

- `tdx ps list --json`: get audience name if provided with audience id
- `tdx journey list --json`: get journey name if provided with journey id 
- `tdx journey columns "<journey_name>"`: physical columns and journey/step details
- `tdx describe cdp_audience_<audience_id>.journey_<journey_id>`: verify the table and column types.

If these don't give enough information, ask for the output or a user-authorized journey definition. If anything is ambiguous, ask rather than guess.

## Column Alias Rules

- Append each column with `Enter|Exit` depending on the `direction`. `direction=in` is Enter, `direction=out` is Exit
- Use a one-based stage number instead of the stage index. <stage_number> = <stage_index> + 1
- `cdp_customer_id` and `time` columns remain the same, no alias necessary.
- Select each verified physical column explicitly, wrap confirmed epoch-second step timestamps with `TD_TIME_FORMAT(<column>, 'yyyy-MM-dd HH:mm:ss z', 'utc')`, and alias them with the verified stage/step/branch/variant labels. Preserve other columns by name. Do not invent example IDs or names.

# Non-step Columns (Journey, Stage, Milestone, Goal, ..)

- These columns have `stepType=null` and can be described with the column name itself or by `category` and `direction`.
- If there is a stage available, prefix alias with  `[Stage <stage_number>]

Examples:

1. Journey - Enter
```
    {
        "column": "intime_journey",
        "direction": "in",
        "stageIndex": null,
        "stageName": null,
        "category": "journey",
        "stepType": null,
        "stepName": null,
        "stepId": null,
        "detail": null
    },
```

2. [Stage 1] Enter
```
    {
        "column": "intime_stage_0",
        "direction": "in",
        "stageIndex": 0,
        "stageName": "First",
        "category": "stage",
        "stepType": null,
        "stepName": null,
        "stepId": null,
        "detail": "userid is not null"
    },
```

3. [Stage 1] Milestone - Enter
```
    {
        "column": "intime_stage_0_milestone",
        "direction": "in",
        "stageIndex": 0,
        "stageName": "First",
        "category": "milestone",
        "stepType": null,
        "stepName": null,
        "stepId": null,
        "detail": "action=gotosecond"
    },
```

# General Step Columns

The general format of a step column is: `intime_stage_<stage_index>_<step_id>`
Format aliases as: `[Stage <stage_number>] <stepType>: <stepName> - [Enter|Exit]

Examples:

1. [Stage 1] Activation: td_japan_activate - Enter

```
{
    "column": "intime_stage_0_060866cc_d1c8_4900_8315_6be58a164429",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "step",
    "stepType": "Activation",
    "stepName": "td_japan_activate",
    "stepId": "060866cc-d1c8-4900-8315-6be58a164429",
    "detail": null
},
```

2. [Stage 2] End - Exit
```
{
    "column": "outtime_stage_1_cb9778c6_4d4c_48f0_bf60_52556e3b0f99",
    "direction": "out",
    "stageIndex": 1,
    "stageName": "Second",
    "category": "step",
    "stepType": "End",
    "stepName": null,
    "stepId": "cb9778c6-4d4c-48f0-bf60-52556e3b0f99",
    "detail": null
},
```

3. [Stage 1] Milestone - Enter
```
{
    "column": "intime_stage_0_milestone",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "milestone",
    "stepType": null,
    "stepName": null,
    "stepId": null,
    "detail": "action=gotosecond"
},
```

# Wait and Merge

Wait and Merge steps don't have step names. Use "1st Wait Step", "2nd Wait Step", etc. Restart from 1 for every stage.

Examples:

1. [Stage 1] - First Wait - Enter
```
  {
    "column": "intime_stage_0_b22aa9a7_50e1_4b28_9b7b_e0c3e78231b0",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "step",
    "stepType": "WaitStep",
    "stepName": null,
    "stepId": "b22aa9a7-50e1-4b28-9b7b-e0c3e78231b0",
    "detail": null
  },
```

2. [Stage 2] 1st Merge - Exit
```
{
    "column": "outtime_stage_1_4ad850ca_61f2_4dc4_aacf_5cdc6e79add9",
    "direction": "out",
    "stageIndex": 1,
    "stageName": "Second",
    "category": "step",
    "stepType": "Merge",
    "stepName": null,
    "stepId": "4ad850ca-61f2-4dc4-aacf-5cdc6e79add9",
    "detail": null
},
```

# Decision Point

There are two formats for decision points depending on the `category`:

1. `category=step` (Decision Point Root): `intime_stage_<stage_index>_<step_id>`
2. `category=branch` (Decision Point Branch): `intime_stage_<stage_index>_<step_id>_<branch_segmentId>`

Alias rules:
- Use "1st Decision Point", "2nd Decision Point", etc to differentiate between Decision Point steps. Start from 1 on each stage.

- Branches:
  - Use `detail` in the alias if not null
  - If the column name has a `<branch_segmentId>` but `detail` is null, use "Excluded Path".

Examples:

1. [Stage 1] 1st Decision Point - Enter
```
{
    "column": "intime_stage_0_4314162e_8c2c_4c43_b124_dcd3de3a39a6",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "step",
    "stepType": "DecisionPoint",
    "stepName": null,
    "stepId": "4314162e-8c2c-4c43-b124-dcd3de3a39a6",
    "detail": null
},
```

2. [Stage 1] 1st Decision Point: country is japan - Enter
```
{
    "column": "intime_stage_0_4314162e_8c2c_4c43_b124_dcd3de3a39a6_2696623",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "branch",
    "stepType": "DecisionPoint",
    "stepName": null,
    "stepId": "4314162e-8c2c-4c43-b124-dcd3de3a39a6",
    "detail": "country is japan"
},
```

3. [Stage 1] 1st Decision Point: Excluded Path - Enter
```
{
    "column": "intime_stage_0_4314162e_8c2c_4c43_b124_dcd3de3a39a6_2696630",
    "direction": "in",
    "stageIndex": 0,
    "stageName": "First",
    "category": "branch",
    "stepType": "DecisionPoint",
    "stepName": null,
    "stepId": "4314162e-8c2c-4c43-b124-dcd3de3a39a6",
    "detail": null
},
```

# AB Tests

There are two formats for AB Tests depending on the `category`:

1. `category=step` (AB Test Root): `intime_stage_<stage_index>_<step_id>`
2. `category=variant` (AB Test Variant): `intime_stage_<stage_index>_<step_id>_variant_<variant_id>`

Examples:

1. [Stage 2] ab test  - Exit
```
{
    "column": "intime_stage_1_17aa131f_112c_4a37_915f_708082ff8350",
    "direction": "in",
    "stageIndex": 1,
    "stageName": "Second",
    "category": "step",
    "stepType": "ABTest",
    "stepName": "ab test",
    "stepId": "17aa131f-112c-4a37-915f-708082ff8350",
    "detail": null
},
```

2. [Stage 2] ab test: Control - Enter
```
{
    "column": "intime_stage_1_17aa131f_112c_4a37_915f_708082ff8350_variant_fd2a65a3_1ba2_4d19_87a0_ad91cba6c6b6",
    "direction": "in",
    "stageIndex": 1,
    "stageName": "Second",
    "category": "variant",
    "stepType": "ABTest",
    "stepName": "ab test",
    "stepId": "17aa131f-112c-4a37-915f-708082ff8350",
    "detail": "Control"
},
```

## Create the query with column aliases for journey_xxxx table

- Write a new query to get human-readable column name using the journey details from `tdx journey columns` response. 
- Use `TD_TIME_FORMAT` function to convert the timestamp to a readable format.
- Add comments to explain the query and the mapping rules.

Example of converted column name:

```
select 
  cdp_customer_id,
  TD_TIME_FORMAT(intime_journey, 'yyyy-MM-dd HH:mm:ss z', 'utc'),
  TD_TIME_FORMAT(outtime_journey, 'yyyy-MM-dd HH:mm:ss z', 'utc'),
  TD_TIME_FORMAT(intime_stage_0_b22aa9a7_50e1_4b28_9b7b_e0c3e78231b0, 'yyyy-MM-dd HH:mm:ss z', 'utc') as "[Stage 1] First Wait"
  ...
  ...
  ...

from cdp_audience_xxx.journey_yyy
```