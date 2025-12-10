# Merge Steps Implementation Guide

## Overview

This document explains the implementation of Merge step handling in the CJO Profile Viewer to address the issue of duplicated steps after merge points in customer journey flows.

## Problem Addressed

Previously, when multiple paths converged at a merge point, all subsequent steps after the merge would be duplicated across different paths, making the journey visualization confusing and inefficient.

## Solution

The implementation now handles merge steps by:

1. **Detecting Merge Points**: Automatically identifies steps with type "Merge" in the journey configuration
2. **Separate Path Building**: Builds paths up to merge points separately, then shows merge steps distinctly
3. **Unified Post-Merge Path**: Steps after merge are shown only once, avoiding duplication
4. **Proper Profile Counting**: Merge steps correctly aggregate profile counts from all incoming paths

## Technical Implementation

### FlowchartGenerator Changes

- **New Step Type**: Added support for `Merge` step type
- **Enhanced Path Building**: `_build_paths_with_merges()` method handles stages containing merge steps
- **Merge Point Detection**: `_find_merge_points()` identifies all merge steps in a stage
- **Path Separation**: `_build_pre_merge_paths()` builds paths until merge points
- **Unified Continuation**: `_follow_path_until_merge()` stops path building at merge points

### Key Methods Added

```python
def _find_merge_points(steps: dict) -> set
def _build_paths_with_merges(steps: dict, root_step_id: str, stage_idx: int, merge_points: set) -> List[List[FlowchartStep]]
def _build_pre_merge_paths(steps: dict, root_step_id: str, stage_idx: int, merge_points: set) -> List[List[FlowchartStep]]
def _follow_path_until_merge(steps: dict, step_id: str, path: List[FlowchartStep], stage_idx: int, merge_points: set)
```

### Streamlit App Changes

- **Color Coding**: Added distinctive light blue color (`#d5e7f0`) for Merge steps
- **Saturated Colors**: Added darker blue (`#0099CC`) for merge steps in detailed views
- **Consistent Styling**: Merge steps are styled consistently across all visualization modes

## Usage

### Journey Configuration

To use merge steps in your journey, configure a step with type "Merge":

```json
{
  "merge-step-id": {
    "type": "Merge",
    "name": "Customer Merge Point",
    "next": "next-step-id"
  }
}
```

### Expected Behavior

1. **Before Merge**: All branching paths (Decision Points, AB Tests, Wait Conditions) are shown separately
2. **Merge Step**: Displayed as a single step that consolidates incoming paths
3. **After Merge**: Subsequent steps appear only once, avoiding duplication
4. **Profile Counts**: Merge step shows combined count from all incoming paths

## Example Journey Flow

```
Decision Point
├── Branch A → Activation A ─┐
└── Branch B → Activation B ─┤
                             ├── Merge Step → Final Activation → End
AB Test                      │
├── Variant 1 → Action 1 ────┤
└── Variant 2 → Action 2 ────┘
```

## Benefits

1. **Cleaner Visualization**: Eliminates duplicate steps after convergence points
2. **Better UX**: Users see each step only once after paths merge
3. **Accurate Metrics**: Profile counts properly aggregate at merge points
4. **Scalable**: Handles complex journeys with multiple merge points
5. **Backward Compatible**: Existing journeys without merge steps continue to work unchanged

## Testing

Run the test suite to verify merge step functionality:

```bash
python test_merge_steps.py
```

The test verifies:
- Merge step type recognition
- Proper path building with merges
- Step display name formatting
- Profile counting for merge steps
- No duplication of post-merge steps

## Visual Indicators

- **Color**: Light blue background (`#d5e7f0`) for merge steps
- **Icon**: Can be enhanced with a merge/confluence icon in future versions
- **Position**: Clearly separated from branching paths, positioned before unified continuation

This implementation provides a clean, efficient way to visualize customer journey convergence points while maintaining all existing functionality.