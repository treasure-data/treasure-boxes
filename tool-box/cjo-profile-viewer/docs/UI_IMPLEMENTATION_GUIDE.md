# UI Implementation Guide

This guide documents the user interface patterns, display formatting rules, and implementation details for the CJO Profile Viewer's visual components.

## Table of Contents
- [Overview](#overview)
- [Step Dropdown Formatting](#step-dropdown-formatting)
- [Flowchart Visualization](#flowchart-visualization)
- [Profile Display Components](#profile-display-components)
- [Indentation and Hierarchy](#indentation-and-hierarchy)
- [Interactive Elements](#interactive-elements)
- [Implementation Details](#implementation-details)

## Overview

The CJO Profile Viewer uses several key UI patterns to present complex journey data in an intuitive, hierarchical format. The interface consists of:

1. **Step Selection Dropdown** - Hierarchical list of all journey steps
2. **Interactive Flowchart** - Visual journey representation with clickable steps
3. **Profile Detail Panels** - Customer data display and analysis
4. **Breadcrumb Navigation** - Path context and journey progression

## Step Dropdown Formatting

### Display Hierarchy Rules

The step dropdown uses a consistent indentation pattern to show journey structure:

#### Standard Format
```
Stage Name → Step Name (profile count)
```

#### Grouped Elements (Decision Points, AB Tests)
```
Decision: segment name (total profiles)
--- Branch: condition name (branch profiles)
--- Branch: condition name (branch profiles)
```

#### Merge Hierarchies
```
// Branch paths leading to merge
Decision: country routing (45 profiles)
--- Wait 3 days (12 profiles)
--- Merge (5eca44ab) (15 profiles)

// Post-merge consolidated path
Merge: (5eca44ab) - grouping header (15 profiles)
--- Wait 1 day (8 profiles)
--- End Step (5 profiles)
```

### Indentation Implementation

**Indentation Levels:**
- **Level 0**: Main steps and grouping headers
- **Level 1**: Branch steps, variants, and post-merge steps (prefix: `---`)
- **Level 2**: Nested elements (prefix: `------`)

**Code Implementation:**
```python
def format_step_display(step_name: str, profile_count: int, indent_level: int = 0) -> str:
    """Format step display with proper indentation."""
    prefix = "--- " if indent_level > 0 else ""
    return f"{prefix}{step_name} ({profile_count} profiles)"
```

### Special Formatting Cases

#### Decision Point Branches
```python
# Main decision point (no profile count)
"Decision: country routing"

# Individual branches (with counts)
"--- Branch: country is japan (23 profiles)"
"--- Branch: country is canada (15 profiles)"
"--- Branch: Default/Excluded path (7 profiles)"
```

#### AB Test Variants
```python
# Main AB test (no profile count)
"AB Test: email variants"

# Individual variants (with percentages and counts)
"--- Variant A (5%): 2 profiles"
"--- Variant B (5%): 3 profiles"
"--- Control (90%): 40 profiles"
```

#### Merge Step Handling
```python
# Merge endpoint (end of branch path)
"--- Merge (5eca44ab) (15 profiles)"

# Merge grouping header (start of consolidated path)
"Merge: (5eca44ab) - grouping header (15 profiles)"
```

## Flowchart Visualization

### HTML/CSS Implementation

The flowchart uses custom HTML/CSS rendering instead of external libraries for better performance and control.

#### Stage Containers
```css
.stage-container {
    margin: 30px 0;
    padding: 20px;
    border: 1px solid #444444;
    border-radius: 8px;
    background-color: #2D2D2D;
}

.stage-header {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    text-align: center;
}
```

#### Step Boxes
```css
.step-box {
    background-color: #f8eac5;
    color: #000000;
    padding: 15px 20px;
    margin: 5px 0;
    border-radius: 8px;
    min-width: 180px;
    max-width: 220px;
    text-align: center;
    cursor: pointer;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.3s ease;
}

.step-box:hover {
    transform: scale(1.03);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-color: #85C1E9;
}
```

#### Step Type Colors
```python
step_type_colors = {
    'DecisionPoint': '#f8eac5',        # Decision Point - yellow/beige
    'DecisionPoint_Branch': '#f8eac5', # Decision Point Branch
    'ABTest': '#f8eac5',               # AB Test
    'ABTest_Variant': '#f8eac5',       # AB Test Variant
    'WaitStep': '#f8dcda',             # Wait Step - light pink/red
    'WaitCondition_Path': '#f8dcda',   # Wait Condition Path
    'Activation': '#d8f3ed',           # Activation - light green
    'Jump': '#e8eaff',                 # Jump - light blue/purple
    'End': '#e8eaff',                  # End Step - light blue/purple
    'Merge': '#f8eac5',                # Merge Step - yellow/beige
    'Unknown': '#f8eac5'               # Unknown - default
}
```

### Interactive Features

#### Click Handling
```javascript
function showProfileModal(stepDataKey) {
    const stepData = stepDataStore[stepDataKey];
    if (!stepData) {
        console.error('Step data not found for key:', stepDataKey);
        return;
    }

    // Display modal with profile details
    document.getElementById('modalTitle').textContent = stepData.name;
    displayProfiles(stepData.profiles, stepData.profile_data);
    document.getElementById('profileModal').style.display = 'block';
}
```

#### Tooltip Implementation
```css
.step-tooltip {
    position: absolute;
    top: -65px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0,0,0,0.9);
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 999999;
    max-width: 400px;
    text-align: center;
}

.step-box:hover .step-tooltip {
    opacity: 1;
}
```

## Profile Display Components

### Modal Profile Viewer

#### Structure
```html
<div id="profileModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2 class="modal-title" id="modalTitle">Step Details</h2>
            <span class="close-button" onclick="closeModal()">&times;</span>
        </div>

        <div id="profileCountInfo" class="profile-count-info">
            <strong>Total Profiles:</strong> 0
        </div>

        <input type="text" id="searchBox" class="search-box"
               placeholder="Search customer ID..."
               oninput="filterProfiles()">

        <div id="profilesContainer"></div>
    </div>
</div>
```

#### Profile Data Table
```css
.profiles-table {
    width: 100%;
    border-collapse: collapse;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 12px;
    color: #E0E0E0;
    background-color: #3A3A3A;
}

.profiles-table th {
    background-color: #2D2D2D;
    color: #FFFFFF;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 2px solid #444444;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 10;
}
```

### Keyboard Shortcuts

#### Auto-Load on Enter
The application supports pressing Enter in the Journey ID field to automatically trigger configuration loading:

```python
# In streamlit_app.py
journey_id = st.text_input(
    "Journey ID",
    placeholder="e.g., 12345",
    key="main_journey_id",
    on_change=lambda: st.session_state.update({"auto_load_triggered": True})
)

# Auto-load trigger handling
auto_load_triggered = st.session_state.get("auto_load_triggered", False)
if auto_load_triggered and journey_id:
    st.session_state["auto_load_triggered"] = False
    load_config_button = True  # Trigger the loading logic
```

### Search and Filtering

#### Search Implementation
```javascript
function filterProfiles() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();

    if (searchTerm === '') {
        currentProfiles = allProfiles;
    } else {
        if (allProfileData.length > 0) {
            // Search across all columns in the profile data
            const matchingCustomerIds = allProfileData
                .filter(profile => {
                    return Object.values(profile).some(value =>
                        String(value).toLowerCase().includes(searchTerm)
                    );
                })
                .map(profile => profile.cdp_customer_id);

            currentProfiles = matchingCustomerIds;
        } else {
            // Fallback to simple customer ID search
            currentProfiles = allProfiles.filter(profile =>
                profile.toLowerCase().includes(searchTerm)
            );
        }
    }

    displayProfiles(currentProfiles, allProfileData);
}
```

## Indentation and Hierarchy

### Merge Step Indentation Logic

The most complex UI challenge is properly displaying merge step hierarchies without duplication.

#### Problem Solved
**Before Fix:**
```
Merge (5eca44ab) (0 profiles)
Wait 1 day (0 profiles)          ← Same level as merge (incorrect)
End Step (0 profiles)            ← Same level as merge (incorrect)
```

**After Fix:**
```
Merge: (5eca44ab) - grouping header (3 profiles)
--- Wait 1 day (0 profiles)      ← Properly indented
--- End Step (0 profiles)        ← Properly indented
```

#### Implementation Solution
```python
# Bypass reorganization logic for merge hierarchies
if all_steps and not has_merge_points:
    # Original reorganization logic here
    pass
else:
    # Preserve merge hierarchy formatting
    formatted_steps = merge_display_formatter.format_merge_hierarchy(
        generator, journey_api_response
    )
```

### Breadcrumb Preservation

#### Breadcrumb Logic
```python
def build_breadcrumb_trail(steps_in_path: List[str]) -> str:
    """Build complete breadcrumb trail showing path progression."""
    breadcrumb_parts = []

    for step_id in steps_in_path:
        step_display = format_step_name(step_id)
        breadcrumb_parts.append(step_display)

    return " → ".join(breadcrumb_parts)
```

#### Post-Merge Breadcrumbs
For steps after merge points, breadcrumbs show the complete path:
```
Entry → Decision: country routing → Wait 3 days → Merge → Wait 1 day
```

## Interactive Elements

### Button Styling

#### Primary Buttons
```css
.stButton > button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"] {
    background-color: #0066CC !important;
    border-color: #0066CC !important;
    color: white !important;
}

.stButton > button[data-testid="baseButton-primary"]:hover,
.stButton > button[kind="primary"]:hover {
    background-color: #0052A3 !important;
    border-color: #0052A3 !important;
    color: white !important;
}
```

#### Download Buttons
```python
st.download_button(
    label="📥 Download as CSV",
    data=csv_data,
    file_name=f"step_{step_id}_profiles.csv",
    mime="text/csv",
    key=f"download_{step_id}"
)
```

### Progress Indicators

#### Loading States
```python
with st.spinner("Loading journey configuration..."):
    api_response, error = td_api_service.fetch_journey_data(journey_id)

with st.spinner("Loading profile data..."):
    profile_data = td_api_service.load_profile_data(journey_id, audience_id)
```

#### Status Messages
```python
st.toast(f"Journey configuration loaded successfully!", icon="✅")
st.toast(f"Profile data loaded: {len(profile_data)} profiles found.", icon="✅")
st.toast(f"API Error: {error}", icon="❌", duration=30)
```

## Implementation Details

### Component Architecture

#### Modular Structure
```python
# UI Component rendering functions
def render_configuration_panel() -> Tuple[str, bool]:
def render_attribute_selector() -> bool:
def render_journey_tabs() -> None:
def render_step_selection_tab(generator, column_mapper) -> None:
def render_canvas_tab(generator, column_mapper) -> None:
def render_data_tab(generator, column_mapper) -> None:
```

#### State Management
```python
# Session state for UI persistence
SessionStateManager.set("config_loaded", True)
SessionStateManager.set("journey_loaded", True)
SessionStateManager.set("selected_attributes", attributes)
```

### Performance Optimizations

#### Lazy Loading
- Profile data only loaded when explicitly requested
- Flowchart generation on-demand via button click
- Modal content populated only when step is clicked

#### Caching Strategy
- API responses cached in session state
- Column mapper initialized once per session
- Flowchart generator reused across tabs

#### Memory Management
- Large profile datasets handled with pagination
- Search results filtered client-side for responsiveness
- Modal content cleared between uses

---

This UI implementation provides a clean, hierarchical interface for complex journey data while maintaining good performance and user experience across all journey types and sizes.