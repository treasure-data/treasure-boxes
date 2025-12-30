# CJO Step Types Implementation Guide

This guide documents the implementation of all CJO (Customer Journey Orchestration) step types in the Profile Viewer, including their display formatting, profile tracking, and special handling requirements.

## Table of Contents
- [Overview](#overview)
- [Step Type Implementations](#step-type-implementations)
- [Display Formatting Patterns](#display-formatting-patterns)
- [Profile Tracking](#profile-tracking)
- [Technical Implementation](#technical-implementation)

## Overview

The CJO Profile Viewer supports all 7 core step types defined in the Treasure Data CDP system:

1. **Wait Steps** - Time-based delays and condition waits
2. **Activation Steps** - Data export and syndication actions
3. **Decision Points** - Segment-based branching logic
4. **AB Test Steps** - Split testing with variant allocation
5. **Jump Steps** - Stage and journey transitions
6. **Merge Steps** - Path consolidation and convergence
7. **End Steps** - Journey termination points

## Step Type Implementations

### 1. Wait Steps

**Types Supported:**
- **Duration Waits**: Fixed time delays (e.g., "Wait 7 days")
- **Condition Waits**: Wait for customer behavior with timeout
- **Date Waits**: Wait until specific date/time
- **Days of Week Waits**: Wait for specific days

**Step Type Variants:**
- **`WaitStep`**: Standard wait steps (duration, date, days of week)
- **`WaitCondition_Path`**: Conditional wait paths with timeout handling

**Display Format:**
```
Wait 7 days (45 profiles)
Wait for purchase (timeout: 14 days) (23 profiles)
Wait until 2024-01-15 (12 profiles)
Wait for Monday, Wednesday (8 profiles)
Wait Condition: event_name - path_name (15 profiles)  # WaitCondition_Path
```

**Profile Tracking:**
- **Entry Column**: `intime_stage_{N}_{step_uuid}`
- **Exit Column**: `outtime_stage_{N}_{step_uuid}`
- **Active Profiles**: `intime IS NOT NULL AND outtime IS NULL`

### 2. Activation Steps

**Purpose:** Data syndication and export to external systems

**Display Format:**
```
Activation: Email Campaign Send (67 profiles)
Activation: CRM Data Export (34 profiles)
```

**Profile Tracking:**
- **Entry Column**: `intime_stage_{N}_{step_uuid}`
- **Execution Logic**: Typically immediate (no wait state)
- **Success Tracking**: Via outtime columns

### 3. Decision Points

**Purpose:** Segment-based routing with multiple branches

**Display Format:**
```
Decision: country routing (145 profiles)
--- Branch: country is japan (67 profiles)
--- Branch: country is canada (23 profiles)
--- Branch: Default/Excluded path (55 profiles)
```

**Profile Tracking:**
- **Main Step**: `intime_stage_{N}_{step_uuid}`
- **Branch Columns**: `intime_stage_{N}_{step_uuid}_{segment_id}`
- **Branch Logic**: Each profile enters exactly one branch

**Technical Implementation:**
- Branch detection via `branches[]` array in step definition
- Segment ID extraction from API response
- Hierarchical display with `---` indentation

### 4. AB Test Steps

**Purpose:** Split testing with percentage-based variant allocation

**Display Format:**
```
AB Test: email variants (89 profiles)
--- Variant A (5%): 4 profiles
--- Variant B (5%): 5 profiles
--- Control (90%): 80 profiles
```

**Profile Tracking:**
- **Main Step**: `intime_stage_{N}_{step_uuid}`
- **Variant Columns**: `intime_stage_{N}_{step_uuid}_variant_{variant_id}`
- **Assignment Logic**: Hash-based consistent allocation

**Technical Implementation:**
- Variant detection via `variants[]` array
- Percentage display from variant configuration
- Profile distribution across variants

### 5. Jump Steps

**Purpose:** Transitions between stages or journeys

**Display Format:**
```
Jump to Stage 2 (12 profiles)
Jump to Journey 'Onboarding Flow' (8 profiles)
```

**Profile Tracking:**
- **Exit Tracking**: Via `journey_{id}_standby` table
- **Transition Logic**: Profiles move to target destination
- **History Preservation**: Via `journey_{id}_jump_history` table

### 6. Merge Steps

**Purpose:** Path consolidation where multiple branches converge

**Special Implementation:** Merge steps require hierarchical display to avoid step duplication.

#### 6.1 Merge Step Hierarchy Format

**Before Merge (Branch Paths):**
```
Decision: country is japan (2 profiles)
--- Wait 3 days (0 profiles)
--- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe) (3 profiles)

Decision: Excluded Profiles (1 profiles)
--- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe) (3 profiles)
```

**After Merge (Consolidated Path):**
```
Merge: (5eca44ab-201f-40a7-98aa-b312449df0fe) - grouping header (3 profiles)
--- Wait 1 day (0 profiles)
--- End Step (0 profiles)
```

#### 6.2 Merge Technical Implementation

**Enhanced FlowchartStep Class:**
```python
class FlowchartStep:
    is_merge_endpoint: bool = False  # Merge at end of branch
    is_merge_header: bool = False    # Merge as grouping header
```

**Path Building Logic:**
- `_build_paths_with_merges()`: Handles stages with merge points
- `_trace_paths_to_merge()`: Traces branch paths to convergence
- `_build_pre_merge_paths()`: Builds paths leading to merges
- `_build_post_merge_paths()`: Handles paths after merge points

**Display Integration:**
- Automatic merge point detection
- Conditional hierarchical formatting
- Breadcrumb preservation for post-merge steps
- Profile count aggregation at merge points

**Specialized Formatter Module:**
- **`merge_display_formatter.py`**: Dedicated module for merge hierarchy formatting
- **`format_merge_hierarchy()`**: Creates the exact hierarchical display format
- **Branch Path Separation**: Distinguishes pre-merge and post-merge paths
- **Smart Detection**: Only activates when merge points are present in journey

#### 6.3 Merge Step Profile Tracking

**Branch Entry Tracking:**
```sql
-- Profiles entering merge from different branches
SELECT COUNT(*) FROM journey_{id}
WHERE intime_stage_{N}_{merge_uuid} IS NOT NULL
```

**Post-Merge Tracking:**
```sql
-- Profiles continuing after merge
SELECT COUNT(*) FROM journey_{id}
WHERE intime_stage_{N}_{merge_uuid} IS NOT NULL
  AND outtime_stage_{N}_{merge_uuid} IS NOT NULL
```

### 7. End Steps

**Purpose:** Journey termination points

**Display Format:**
```
End Step (23 profiles)
Goal Achievement (45 profiles)
```

**Profile Tracking:**
- **Entry Column**: `intime_stage_{N}_{step_uuid}`
- **Journey Completion**: Via `intime_goal` or `outtime_journey`
- **Final State**: No exit from end steps

## Display Formatting Patterns

### Indentation Rules

**Standard Steps:**
```
Step Name (profile count)
```

**Grouped Steps (Decision/AB Test branches):**
```
Decision: name (total count)
--- Branch: name (branch count)
--- Branch: name (branch count)
```

**Merge Hierarchies:**
```
Branch Path → Merge Endpoint:
--- Merge (uuid) (count)

Merge Grouping Header:
Merge: (uuid) - grouping header (count)
--- Post-merge step (count)
```

### Profile Count Display

**Active Profiles Only:**
- Profiles currently in the step (not completed/exited)
- Query pattern: `intime IS NOT NULL AND outtime IS NULL`

**Aggregation Rules:**
- **Decision Points**: Sum of all branch profiles
- **AB Tests**: Sum of all variant profiles
- **Merge Points**: Aggregated count from all converging paths

### UUID Handling

**Display Format:**
- Short UUID format: First 8 characters (e.g., `5eca44ab`)
- Full UUID in tooltips and details
- Consistent shortening across all step types

## Profile Tracking

### Column Naming Patterns

**Standard Steps:**
```
intime_stage_{stage_index}_{step_uuid}
outtime_stage_{stage_index}_{step_uuid}
```

**Decision Point Branches:**
```
intime_stage_{stage_index}_{step_uuid}_{segment_id}
outtime_stage_{stage_index}_{step_uuid}_{segment_id}
```

**AB Test Variants:**
```
intime_stage_{stage_index}_{step_uuid}_variant_{variant_id}
outtime_stage_{stage_index}_{step_uuid}_variant_{variant_id}
```

### Profile State Logic

**Active in Step:**
```sql
WHERE intime_stage_{N}_{step_uuid} IS NOT NULL
  AND outtime_stage_{N}_{step_uuid} IS NULL
  AND intime_journey IS NOT NULL
  AND outtime_journey IS NULL
  AND intime_goal IS NULL
```

**Actual Implementation Logic:**
The `CJOFlowchartGenerator` class implements detailed profile counting:

```python
def _get_step_profile_count(self, step_id: str, stage_idx: int, step_type: str) -> int:
    """Get profile count for a specific step with type-specific logic."""
    if self.profile_data.empty:
        return 0

    try:
        # Convert step ID to column name
        step_uuid = step_id.replace('-', '_')
        step_column = f"intime_stage_{stage_idx}_{step_uuid}"
        outtime_column = f"outtime_stage_{stage_idx}_{step_uuid}"

        if step_column not in self.profile_data.columns:
            return 0

        # Base condition: profiles that entered this step
        condition = self.profile_data[step_column].notna()

        # For non-endpoint steps, only count active profiles
        if outtime_column in self.profile_data.columns:
            # Still in step (not exited)
            condition = condition & self.profile_data[outtime_column].isna()

        # Only count profiles still active in journey
        condition = condition & self.profile_data['intime_journey'].notna()
        condition = condition & self.profile_data['outtime_journey'].isna()
        condition = condition & self.profile_data['intime_goal'].isna()

        return len(self.profile_data[condition])
    except Exception:
        return 0
```

**Completed Step:**
```sql
WHERE intime_stage_{N}_{step_uuid} IS NOT NULL
  AND outtime_stage_{N}_{step_uuid} IS NOT NULL
```

## Technical Implementation

### Core Classes

**FlowchartStep:**
```python
@dataclass
class FlowchartStep:
    step_id: str
    step_type: str
    name: str
    stage_index: int
    profile_count: int = 0
    is_merge_endpoint: bool = False
    is_merge_header: bool = False
```

**Step Type Detection:**
```python
def get_step_type(step_data: dict) -> str:
    step_type = step_data.get('type', 'Unknown')

    # Handle complex step variants
    if step_type == 'DecisionPoint':
        return 'DecisionPoint_Branch' if has_branches else 'DecisionPoint'
    elif step_type == 'ABTest':
        return 'ABTest_Variant' if has_variants else 'ABTest'
    elif step_type == 'WaitStep':
        return 'WaitCondition_Path' if has_conditions else 'WaitStep'

    return step_type
```

**Column Mapper Integration:**
The `CJOColumnMapper` class handles complex step type detection and formatting:

```python
# In column_mapper.py - Decision Point branch detection
if step_data.get('type') == 'DecisionPoint':
    branches = step_data.get('branches', [])
    for branch in branches:
        segment_id = branch.get('segmentId')
        # Creates DecisionPoint_Branch entries

# AB Test variant detection
if step_data.get('type') == 'ABTest':
    variants = step_data.get('variants', [])
    for variant in variants:
        variant_id = variant.get('id')
        # Creates ABTest_Variant entries
```

### Display Integration

**Step Formatting Pipeline:**
1. **Step Detection**: Identify step type from API response
2. **Profile Counting**: Query live journey table data
3. **Display Formatting**: Apply type-specific formatting rules
4. **Hierarchy Building**: Handle indentation and grouping
5. **UI Rendering**: Generate final display strings

**Special Handling:**
- **Merge Detection**: Automatic identification of merge points in stages
- **Conditional Formatting**: Hierarchical display only when merges present
- **Breadcrumb Preservation**: Maintain path context through merges
- **Profile Aggregation**: Correct counting across merged paths

### Error Handling

**Missing Columns:**
- Graceful handling of non-existent step columns
- Default to 0 profiles for missing data
- Error logging for debugging

**Invalid Step Types:**
- Fallback to generic step formatting
- Warning messages for unknown types
- Defensive programming throughout

---

This implementation provides comprehensive support for all CJO step types while maintaining clean, hierarchical display formatting and accurate profile tracking across complex journey structures.