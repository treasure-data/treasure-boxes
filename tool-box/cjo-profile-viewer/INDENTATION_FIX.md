# Post-Merge Step Indentation Fix - Complete

## Issue Identified

Based on the screenshot at `~/Desktop/merge.png`, the dropdown was showing:

```
❌ INCORRECT (Before Fix):
Merge (5eca44ab) (0 profiles)
Wait 1 day (0 profiles)          ← Not indented (same level as merge)
End Step (0 profiles)            ← Not indented (same level as merge)
```

## Root Cause

The issue was caused by the **step reorganization logic** in `streamlit_app.py` that runs after our merge formatter. This reorganization was designed for the old system and was interfering with our carefully crafted merge hierarchy indentation.

## Fix Applied

**Updated streamlit_app.py line 1364:**

```python
# Before:
if all_steps:

# After:
if all_steps and not has_merge_points:
```

**Effect:** This bypasses the reorganization logic when merge hierarchies are present, preserving our proper indentation.

## Result After Fix

```
✅ CORRECT (After Fix):
Merge (5eca44ab) (3 profiles)
--- Wait 1 day (0 profiles)      ← Properly indented with ---
--- End Step (0 profiles)        ← Properly indented with ---
```

## Technical Details

### **The Problem**
The reorganization logic in `streamlit_app.py` was:
1. Processing our already-formatted merge hierarchy steps
2. Removing the indentation we carefully applied
3. Flattening the hierarchy structure

### **The Solution**
By adding `and not has_merge_points` condition:
1. Merge hierarchies bypass the reorganization entirely
2. Our formatter's indentation is preserved
3. Post-merge steps maintain their `---` prefix

### **Code Change**
```python
# Skip reorganization for merge hierarchies as they're already properly formatted
if all_steps and not has_merge_points:
    reorganized_steps = []
    decision_branch_groups = {}
    # ... reorganization logic only runs for non-merge hierarchies
```

## Verification

### ✅ **Test Results Confirm Fix**

**Formatter Test:**
```
6. Stage 1: Merge (5eca44ab) (3 profiles)
7. Stage 1: --- Wait 1 day (0 profiles)      ← ✅ Indented
8. Stage 1: --- End Step (0 profiles)        ← ✅ Indented
```

**Dropdown Test:**
```
7. POST-MERGE STEP - Properly indented with ---   ✅
8. POST-MERGE STEP - Properly indented with ---   ✅
```

## Expected Dropdown Behavior

The dropdown should now display:

```
📋 Correct Hierarchy:
Decision: country is japan (X profiles)
├── --- Wait 3 day (X profiles)
└── --- Merge (5eca44ab) (X profiles)

Decision: Excluded Profiles (X profiles)
└── --- Merge (5eca44ab) (X profiles)

Merge (5eca44ab) (X profiles)                     ← Grouping header
├── --- Wait 1 day (X profiles)                   ← ✅ Properly indented
└── --- End Step (X profiles)                     ← ✅ Properly indented
```

## Benefits of the Fix

1. **Preserves Intended Formatting**: Our merge hierarchy formatter's output is no longer modified
2. **Consistent Behavior**: Merge steps now behave exactly like Decision/AB Test grouping headers
3. **Clean Hierarchy**: Clear visual indication that post-merge steps belong under the merge
4. **No Side Effects**: Non-merge journeys still use the reorganization logic as before

## Summary

The indentation issue visible in the screenshot has been resolved by preventing the step reorganization logic from interfering with merge hierarchies. Post-merge steps now display with proper `---` indentation under their merge grouping headers, creating the correct hierarchical structure in the dropdown.

**The fix ensures that steps coming from a merge are properly indented one level deeper to show they come from the merge grouping header.**