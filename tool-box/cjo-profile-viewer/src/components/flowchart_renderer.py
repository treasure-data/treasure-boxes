"""
Flowchart Renderer Component

This module handles the generation of interactive HTML flowchart visualizations
for CJO journey data.
"""

import json
from typing import Dict, List
from ..flowchart_generator import CJOFlowchartGenerator
from ..styles import load_flowchart_styles
from ..utils.step_display import get_step_display_name
from ..utils.profile_filtering import get_step_profiles, get_filtered_profile_data


def _get_step_profiles_from_dict(generator: CJOFlowchartGenerator, step) -> List[str]:
    """Get profiles for a specific step (wrapper for shared utility)."""
    step_id = step.get('id', '')
    stage_idx = step.get('stage_idx', 0)

    if not step_id:
        return []

    try:
        return get_step_profiles(generator.profile_data, step_id, stage_idx)
    except Exception:
        return []


def _get_step_profile_data(generator: CJOFlowchartGenerator, step) -> List[Dict]:
    """Get profile data with additional attributes for a specific step."""
    import streamlit as st

    step_profiles = _get_step_profiles_from_dict(generator, step)

    if not step_profiles or generator.profile_data.empty:
        return []

    # Get selected attributes from session state
    selected_attributes = st.session_state.get("selected_attributes", [])

    # Filter profile data for customers in this step
    profile_data_subset = generator.profile_data[
        generator.profile_data['cdp_customer_id'].isin(step_profiles)
    ]

    # Select columns to include
    columns_to_show = ['cdp_customer_id'] + selected_attributes
    available_columns = [col for col in columns_to_show if col in profile_data_subset.columns]

    if available_columns:
        # Convert to list of dictionaries for JavaScript
        profile_records = profile_data_subset[available_columns].to_dict('records')
        return profile_records

    return []


def create_flowchart_html(generator: CJOFlowchartGenerator) -> str:
    """
    Create an HTML/CSS flowchart visualization.

    Args:
        generator: CJOFlowchartGenerator instance

    Returns:
        Complete HTML string with embedded CSS and JavaScript
    """
    # Get styles
    css = load_flowchart_styles()

    # Get journey summary
    summary = generator.get_journey_summary()

    # Define specific colors for different step types
    step_type_colors = {
        'DecisionPoint': '#f8eac5',        # Decision Point
        'DecisionPoint_Branch': '#f8eac5', # Decision Point Branch - yellow/beige
        'ABTest': '#f8eac5',               # AB Test
        'ABTest_Variant': '#f8eac5',       # AB Test Variant - yellow/beige
        'WaitStep': '#f8dcda',             # Wait Step - light pink/red
        'WaitCondition_Path': '#f8dcda',   # Wait Condition Path - light pink/red
        'Activation': '#d8f3ed',           # Activation - light green
        'Jump': '#e8eaff',                 # Jump - light blue/purple
        'End': '#e8eaff',                  # End Step - light blue/purple
        'Merge': '#f8eac5',                # Merge Step - yellow/beige (same as Decision/AB Test)
        'Unknown': '#f8eac5'               # Unknown - default to yellow/beige
    }

    # Build HTML content
    html = f'''
    {css}

    <div class="flowchart-container">
        <div class="journey-header">
            <strong>Journey:</strong> {summary.get('journey_name', 'N/A')} (ID: {summary.get('journey_id', 'N/A')})<br>
            <strong>Audience ID:</strong> {summary.get('audience_id', 'N/A')}<br>
            <strong>Total Profiles:</strong> {summary.get('total_profiles', 0)}<br>
            <strong>Stages:</strong> {len(summary.get('stages', []))}
        </div>
    '''

    # Collect step data for JavaScript
    step_data = {}

    # Process each stage using available properties
    stages_data = generator.stages_data
    for stage_idx, stage_data in enumerate(stages_data):
        stage_name = stage_data.get('name', f'Stage {stage_idx + 1}')

        html += f'''
        <div class="stage-container">
            <div class="stage-header">{stage_name}</div>
        '''

        # Add simple stage info
        steps = stage_data.get('steps', {})
        html += f'''
        <div class="stage-info">
            <div class="stage-info-section">
                <span class="stage-info-header">Steps:</span> {len(steps)}
            </div>
        </div>
        '''

        html += '<div class="paths-container">'

        # Process steps in this stage
        html += '<div class="path">'

        for i, (step_id, step_data_dict) in enumerate(steps.items()):
            # Use shared utility for consistent step naming
            step_name = get_step_display_name(step_data_dict)
            step_type = step_data_dict.get('type', 'Unknown')

            # Create step object for helper functions
            step_obj = {
                'id': step_id,
                'name': step_name,
                'type': step_type,
                'stage_idx': stage_idx
            }

            # Get profile count for this step
            step_profiles = _get_step_profiles_from_dict(generator, step_obj)
            profile_count = len(step_profiles)

            # Get profile data for modal
            step_profile_data = _get_step_profile_data(generator, step_obj)

            # Store step data for JavaScript
            step_data_key = f"step_{stage_idx}_{i}_{step_id}"
            step_data[step_data_key] = {
                'name': step_name,
                'type': step_type,
                'profiles': step_profiles,
                'profile_data': step_profile_data
            }

            # Get color for step type
            color = step_type_colors.get(step_type, step_type_colors['Unknown'])

            # Use step name directly (column mapper is for database columns, not step names)
            display_name = step_name

            # Create tooltip content
            tooltip_content = f"Type: {step_type}\\nProfiles: {profile_count}"
            if step_id:
                tooltip_content += f"\\nID: {step_id}"

            html += f'''
            <div class="step-box" style="background-color: {color};"
                 onclick="showProfileModal('{step_data_key}')"
                 title="{tooltip_content}">
                <div class="step-name">{display_name}</div>
                <div class="step-count">{profile_count} profiles</div>
                <div class="step-tooltip">{tooltip_content}</div>
            </div>
            '''

            # Add arrow if not last step
            if i < len(steps) - 1:
                html += '<div class="arrow">→</div>'

        html += '</div>'  # Close path div
        html += '</div>'  # Close paths-container div
        html += '</div>'  # Close stage-container div

    # Convert step data to JSON
    step_data_json = json.dumps(step_data)

    # Add JavaScript for interactivity
    html += f'''
    <script>
    // Step data store
    const stepDataStore = {step_data_json};

    let currentProfiles = [];
    let allProfiles = [];
    let allProfileData = [];

    function showProfileModal(stepDataKey) {{
        const stepData = stepDataStore[stepDataKey];
        if (!stepData) {{
            console.error('Step data not found for key:', stepDataKey);
            return;
        }}

        const stepName = stepData.name;
        const profiles = stepData.profiles;
        const profileData = stepData.profile_data || [];

        allProfiles = profiles;
        allProfileData = profileData;
        currentProfiles = profiles;

        document.getElementById('modalTitle').textContent = stepName;
        document.getElementById('profileCountInfo').innerHTML =
            `<strong>Total Profiles:</strong> ${{profiles.length}}`;

        document.getElementById('searchBox').value = '';
        document.getElementById('searchBox').placeholder = profileData.length > 0 ?
            'Search customer ID or any attribute...' : 'Search customer ID...';

        displayProfiles(profiles, profileData);
        document.getElementById('profileModal').style.display = 'block';
    }}

    function closeModal() {{
        document.getElementById('profileModal').style.display = 'none';
    }}

    function filterProfiles() {{
        const searchTerm = document.getElementById('searchBox').value.toLowerCase();

        if (searchTerm === '') {{
            currentProfiles = allProfiles;
        }} else {{
            if (allProfileData.length > 0) {{
                // Search across all columns in the profile data
                const matchingCustomerIds = allProfileData
                    .filter(profile => {{
                        return Object.values(profile).some(value =>
                            String(value).toLowerCase().includes(searchTerm)
                        );
                    }})
                    .map(profile => profile.cdp_customer_id);

                currentProfiles = matchingCustomerIds;
            }} else {{
                // Fallback to simple customer ID search
                currentProfiles = allProfiles.filter(profile =>
                    profile.toLowerCase().includes(searchTerm)
                );
            }}
        }}

        displayProfiles(currentProfiles, allProfileData);
    }}

    function displayProfiles(profiles, profileData) {{
        const container = document.getElementById('profilesContainer');

        if (profiles.length === 0) {{
            container.innerHTML = '<div class="no-profiles">No profiles found matching your search.</div>';
            return;
        }}

        if (profileData.length > 0) {{
            // Display as table with additional attributes
            const headers = Object.keys(profileData[0]);
            let tableHtml = '<table class="profiles-table"><thead><tr>';

            headers.forEach(header => {{
                tableHtml += `<th>${{header}}</th>`;
            }});

            tableHtml += '</tr></thead><tbody>';

            // Filter profileData to only show current profiles
            const filteredData = profileData.filter(row =>
                profiles.includes(row.cdp_customer_id)
            );

            filteredData.forEach(row => {{
                tableHtml += '<tr>';
                headers.forEach(header => {{
                    tableHtml += `<td>${{row[header] || ''}}</td>`;
                }});
                tableHtml += '</tr>';
            }});

            tableHtml += '</tbody></table>';
            container.innerHTML = tableHtml;
        }} else {{
            // Display as simple list
            const listHtml = profiles
                .map(profile => `<div class="profile-item">${{profile}}</div>`)
                .join('');
            container.innerHTML = `<div class="profiles-list">${{listHtml}}</div>`;
        }}

        // Update profile count
        document.getElementById('profileCountInfo').innerHTML =
            `<strong>Showing:</strong> ${{profiles.length}} of ${{allProfiles.length}} profiles`;
    }}

    // Handle Enter key in search box
    document.addEventListener('DOMContentLoaded', function() {{
        const searchBox = document.getElementById('searchBox');
        if (searchBox) {{
            searchBox.addEventListener('keyup', function(event) {{
                if (event.key === 'Enter') {{
                    filterProfiles();
                }}
            }});
        }}
    }});

    // Close modal when clicking outside
    window.onclick = function(event) {{
        const modal = document.getElementById('profileModal');
        if (event.target === modal) {{
            closeModal();
        }}
    }}
    </script>

    <!-- Modal -->
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
                   oninput="filterProfiles()"
                   onkeyup="if(event.key==='Enter') filterProfiles();">

            <div id="profilesContainer"></div>
        </div>
    </div>

    </div>
    '''

    return html