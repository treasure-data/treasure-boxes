"""
CJO Profile Viewer - Streamlit Application

A tool for visualizing Customer Journey Orchestration (CJO) journeys with profile data.
This app reads journey API responses and profile CSV data to create interactive flowcharts.
"""

import streamlit as st
import pandas as pd
import json
import requests
import os
import pytd
from typing import Dict, List, Optional, Tuple

from src.column_mapper import CJOColumnMapper
from src.flowchart_generator import CJOFlowchartGenerator


def get_api_key():
    """Get TD API key from environment variable or config file."""
    # First try environment variable
    api_key = os.getenv('TD_API_KEY')
    if api_key:
        return api_key

    # Try to read from config file
    config_paths = [
        os.path.expanduser('~/.td/config'),
        'td_config.txt',
        '.env'
    ]

    for config_path in config_paths:
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    for line in f:
                        if line.startswith('TD_API_KEY=') or line.startswith('apikey='):
                            return line.split('=', 1)[1].strip()
        except Exception:
            continue

    return None


def fetch_journey_data(journey_id: str, api_key: str) -> Tuple[Optional[dict], Optional[str]]:
    """Fetch journey data from TD API."""
    if not journey_id or not api_key:
        return None, "Journey ID and API key are required"

    url = f"https://api-cdp.treasuredata.com/entities/journeys/{journey_id}"
    headers = {
        'Authorization': f'TD1 {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        with st.spinner(f"Fetching journey data for ID: {journey_id}..."):
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 401:
                return None, "Authentication failed. Please check your API key."
            elif response.status_code == 404:
                return None, f"Journey ID '{journey_id}' not found."
            else:
                return None, f"API request failed with status {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to TD API. Please check your internet connection."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def get_available_attributes(audience_id: str, api_key: str) -> List[str]:
    """Get list of available customer attributes from the customers table."""
    if not audience_id or not api_key:
        return []

    try:
        with st.spinner("Loading available customer attributes..."):
            client = pytd.Client(
                apikey=api_key,
                endpoint='https://api.treasuredata.com',
                engine='presto'
            )

            # Query to describe the customers table
            describe_query = f"DESCRIBE cdp_audience_{audience_id}.customers"
            result = client.query(describe_query)

            if result and result.get('data'):
                # Extract column names, excluding 'time' and 'cdp_customer_id'
                columns = [row[0] for row in result['data'] if row[0] not in ['time', 'cdp_customer_id']]
                return sorted(columns)

    except Exception as e:
        st.toast(f"Could not load customer attributes: {str(e)}", icon="⚠️")

    return []

def load_profile_data(journey_id: str, audience_id: str, api_key: str) -> Optional[pd.DataFrame]:
    """Load profile data using pytd from live Treasure Data tables."""
    if not journey_id or not audience_id or not api_key:
        st.error("Journey ID, Audience ID, and API key are required for live data query")
        return None

    try:
        # Initialize pytd client with presto engine and api.treasuredata.com endpoint
        with st.spinner(f"Connecting to Treasure Data and querying profile data..."):
            client = pytd.Client(
                apikey=api_key,
                endpoint='https://api.treasuredata.com',
                engine='presto'
            )

            # Check if additional attributes are selected
            selected_attributes = st.session_state.get("selected_attributes", [])

            # Construct the query for live profile data
            table_name = f"cdp_audience_{audience_id}.journey_{journey_id}"

            if selected_attributes:
                # JOIN query with additional attributes from customers table
                attributes_str = ", ".join([f"c.{attr}" for attr in selected_attributes])
                query = f"""
                SELECT j.cdp_customer_id, {attributes_str}
                FROM {table_name} j
                JOIN cdp_audience_{audience_id}.customers c
                ON c.cdp_customer_id = j.cdp_customer_id
                """
                st.toast(f"Querying journey table with {len(selected_attributes)} additional attributes", icon="🔍")
            else:
                # Standard query without JOIN
                query = f"SELECT * FROM {table_name}"
                st.toast(f"Querying table: {table_name}", icon="🔍")

            # Execute the query and return as DataFrame
            query_result = client.query(query)

            # Convert the result to a pandas DataFrame
            if not query_result.get('data'):
                st.toast(f"No data found in table {table_name}", icon="⚠️")
                return pd.DataFrame()

            profile_data = pd.DataFrame(query_result['data'], columns=query_result['columns'])

            # If we used JOIN query, we need to merge back with the full journey data
            if selected_attributes and not profile_data.empty:
                # Get the full journey data for journey step information
                full_journey_query = f"SELECT * FROM {table_name}"
                full_result = client.query(full_journey_query)

                if full_result and full_result.get('data'):
                    full_journey_data = pd.DataFrame(full_result['data'], columns=full_result['columns'])

                    # Merge the customer attributes with the full journey data
                    profile_data = full_journey_data.merge(
                        profile_data,
                        on='cdp_customer_id',
                        how='left'
                    )

            return profile_data

    except Exception as e:
        error_msg = str(e)
        st.error(f"Error querying live profile data: {error_msg}")

        # Provide helpful error messages for common issues
        if "Table not found" in error_msg or "does not exist" in error_msg:
            st.error(f"Table 'cdp_audience_{audience_id}.journey_{journey_id}' does not exist. Please verify the audience ID and journey ID. Note: The journey workflow may not have been run yet and the audience needs to be built first.")
        elif "Authentication" in error_msg or "401" in error_msg:
            st.error("Authentication failed. Please check your TD API key.")
        elif "Permission denied" in error_msg or "403" in error_msg:
            st.error("Permission denied. Please ensure your API key has access to the audience data.")

        return None


def create_flowchart_html(generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Create an HTML/CSS flowchart visualization."""

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

    # Store all step profile data
    step_data_store = {}

    # CSS styles
    css = """
    <style>
    .flowchart-container {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: "Source Sans Pro", sans-serif;
        border: 1px solid #333333;
    }

    .journey-header {
        background-color: #2D2D2D;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #444444;
        font-size: 14px;
    }

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

    .stage-info {
        background-color: #d4ebf7;
        color: #000000;
        padding: 15px 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 13px;
        border: 1px solid rgba(0,0,0,0.1);
        line-height: 1.6;
    }

    .stage-info-section {
        display: inline-block;
        margin-right: 30px;
        font-weight: normal;
    }

    .stage-info-header {
        font-weight: bold;
        color: #000000;
    }

    .paths-container {
        position: relative;
    }

    .path {
        display: flex;
        align-items: center;
        margin: 20px 0;
        justify-content: flex-start;
        flex-wrap: wrap;
        gap: 10px;
    }

    .step-box {
        background-color: #f8eac5;
        color: #000000;
        padding: 15px 20px;
        margin: 5px 0;
        border-radius: 8px;
        border: 1px solid rgba(0,0,0,0.1);
        min-width: 180px;
        max-width: 220px;
        text-align: center;
        cursor: pointer;
        font-weight: 600;
        font-size: 13px;
        line-height: 1.3;
        transition: all 0.3s ease;
        position: relative;
        font-family: "Source Sans Pro", sans-serif;
        flex-shrink: 0;
    }

    .step-box:hover {
        transform: scale(1.03);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-color: #85C1E9;
    }

    .step-name {
        font-size: 12px;
        margin-bottom: 5px;
        word-wrap: break-word;
        font-weight: 600;
        color: #000000;
    }

    .step-count {
        font-size: 11px;
        font-weight: 400;
        color: #000000;
    }

    .arrow {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: bold;
        margin: 0 5px;
        opacity: 0.8;
        flex-shrink: 0;
        align-self: center;
    }

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
        white-space: pre-line;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s;
        z-index: 999999;
        max-width: 400px;
        text-align: center;
        word-wrap: break-word;
    }

    /* Adjust tooltip position for elements near left edge */
    .path .step-box:first-child .step-tooltip {
        left: 0;
        transform: translateX(0);
    }

    /* Adjust tooltip position for elements near right edge */
    .path .step-box:last-child .step-tooltip {
        left: auto;
        right: 0;
        transform: translateX(0);
    }

    /* Ensure tooltips don't go off-screen */
    .step-tooltip {
        min-width: 200px;
    }

    .step-box {
        position: relative;
        z-index: 1;
    }

    .step-box:hover {
        z-index: 1000000;
    }

    .step-box:hover .step-tooltip {
        opacity: 1;
    }

    /* Modal styles */
    .modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.8);
        font-family: Arial, sans-serif;
    }

    .modal-content {
        background-color: #2D2D2D;
        margin: 5% auto;
        padding: 20px;
        border: 1px solid #444444;
        border-radius: 8px;
        width: 90%;
        max-width: 1200px;
        min-width: 600px;
        max-height: 80%;
        overflow-y: auto;
        color: #FFFFFF;
        font-family: "Source Sans Pro", sans-serif;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #444444;
        padding-bottom: 10px;
    }

    .modal-title {
        font-size: 18px;
        font-weight: 600;
        color: #FFFFFF;
    }

    .close-button {
        color: #CCCCCC;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        background: none;
        border: none;
    }

    .close-button:hover {
        color: #FF6B6B;
    }

    .search-box {
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #444444;
        border-radius: 5px;
        background-color: #3A3A3A;
        color: #FFFFFF;
        font-size: 14px;
        font-family: "Source Sans Pro", sans-serif;
    }

    .search-box::placeholder {
        color: #AAAAAA;
    }

    .search-box:focus {
        outline: none;
        border-color: #666666;
        background-color: #404040;
    }

    .profiles-list {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #444444;
        border-radius: 5px;
        background-color: #3A3A3A;
    }

    .profile-item {
        padding: 8px 12px;
        border-bottom: 1px solid #444444;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 12px;
        color: #E0E0E0;
    }

    .profile-item:hover {
        background-color: #404040;
    }

    .profile-item:last-child {
        border-bottom: none;
    }

    .no-profiles {
        text-align: center;
        padding: 20px;
        color: #AAAAAA;
        font-style: italic;
    }

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

    .profiles-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #444444;
        vertical-align: top;
    }

    .profiles-table tr:hover {
        background-color: #404040;
    }

    .profiles-table tr:last-child td {
        border-bottom: none;
    }

    .profile-count-info {
        margin-bottom: 15px;
        padding: 10px;
        background-color: #3A3A3A;
        border-radius: 5px;
        font-size: 14px;
        color: #E0E0E0;
        border: 1px solid #555555;
    }
    </style>
    """

    # Build HTML content
    html = css + '<div class="flowchart-container">'

    # Journey header
    html += f'''
    <div class="journey-header">
        <strong>Journey:</strong> {summary['journey_name']} (ID: {summary['journey_id']})
    </div>
    '''

    # Process each stage
    for stage_idx, stage in enumerate(generator.stages):
        html += f'<div class="stage-container">'
        html += f'<div class="stage-header">Stage {stage_idx + 1}: {stage.name}</div>'

        # Stage info with better formatting
        entry_criteria = stage.entry_criteria or 'None'
        milestone = stage.milestone or 'No Milestone'
        profiles_count = summary['stage_counts'].get(stage_idx, 0)

        stage_info = f'''
        <div class="stage-info">
            <div class="stage-info-section">
                <span class="stage-info-header">Entry:</span> {entry_criteria}
            </div>
            <div class="stage-info-section">
                <span class="stage-info-header">Milestone:</span> {milestone}
            </div>
            <div class="stage-info-section">
                <span class="stage-info-header">Profiles in Stage:</span> {profiles_count}
            </div>
        </div>
        '''

        html += stage_info

        # Paths container
        html += '<div class="paths-container">'

        # Process each path in the stage
        for path_idx, path in enumerate(stage.paths):
            html += '<div class="path">'

            # Filter out DecisionPoint steps for display, but keep them for logic
            visible_steps = [(idx, step) for idx, step in enumerate(path) if step.step_type != 'DecisionPoint']

            # Process each visible step in the path
            for display_idx, (step_idx, step) in enumerate(visible_steps):
                # Get color for step type
                step_color = step_type_colors.get(step.step_type, step_type_colors['Unknown'])

                # Create step name with prefixes for grouping types
                if step.step_type == 'DecisionPoint_Branch':
                    display_name = f"Decision: {step.name}"
                elif step.step_type == 'ABTest_Variant':
                    display_name = f"AB: {step.name}"
                elif step.step_type == 'WaitCondition_Path':
                    display_name = step.name  # Already formatted as "Wait Condition <wait_name>: <path_name>"
                else:
                    display_name = step.name

                # Truncate display name if too long
                step_name = display_name[:25] + "..." if len(display_name) > 25 else display_name

                # Create tooltip info - show full display name and step UUID on separate lines
                tooltip = f"{display_name}\n({step.step_id})"

                # Determine the count text based on step type
                if step.step_type in ['DecisionPoint_Branch', 'ABTest_Variant', 'WaitCondition_Path']:
                    # For groupings, don't show profile count
                    count_text = ""
                else:
                    # For actual steps, show "In Step: X"
                    count_text = f"In Step: {step.profile_count}"

                # Get profiles for this step
                step_profiles = _get_step_profiles(generator, step)

                # Get full profile data with attributes for this step
                step_profile_data = _get_step_profile_data(generator, step)

                # Store step data for JavaScript access
                step_data_key = f"step_{stage_idx}_{path_idx}_{step_idx}"
                step_data_store[step_data_key] = {
                    'name': step.name,
                    'profiles': step_profiles,
                    'profile_data': step_profile_data
                }

                # Create step box with click handler (only clickable if has profiles)
                step_name_js = step.name.replace("'", "\\'").replace('"', '\\"')
                cursor_style = "cursor: pointer;" if step.profile_count > 0 else "cursor: default;"
                click_handler = f"showProfileModal('{step_data_key}')" if step.profile_count > 0 else ""

                step_html = f'''
                <div class="step-box"
                     style="background-color: {step_color}; {cursor_style}"
                     onclick="{click_handler}">
                    <div class="step-name">{step_name}</div>
                    <div class="step-count">{count_text}</div>
                    <div class="step-tooltip">{tooltip}</div>
                </div>
                '''
                html += step_html

                # Add arrow if not the last visible step
                if display_idx < len(visible_steps) - 1:
                    html += '<div class="arrow">→</div>'

            html += '</div>'  # End path

        html += '</div>'  # End paths-container
        html += '</div>'  # End stage-container

    html += '</div>'  # End flowchart-container

    # Add modal HTML
    html += '''
    <!-- Profile Modal -->
    <div id="profileModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">Step Profiles</div>
                <button class="close-button" onclick="closeModal()">&times;</button>
            </div>
            <div class="profile-count-info" id="profileCountInfo"></div>
            <input type="text" class="search-box" id="searchBox" placeholder="Search by Customer ID..." onkeyup="filterProfiles()">
            <div class="profiles-list" id="profilesList">
                <div class="no-profiles">No profiles to display</div>
            </div>
        </div>
    </div>
    '''

    # Add the step data store as JavaScript
    step_data_json = json.dumps(step_data_store)
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
                // Fall back to searching just customer IDs
                currentProfiles = allProfiles.filter(profile =>
                    profile.toLowerCase().includes(searchTerm)
                );
            }}
        }}

        const currentProfileData = allProfileData.filter(profile =>
            currentProfiles.includes(profile.cdp_customer_id)
        );

        displayProfiles(currentProfiles, currentProfileData);
    }}

    function displayProfiles(profiles, profileData = []) {{
        const profilesList = document.getElementById('profilesList');

        if (profiles.length === 0) {{
            profilesList.innerHTML = '<div class="no-profiles">No profiles found</div>';
            return;
        }}

        let html = '';

        if (profileData.length > 0 && profileData.length === profiles.length) {{
            // Display full profile data with attributes in table format
            const keys = Object.keys(profileData[0]);

            // Create table with headers
            html += '<table class="profiles-table">';
            html += '<thead><tr>';
            keys.forEach(key => {{
                const headerName = key === 'cdp_customer_id' ? 'Customer ID' : key;
                html += `<th>${{headerName}}</th>`;
            }});
            html += '</tr></thead>';

            // Create table body with data
            html += '<tbody>';
            profileData.forEach(profile => {{
                html += '<tr>';
                keys.forEach(key => {{
                    const value = profile[key] || 'N/A';
                    html += `<td>${{value}}</td>`;
                }});
                html += '</tr>';
            }});
            html += '</tbody></table>';
        }} else {{
            // Fall back to displaying just customer IDs in table format
            html += '<table class="profiles-table">';
            html += '<thead><tr><th>Customer ID</th></tr></thead>';
            html += '<tbody>';
            profiles.forEach(profile => {{
                html += `<tr><td>${{profile}}</td></tr>`;
            }});
            html += '</tbody></table>';
        }}

        profilesList.innerHTML = html;

        // Update count info
        document.getElementById('profileCountInfo').innerHTML =
            `<strong>Showing:</strong> ${{profiles.length}} of ${{allProfiles.length}} profiles`;
    }}

    // Close modal when clicking outside
    window.onclick = function(event) {{
        const modal = document.getElementById('profileModal');
        if (event.target === modal) {{
            closeModal();
        }}
    }}

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {{
        if (event.key === 'Escape') {{
            closeModal();
        }}
    }});
    </script>
    '''

    return html

def _get_step_profiles(generator: CJOFlowchartGenerator, step):
    """Get list of customer IDs for profiles in a specific step."""
    # Determine the column name for this step
    step_column = None

    if '_branch_' in step.step_id:
        # Decision point branch
        parts = step.step_id.split('_branch_')
        if len(parts) == 2:
            step_uuid = parts[0].replace('-', '_')
            segment_id = parts[1]
            step_column = f"intime_stage_{step.stage_index}_{step_uuid}_{segment_id}"
    elif '_variant_' in step.step_id:
        # AB test variant
        parts = step.step_id.split('_variant_')
        if len(parts) == 2:
            step_uuid = parts[0].replace('-', '_')
            variant_uuid = parts[1].replace('-', '_')
            step_column = f"intime_stage_{step.stage_index}_{step_uuid}_variant_{variant_uuid}"
    else:
        # Regular step
        step_uuid = step.step_id.replace('-', '_')
        step_column = f"intime_stage_{step.stage_index}_{step_uuid}"

    if step_column and step_column in generator.profile_data.columns:
        # Get the corresponding outtime column
        outtime_column = step_column.replace('intime_', 'outtime_')

        # Filter profiles that have entered (intime not null) but not exited (outtime is null)
        condition = generator.profile_data[step_column].notna()

        if outtime_column in generator.profile_data.columns:
            # Exclude profiles that have exited (outtime is not null)
            condition = condition & generator.profile_data[outtime_column].isna()

        profiles = generator.profile_data[condition]['cdp_customer_id'].tolist()
        return profiles

    return []

def _get_step_profile_data(generator: CJOFlowchartGenerator, step):
    """Get full profile data with attributes for profiles in a specific step."""
    # Get customer IDs in this step
    step_profiles = _get_step_profiles(generator, step)

    if not step_profiles or generator.profile_data.empty:
        return []

    # Get selected attributes from session state
    import streamlit as st
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


def show_step_details(step_info: Dict, generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Show detailed information about a selected step."""
    st.subheader(f"Step Details: {step_info['name']}")

    # Show breadcrumb trail if available
    if 'breadcrumbs' in step_info and len(step_info['breadcrumbs']) > 1:
        st.markdown("### 🧭 Journey Path")

        # Show individual breadcrumb steps with styling directly under the header
        breadcrumb_html = '<div style="display: flex; align-items: center; gap: 10px; margin: 10px 0; flex-wrap: wrap;">'

        # Define step type colors for journey path
        step_type_colors = {
            'DecisionPoint': '#f8eac5',        # Decision Point
            'DecisionPoint_Branch': '#f8eac5', # Decision Point Branch - yellow/beige
            'ABTest': '#f8eac5',               # AB Test
            'ABTest_Variant': '#f8eac5',       # AB Test Variant - yellow/beige
            'WaitStep': '#f8dcda',             # Wait Step - light pink/red
            'Activation': '#d8f3ed',           # Activation - light green
            'Jump': '#e8eaff',                 # Jump - light blue/purple
            'End': '#e8eaff',                  # End Step - light blue/purple
            'Merge': '#d5e7f0',                # Merge Step - light blue
            'Unknown': '#f8eac5'               # Unknown - default to yellow/beige
        }

        # We need to get step types for each breadcrumb step
        # This requires looking up the step info for each breadcrumb
        for i, crumb in enumerate(step_info['breadcrumbs']):
            # Check if this is the stage entry criteria (first item and has stage_entry_criteria)
            is_entry_criteria = (i == 0 and step_info.get('stage_entry_criteria') and
                                crumb == step_info['stage_entry_criteria'])

            if i == len(step_info['breadcrumbs']) - 1:
                # Current step - use its step type color with blue border
                step_type = step_info.get('step_type', 'Unknown')
                bg_color = step_type_colors.get(step_type, '#f8eac5')
                breadcrumb_html += f'''
                <div style="background-color: {bg_color}; color: #000000; padding: 8px 12px; border-radius: 4px; font-weight: normal; border: 2px solid #0066CC;">
                    {crumb}
                </div>
                '''
            elif is_entry_criteria:
                # Stage entry criteria - use specified background color
                breadcrumb_html += f'''
                <div style="background-color: #d4ebf7; color: #000000; padding: 8px 12px; border-radius: 4px; font-weight: normal;">
                    {crumb}
                </div>
                '''
            else:
                # Previous steps - need to find their step type from all_steps
                # For now, use default muted color since we don't have easy access to previous step types
                breadcrumb_html += f'''
                <div style="background-color: #f0f0f0; color: #000000; padding: 8px 12px; border-radius: 4px; font-weight: normal;">
                    {crumb}
                </div>
                '''

            if i < len(step_info['breadcrumbs']) - 1:
                breadcrumb_html += '<div style="color: #666; font-weight: bold;">→</div>'

        breadcrumb_html += '</div>'
        st.markdown(breadcrumb_html, unsafe_allow_html=True)

    st.markdown("### 📊 Step Information")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Step Type:** {step_info['step_type']}")
        st.write(f"**Stage:** {step_info['stage_index'] + 1}")
        st.write(f"**Profiles in Step:** {step_info['profile_count']}")

    with col2:
        # Generate intime/outtime column names for this step
        if '_branch_' in step_info['step_id']:
            # Decision point branch
            parts = step_info['step_id'].split('_branch_')
            if len(parts) == 2:
                step_uuid = parts[0].replace('-', '_')
                segment_id = parts[1]
                intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
                outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
        elif '_variant_' in step_info['step_id']:
            # AB test variant
            parts = step_info['step_id'].split('_variant_')
            if len(parts) == 2:
                step_uuid = parts[0].replace('-', '_')
                variant_uuid = parts[1].replace('-', '_')
                intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
                outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
        else:
            # Regular step
            step_uuid = step_info['step_id'].replace('-', '_')
            intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}"
            outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}"

        st.markdown(f"**Step UUID:** `{step_info['step_id']}`")
        st.markdown(f"**Intime Column:** `{intime_column}`")
        st.markdown(f"**Outtime Column:** `{outtime_column}`")

    # Get profiles in this step
    if step_info['profile_count'] > 0:
        # Try to find the corresponding column name
        step_column = None

        # For regular steps
        if '_branch_' in step_info['step_id']:
            # Decision point branch
            parts = step_info['step_id'].split('_branch_')
            if len(parts) == 2:
                step_uuid = parts[0].replace('-', '_')
                segment_id = parts[1]
                step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
        elif '_variant_' in step_info['step_id']:
            # AB test variant
            parts = step_info['step_id'].split('_variant_')
            if len(parts) == 2:
                step_uuid = parts[0].replace('-', '_')
                variant_uuid = parts[1].replace('-', '_')
                step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
        else:
            # Regular step
            step_uuid = step_info['step_id'].replace('-', '_')
            step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}"

        if step_column:
            profiles = generator.get_profiles_in_step(step_column)

            if profiles:
                st.subheader("Profiles in this Step")

                # Add search/filter functionality
                search_term = st.text_input("Filter by Customer ID:", placeholder="Enter customer ID to search...")

                # Filter profiles if search term is provided
                if search_term:
                    filtered_profiles = [p for p in profiles if search_term.lower() in p.lower()]
                else:
                    filtered_profiles = profiles

                st.write(f"Showing {len(filtered_profiles)} of {len(profiles)} profiles")

                # Display profiles in a scrollable container
                if filtered_profiles:
                    # Create DataFrame for better display
                    profile_df = pd.DataFrame({'Customer ID': filtered_profiles})
                    st.dataframe(profile_df, height=300)

                    # Add download button
                    csv = profile_df.to_csv(index=False)
                    st.download_button(
                        label="Download Profile List",
                        data=csv,
                        file_name=f"profiles_{step_info['name'].replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.write("No profiles match the search criteria.")
            else:
                st.write("No profiles found for this step.")
        else:
            st.write("Could not determine column name for this step.")


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="CJO Profile Viewer",
        page_icon="🔍",
        layout="wide"
    )

    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .main {
        background-color: #2C3E50;
    }
    .stTitle {
        color: white;
    }
    .stMarkdown {
        color: white;
    }
    .stSelectbox label {
        color: white;
    }
    .stTextInput label {
        color: white;
    }
    .stDataFrame {
        background-color: white;
    }

    """, unsafe_allow_html=True)

    st.title("🔍 CJO Profile Viewer")
    st.markdown("**Visualize Customer Journey Orchestration journeys with profile data**")

    # Journey loading container
    with st.container():
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            journey_id = st.text_input(
                "Journey ID",
                placeholder="e.g., 12345",
                key="main_journey_id",
                on_change=lambda: st.session_state.update({"auto_load_triggered": True}),
                label_visibility="collapsed"
            )
        with col2:
            load_config_button = st.button(
                "📋 Load Journey Config",
                type="primary",
                key="load_config_button"
            )

        # Additional Customer Attributes Selection (show after config loaded)
        if st.session_state.get("config_loaded") and st.session_state.get("api_response"):
            st.markdown("**Step 2: Select Additional Customer Attributes**")
            st.caption("Select additional customer attributes to include when viewing step profiles. cdp_customer_id is included by default.")

            try:
                audience_id = st.session_state.api_response.get('data', {}).get('attributes', {}).get('audienceId')
                if audience_id and audience_id in st.session_state.get("available_attributes", {}):
                    available_attributes = st.session_state.available_attributes[audience_id]

                    if available_attributes:
                        selected_attributes = st.multiselect(
                            "Select customer attributes:",
                            options=available_attributes,
                            default=st.session_state.get("selected_attributes", []),
                            key="attribute_selector",
                            help="These attributes will be joined from the customers table",
                            label_visibility="collapsed"
                        )

                        # Store selected attributes in session state
                        st.session_state.selected_attributes = selected_attributes

                        # Show Load Profile Data button
                        load_profile_button = st.button(
                            "📊 Load Profile Data",
                            type="primary",
                            key="load_profile_button",
                            help="Load customer profile data with selected attributes"
                        )
                    else:
                        st.info("No additional customer attributes available.")
                        # Show Load Profile Data button even without attributes
                        load_profile_button = st.button(
                            "📊 Load Profile Data",
                            type="primary",
                            key="load_profile_button_no_attr",
                            help="Load customer profile data"
                        )
                else:
                    st.warning("Could not find audience ID or attributes not loaded.")
                    load_profile_button = False
            except Exception as e:
                st.warning(f"Could not load customer attributes: {str(e)}")
                load_profile_button = False
        else:
            st.caption("Load journey configuration first to see available customer attributes.")
            load_profile_button = False

        # Check for existing API key (but don't show status)
        existing_api_key = get_api_key()

        # Check for auto-load trigger (when user presses Enter)
        auto_load_triggered = st.session_state.get("auto_load_triggered", False)
        if auto_load_triggered and journey_id:
            st.session_state["auto_load_triggered"] = False
            load_config_button = True  # Trigger the loading logic

        # Handle Step 1: Load Journey Configuration
        if load_config_button:
            if not journey_id or journey_id.strip() == "":
                st.toast("Please enter a Journey ID", icon="⚠️")
                st.stop()

        if load_config_button and journey_id:
            if not existing_api_key:
                st.error("❌ **API Key Required**: Please set up your TD API key (TD_API_KEY environment variable, ~/.td/config, or td_config.txt file)")
                st.stop()

            # Fetch journey data
            api_response, error = fetch_journey_data(journey_id, existing_api_key)

            if error:
                st.toast(f"API Error: {error}", icon="❌", duration=30)
                st.stop()

            if api_response:
                st.session_state.api_response = api_response
                st.session_state.config_loaded = True

                # Extract audience ID from API response
                audience_id = None
                try:
                    audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId')
                    if not audience_id:
                        st.error("❌ **API Response Error**: Audience ID not found in API response")
                        st.stop()
                except Exception as e:
                    st.error(f"❌ **API Response Error**: Failed to extract audience ID: {str(e)}")
                    st.stop()

                # Load available customer attributes
                available_attributes = get_available_attributes(audience_id, existing_api_key)

                # Store available attributes in session state
                if "available_attributes" not in st.session_state:
                    st.session_state.available_attributes = {}
                st.session_state.available_attributes[audience_id] = available_attributes

                # Reset profile data and journey_loaded state since we're doing this in two steps
                st.session_state.profile_data = None
                st.session_state.journey_loaded = False

                st.toast(f"Journey configuration for '{journey_id}' loaded successfully! Now select attributes and load profile data.", icon="✅")

                # Force a rerun to show the attribute selector
                st.rerun()

        # Handle Step 2: Load Profile Data
        if load_profile_button:
            if not st.session_state.get("config_loaded") or not st.session_state.get("api_response"):
                st.toast("Please load journey configuration first", icon="⚠️")
                st.stop()

            if not existing_api_key:
                st.error("❌ **API Key Required**: Please set up your TD API key")
                st.stop()

            # Get journey and audience info from session state
            api_response = st.session_state.api_response
            journey_id = api_response.get('data', {}).get('id')
            audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId')

            if not journey_id or not audience_id:
                st.error("❌ Missing journey or audience ID from configuration")
                st.stop()

            # Load profile data using pytd
            profile_data = load_profile_data(journey_id, audience_id, existing_api_key)
            if profile_data is not None:
                st.session_state.profile_data = profile_data
                st.session_state.journey_loaded = True  # Now we have complete data
                st.toast(f"Profile data loaded successfully! {len(profile_data)} profiles found.", icon="✅")
            else:
                st.toast("Could not load profile data. Some features may be limited.", icon="⚠️")

            # Force a rerun to show the visualization
            st.rerun()

        st.markdown("---")

    # Initialize session state for data
    if 'api_response' not in st.session_state:
        st.session_state.api_response = None
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
    if 'journey_loaded' not in st.session_state:
        st.session_state.journey_loaded = False
    if 'config_loaded' not in st.session_state:
        st.session_state.config_loaded = False
    if 'available_attributes' not in st.session_state:
        st.session_state.available_attributes = {}
    if 'auto_load_attempted' not in st.session_state:
        st.session_state.auto_load_attempted = False


    # Add global CSS styling for the blue button
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)


    # Check if we have data to work with
    if not st.session_state.journey_loaded or st.session_state.api_response is None:
        if not st.session_state.config_loaded:
            st.info("👆 **Step 1**: Enter a Journey ID and click 'Load Journey Config' to begin.")
        else:
            st.info("👆 **Step 2**: Select customer attributes (if desired) and click 'Load Profile Data' to begin visualization.")
        return


    # Load profile data if not already loaded
    if st.session_state.profile_data is None:
        # Extract audience ID from stored API response
        try:
            api_response = st.session_state.api_response
            audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId')
            journey_id = api_response.get('data', {}).get('id')
            api_key = get_api_key()

            if audience_id and journey_id and api_key:
                profile_data = load_profile_data(journey_id, audience_id, api_key)
                if profile_data is not None and not profile_data.empty:
                    st.session_state.profile_data = profile_data
            else:
                st.warning("Missing required data for profile loading: audience_id, journey_id, or api_key")
        except Exception as e:
            st.warning(f"Could not load profile data: {str(e)}")

    # Initialize components
    try:
        column_mapper = CJOColumnMapper(st.session_state.api_response)

        # Handle profile data safely
        profile_data = st.session_state.profile_data
        if profile_data is None or profile_data.empty:
            profile_data = pd.DataFrame()

        generator = CJOFlowchartGenerator(st.session_state.api_response, profile_data)
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        return

    api_response = st.session_state.api_response

    # Journey information above tabs
    summary = generator.get_journey_summary()

    # Display journey information in a nice format
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Journey Name", summary['journey_name'])

    with col2:
        st.metric("Journey ID", summary['journey_id'])

    with col3:
        st.metric("Audience ID", summary['audience_id'])

    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["Step Browser", "Canvas", "Data & Mappings"])

    def _process_steps_from_root(steps, root_step_id, stage_idx, generator):
        """Process all steps from root following comprehensive CJO rules."""
        processed_steps = []
        visited_steps = set()

        def _get_step_profile_count(step_id, step_type=''):
            """Get profile count for a step using existing generator logic."""
            return generator._get_step_profile_count(step_id, stage_idx, step_type)

        def _get_uuid_short(uuid_str):
            """Get short version of UUID (first 8 characters)."""
            return uuid_str.split('-')[0] if uuid_str and '-' in uuid_str else uuid_str

        def _format_days_of_week(days_list):
            """Format days of the week list to proper display format."""
            day_names = {
                1: 'Mondays', 2: 'Tuesdays', 3: 'Wednesdays', 4: 'Thursdays',
                5: 'Fridays', 6: 'Saturdays', 7: 'Sundays'
            }
            day_display = [day_names.get(day, f'Day{day}') for day in days_list]
            return ', '.join(day_display)

        def _format_step_display_name(step_data, step_type, step_id):
            """Format step display name according to comprehensive CJO rules."""
            step_name = step_data.get('name', '')

            if step_type == 'Activation':
                return step_name or 'Activation'
            elif step_type == 'WaitStep':
                wait_step_type = step_data.get('waitStepType', 'Duration')
                if wait_step_type == 'Duration':
                    wait_step = step_data.get('waitStep', 1)
                    wait_unit = step_data.get('waitStepUnit', 'day')
                    # Handle plural forms
                    if wait_step > 1:
                        if wait_unit == 'day':
                            wait_unit = 'days'
                        elif wait_unit == 'hour':
                            wait_unit = 'hours'
                        elif wait_unit == 'minute':
                            wait_unit = 'minutes'
                    return f'Wait {wait_step} {wait_unit}'
                elif wait_step_type == 'Date':
                    wait_until_date = step_data.get('waitUntilDate', 'Unknown Date')
                    return f'Wait until {wait_until_date}'
                elif wait_step_type == 'DaysOfTheWeek':
                    days_list = step_data.get('waitUntilDaysOfTheWeek', [])
                    if days_list:
                        days_str = _format_days_of_week(days_list)
                        return f'Wait until {days_str}'
                    else:
                        return 'Wait until (No Days Specified)'
                elif wait_step_type == 'Condition':
                    return f'Wait Condition: {step_name}' if step_name else 'Wait Condition'
            elif step_type == 'DecisionPoint':
                return f'Decision Point ({_get_uuid_short(step_id)})'
            elif step_type == 'ABTest':
                return f'AB Test ({step_name})' if step_name else f'AB Test ({_get_uuid_short(step_id)})'
            elif step_type == 'Jump':
                return f'Jump: {step_name}' if step_name else 'Jump'
            elif step_type == 'End':
                return 'End'
            elif step_type == 'Merge':
                return f'Merge ({_get_uuid_short(step_id)})'
            else:
                return step_name or step_type

        def _create_step_info(step_id, step_data, step_type, display_name, profile_count=0, show_profiles=True):
            """Create standardized step info dictionary."""
            # Format final display with profile count if applicable
            if show_profiles and profile_count > 0:
                final_display = f"{display_name} ({profile_count} profiles)"
            else:
                final_display = display_name

            return {
                'step_id': step_id,
                'step_type': step_type,
                'stage_index': stage_idx,
                'profile_count': profile_count,
                'name': display_name,
                'display_name': final_display,
                'breadcrumbs': [display_name],
                'stage_entry_criteria': generator.stages[stage_idx].entry_criteria
            }, final_display

        def _create_step_display(step_id, step_data, step_type_override=None, name_override=None, profile_count_override=None):
            """Create step display info following the comprehensive rules."""
            step_type = step_type_override or step_data.get('type', 'Unknown')
            step_name = name_override or step_data.get('name', '')

            # Get profile count
            if profile_count_override is not None:
                profile_count = profile_count_override
            else:
                profile_count = _get_step_profile_count(step_id, step_type)

            # Generate display name based on step type
            display_name = step_name
            show_profile_count = True

            if step_type == 'WaitStep':
                wait_step_type = step_data.get('waitStepType', 'Duration')
                if wait_step_type == 'Duration':
                    wait_step = step_data.get('waitStep', 1)
                    wait_unit = step_data.get('waitStepUnit', 'day')
                    # Handle plural forms
                    if wait_step > 1:
                        if wait_unit == 'day':
                            wait_unit = 'days'
                        elif wait_unit == 'hour':
                            wait_unit = 'hours'
                        elif wait_unit == 'minute':
                            wait_unit = 'minutes'
                    display_name = f'Wait {wait_step} {wait_unit}'
                elif wait_step_type == 'Date':
                    wait_until_date = step_data.get('waitUntilDate', 'Unknown Date')
                    display_name = f'Wait Until {wait_until_date}'
                elif wait_step_type == 'DaysOfTheWeek':
                    days_list = step_data.get('waitUntilDaysOfTheWeek', [])
                    if days_list:
                        days_str = _format_days_of_week(days_list)
                        display_name = f'Wait Until {days_str}'
                    else:
                        display_name = 'Wait Until (No Days Specified)'
                elif wait_step_type == 'Condition':
                    # Wait Condition main step - show profile count
                    display_name = f'Wait: {step_name}' if step_name else 'Wait Condition'
            elif step_type == 'DecisionPoint':
                display_name = step_name or 'Decision Point'
                show_profile_count = False  # Decision points always show 0 profiles
            elif step_type == 'ABTest':
                display_name = step_name or 'AB Test'
                show_profile_count = False  # AB tests don't show profile count on main step
            elif step_type == 'Activation':
                display_name = step_name or 'Activation'
            elif step_type == 'Jump':
                display_name = step_name or 'Jump'
            elif step_type == 'End':
                display_name = 'End Step'
            elif step_type == 'Merge':
                display_name = step_name or 'Merge Step'
                show_profile_count = False  # Merge steps don't show profile count on grouping header

            # Format final display
            if show_profile_count and profile_count > 0:
                step_display = f"{display_name} ({profile_count} profiles)"
            else:
                step_display = display_name

            step_info = {
                'step_id': step_id,
                'step_type': step_type,
                'stage_index': stage_idx,
                'profile_count': profile_count,
                'name': display_name,
                'display_name': display_name,
                'breadcrumbs': [display_name],
                'stage_entry_criteria': generator.stages[stage_idx].entry_criteria
            }

            return (step_display, step_info)

        def _process_step(step_id, visited=None, indent_level=0):
            """Process a single step and its children recursively."""
            if visited is None:
                visited = set()

            if step_id in visited or step_id not in steps:
                return

            visited.add(step_id)
            step_data = steps[step_id]
            step_type = step_data.get('type', 'Unknown')

            if step_type == 'WaitStep' and step_data.get('waitStepType') == 'Condition':
                # Wait Condition: Show main step with profile count, then grouping headers for each condition
                display_name = _format_step_display_name(step_data, step_type, step_id)
                profile_count = _get_step_profile_count(step_id, step_type)
                step_info, final_display = _create_step_info(step_id, step_data, step_type, display_name, profile_count, True)
                processed_steps.append((final_display, step_info))

                # Add condition grouping headers
                wait_name = step_data.get('name', 'wait condition')
                conditions = step_data.get('conditions', [])
                for condition in conditions:
                    condition_name = condition.get('name', 'Unknown Condition')

                    # Format: "Wait Condition: <wait_name> - <condition_name>"
                    grouping_header = f"Wait Condition: {wait_name} - {condition_name}"

                    # Add empty line before grouping header for visual separation
                    empty_info = _create_step_info(f"empty_{step_id}_{condition.get('id', '')}", {}, 'EmptyLine', '', 0, False)
                    processed_steps.append(('', empty_info[0]))

                    # Add grouping header (no profile count)
                    group_info = _create_step_info(f"{step_id}_condition_header_{condition.get('id', '')}", condition, 'WaitCondition_Path_Header', grouping_header, 0, False)
                    processed_steps.append((grouping_header, group_info[0]))

                    # Process next step from this condition with indentation
                    next_step_id = condition.get('next')
                    if next_step_id:
                        _process_step(next_step_id, visited.copy(), indent_level + 1)

            elif step_type == 'DecisionPoint':
                # Decision Point: Show as "Decision Point (<uuid>)" then grouping headers for branches
                display_name = _format_step_display_name(step_data, step_type, step_id)
                step_info, final_display = _create_step_info(step_id, step_data, step_type, display_name, 0, False)
                processed_steps.append((final_display, step_info))

                # Process each branch with proper grouping headers
                branches = step_data.get('branches', [])
                for branch in branches:
                    # Create grouping header for each branch
                    if branch.get('excludedPath'):
                        branch_name = "Excluded Profiles"
                    else:
                        branch_name = branch.get('name', f"Branch {branch.get('segmentId', '')}")

                    # Format: "Decision (<uuid>): <branch_name>"
                    grouping_header = f"Decision ({_get_uuid_short(step_id)}): {branch_name}"

                    # Add empty line before grouping header for visual separation
                    empty_info = _create_step_info(f"empty_{step_id}_{branch.get('id', '')}", {}, 'EmptyLine', '', 0, False)
                    processed_steps.append(('', empty_info[0]))

                    # Add grouping header (no profile count)
                    group_info = _create_step_info(f"{step_id}_branch_header_{branch.get('id', '')}", branch, 'DecisionPoint_Branch_Header', grouping_header, 0, False)
                    processed_steps.append((grouping_header, group_info[0]))

                    # Process next step from this branch with indentation
                    next_step_id = branch.get('next')
                    if next_step_id:
                        _process_step(next_step_id, visited.copy(), indent_level + 1)

            elif step_type == 'ABTest':
                # AB Test: Show main activation step first, then variant grouping headers
                ab_test_name = step_data.get('name', 'AB Test')
                display_name = _format_step_display_name(step_data, step_type, step_id)
                step_info, final_display = _create_step_info(step_id, step_data, step_type, display_name, 0, False)
                processed_steps.append((final_display, step_info))

                # Process each variant with proper grouping headers
                variants = step_data.get('variants', [])
                for variant in variants:
                    variant_name = variant.get('name', 'Unknown Variant')
                    percentage = variant.get('percentage', 0)

                    # Format: "AB Test (<test_name>): <variant_name> (<percentage>%)"
                    grouping_header = f"AB Test ({ab_test_name}): {variant_name} ({percentage}%)"

                    # Add empty line before grouping header for visual separation
                    empty_info = _create_step_info(f"empty_{step_id}_{variant.get('id', '')}", {}, 'EmptyLine', '', 0, False)
                    processed_steps.append(('', empty_info[0]))

                    # Add grouping header (no profile count)
                    group_info = _create_step_info(f"{step_id}_variant_header_{variant.get('id', '')}", variant, 'ABTest_Variant_Header', grouping_header, 0, False)
                    processed_steps.append((grouping_header, group_info[0]))

                    # Process next step from this variant with indentation
                    next_step_id = variant.get('next')
                    if next_step_id:
                        _process_step(next_step_id, visited.copy(), indent_level + 1)

            elif step_type == 'Merge':
                # Merge step: Show as grouping header with proper format
                display_name = _format_step_display_name(step_data, step_type, step_id)

                # Add empty line before merge grouping header for visual separation
                empty_info = _create_step_info(f"empty_merge_{step_id}", {}, 'EmptyLine', '', 0, False)
                processed_steps.append(('', empty_info[0]))

                # Add merge grouping header (no profile count)
                step_info, final_display = _create_step_info(step_id, step_data, step_type, display_name, 0, False)
                processed_steps.append((final_display, step_info))

                # Process next step after merge with indentation
                next_step_id = step_data.get('next')
                if next_step_id:
                    _process_step(next_step_id, visited.copy(), indent_level + 1)

            else:
                # Regular steps (Activation, Jump, End, WaitStep - non-condition, etc.)
                display_name = _format_step_display_name(step_data, step_type, step_id)
                profile_count = _get_step_profile_count(step_id, step_type)

                # Apply proper indentation with -- prefix for steps following path-type steps
                if indent_level > 0:
                    final_display_name = f"-- {display_name}"
                else:
                    final_display_name = display_name

                step_info, final_display = _create_step_info(step_id, step_data, step_type, final_display_name, profile_count, True)
                processed_steps.append((final_display, step_info))

                # Process next step
                next_step_id = step_data.get('next')
                if next_step_id:
                    _process_step(next_step_id, visited.copy(), indent_level)

        # Start processing from root step
        _process_step(root_step_id)

        return processed_steps

    # Create unified step list using comprehensive rule-based logic
    def create_unified_step_list(generator):
        """Create a unified step list based on comprehensive CJO journey rules."""
        unified_steps = []

        for stage_idx, stage in enumerate(generator.stages):
            stage_data = generator.stages_data[stage_idx]
            steps = stage_data.get('steps', {})
            root_step_id = stage_data.get('rootStep')

            if not root_step_id or root_step_id not in steps:
                continue

            # Add stage header following comprehensive rules: "Stage #: <name> (Entry Criteria: <criteria>)"
            stage_name = stage_data.get('name', f'Stage {stage_idx + 1}')
            entry_criteria = stage_data.get('entryCriteria', {})
            entry_criteria_name = entry_criteria.get('name', 'No criteria specified')

            stage_header = f"Stage {stage_idx + 1}: {stage_name} (Entry Criteria: {entry_criteria_name})"
            stage_info = {
                'step_id': f"stage_header_{stage_idx}",
                'step_type': 'StageHeader',
                'stage_index': stage_idx,
                'profile_count': 0,
                'name': stage_header,
                'display_name': stage_header,
                'breadcrumbs': [stage_header],
                'stage_entry_criteria': entry_criteria_name
            }
            unified_steps.append((stage_header, stage_info))

            # Process steps following the "next" field navigation
            processed_steps = _process_steps_from_root(steps, root_step_id, stage_idx, generator)
            unified_steps.extend(processed_steps)

            # Add empty line after stage for visual separation (except for last stage)
            if stage_idx < len(generator.stages) - 1:
                empty_line_info = {
                    'step_id': f"empty_line_{stage_idx}",
                    'step_type': 'EmptyLine',
                    'stage_index': stage_idx,
                    'profile_count': 0,
                    'name': '',
                    'display_name': '',
                    'breadcrumbs': [''],
                    'stage_entry_criteria': entry_criteria_name
                }
                unified_steps.append(('', empty_line_info))

        return unified_steps

    all_steps = create_unified_step_list(generator)

    # Keep display names clean for dropdown selector (no HTML formatting)

    # Canvas logic is now used for both tabs - consistent data, different presentation

    # Tab 1: Step Selection (Default)
    with tab1:
        st.markdown("**Browse through all journey steps to view detailed information including profile counts, customer lists, and journey paths. Select any step from the list below to see which profiles are currently in that step and explore their journey progression.**")

        if all_steps:
            # Container 1: Journey Steps List
            with st.container():
                st.subheader("Journey Steps")

                # Add checkbox to filter steps with profiles
                filter_zero_profiles = st.checkbox("Only show steps with profiles", key="filter_zero_profiles")

                # Add CSS for step type colors in radio buttons and selectbox dropdown background
                st.markdown("""
                <style>
                /* Custom colors for radio button labels based on step types */
                .stRadio > div > div > div > label > div[data-testid="stMarkdownContainer"] {
                    font-weight: 500;
                }

                /* Selectbox dropdown background color */
                div[data-baseweb="popover"] {
                    background-color: #2f3037 !important;
                }

                div[data-baseweb="popover"] div[data-baseweb="menu"] {
                    background-color: #2f3037 !important;
                }

                div[data-baseweb="popover"] div[data-baseweb="menu"] ul {
                    background-color: #2f3037 !important;
                }

                div[data-baseweb="popover"] div[data-baseweb="menu"] li {
                    background-color: #2f3037 !important;
                }

                div[data-baseweb="popover"] [role="option"] {
                    background-color: #2f3037 !important;
                }

                /* Target popover at body level (Streamlit renders these at document root) */
                body div[data-baseweb="popover"] {
                    background-color: #2f3037 !important;
                }

                body div[data-baseweb="popover"] * {
                    background-color: #2f3037 !important;
                }

                /* Hover state - apply to all nested elements */
                div[data-baseweb="popover"] [role="option"]:hover,
                div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover {
                    background-color: #3a3a42 !important;
                }

                div[data-baseweb="popover"] [role="option"]:hover *,
                div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover * {
                    background-color: #3a3a42 !important;
                }

                /* More specific hover targeting */
                body div[data-baseweb="popover"] [role="option"]:hover,
                body div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover {
                    background-color: #3a3a42 !important;
                }

                body div[data-baseweb="popover"] [role="option"]:hover *,
                body div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover * {
                    background-color: #3a3a42 !important;
                }

                </style>
                """, unsafe_allow_html=True)

                # Define saturated colors for step types
                step_type_colors_saturated = {
                    'DecisionPoint': '#E6B800',        # More saturated yellow
                    'DecisionPoint_Branch': '#E6B800', # More saturated yellow
                    'ABTest': '#E6B800',               # More saturated yellow
                    'ABTest_Variant': '#E6B800',       # More saturated yellow
                    'WaitStep': '#CC0000',             # More saturated red
                    'Activation': '#006600',           # More saturated green
                    'Jump': '#0066CC',                 # More saturated blue
                    'End': '#0066CC',                  # More saturated blue
                    'Merge': '#0099CC',                # More saturated light blue
                    'Unknown': '#E6B800'               # More saturated yellow
                }

                # Create colored step display with individual breadcrumb coloring
                def format_step_with_colors(idx):
                    step_display, step_info = all_steps[idx]
                    breadcrumbs = step_info.get('breadcrumbs', [])

                    if len(breadcrumbs) <= 1:
                        # Single step, color the whole thing
                        step_type = step_info.get('step_type', 'Unknown')
                        color = step_type_colors_saturated.get(step_type, '#E6B800')
                        return step_display
                    else:
                        # Multiple breadcrumbs, need to color each part
                        stage_part = f"Stage {step_info['stage_index'] + 1}: "
                        breadcrumb_trail = " → ".join(breadcrumbs)
                        profile_part = f" ({step_info['profile_count']} profiles)"

                        # For now, use the final step's color for the whole line
                        # since we can't easily apply different colors to different parts in radio buttons
                        step_type = step_info.get('step_type', 'Unknown')
                        color = step_type_colors_saturated.get(step_type, '#E6B800')
                        return step_display

                # Add CSS to highlight profile counts in radio buttons
                st.markdown("""
                <style>
                /* Style radio button text to highlight profile counts */
                .stRadio label div[data-testid="stMarkdownContainer"] p {
                    font-family: inherit;
                }

                /* Custom style for steps with profiles - this is a workaround since we can't easily target specific text */
                .radio-with-profiles {
                    color: rgb(92, 228, 136) !important;
                }
                </style>
                """, unsafe_allow_html=True)

                # Simple step display function - formatting is now handled by comprehensive logic
                def format_step_display(idx):
                    step_display, step_info = all_steps[idx]
                    # Return the display text directly since it's already formatted
                    return step_display

                # Group steps by stage for better organization
                grouped_steps = {}
                for i, (step_display, step_info) in enumerate(all_steps):
                    stage_idx = step_info['stage_index']
                    if stage_idx not in grouped_steps:
                        grouped_steps[stage_idx] = []
                    grouped_steps[stage_idx].append((i, step_display, step_info))

                # Filter steps based on checkbox
                if filter_zero_profiles:
                    # Only show steps with profiles > 0
                    filtered_steps = []
                    for stage_idx in sorted(grouped_steps.keys()):
                        stage_steps = [item for item in grouped_steps[stage_idx] if item[2]['profile_count'] > 0 or item[2].get('is_empty_line', False)]
                        if stage_steps:  # Only include stage if it has steps with profiles
                            filtered_steps.extend(stage_steps)

                    if filtered_steps:
                        # Create options with stage headers
                        options_with_headers = []
                        current_stage = None

                        for original_idx, step_display, step_info in filtered_steps:
                            stage_idx = step_info['stage_index']
                            if stage_idx != current_stage:
                                # Add empty line before new stage (except for first stage)
                                if current_stage is not None:
                                    options_with_headers.append("")
                                current_stage = stage_idx
                            # Always use the pre-formatted step_display from unified formatter
                            options_with_headers.append(step_display)

                        # Create mapping that corresponds to options_with_headers
                        step_mapping = {}  # Map dropdown option to original index
                        for original_idx, step_display, step_info in filtered_steps:
                            # Map the step display text to its original index
                            step_mapping[step_display] = original_idx

                        # Use selectbox instead of radio for better header support
                        selected_option = st.selectbox(
                            "Select a step to view details:",
                            options=[""] + options_with_headers,
                            key="step_selector",
                            index=0
                        )

                        # Map back to original index
                        selected_idx = None

                        if selected_option and selected_option != "":
                            # User selected a step - get the index directly from mapping
                            selected_idx = step_mapping.get(selected_option)
                    else:
                        st.info("No steps with profiles found.")
                        selected_idx = None
                else:
                    # Show all steps with stage headers
                    options_with_headers = []
                    step_mapping = {}  # Map dropdown option to original index

                    for i, stage_idx in enumerate(sorted(grouped_steps.keys())):
                        # Add empty line before new stage (except for first stage)
                        if i > 0:
                            options_with_headers.append("")

                        # Add steps for this stage
                        for original_idx, step_display, step_info in grouped_steps[stage_idx]:
                            # Always use the pre-formatted step_display from unified formatter
                            options_with_headers.append(step_display)
                            # Map the step display text to its original index
                            step_mapping[step_display] = original_idx

                    # Use selectbox instead of radio for better header support
                    selected_option = st.selectbox(
                        "Select a step to view details:",
                        options=[""] + options_with_headers,
                        key="step_selector",
                        index=0
                    )

                    # Map back to original index
                    selected_idx = None

                    if selected_option and selected_option != "":
                        # User selected a step - get the index directly from mapping
                        selected_idx = step_mapping.get(selected_option)

                        # Show step details only
                        step_display, step_info = all_steps[selected_idx]

                        # Show step details for all selectable steps
                        step_type = step_info.get('step_type', '')

                        # Skip non-selectable elements
                        if step_type in ['EmptyLine', 'StageHeader']:
                            st.info("Please select an actual step to view details.")
                        elif step_type in ['DecisionPoint_Branch_Header', 'ABTest_Variant_Header', 'WaitCondition_Path_Header', 'DecisionPoint_Branch', 'ABTest_Variant', 'WaitCondition_Path']:
                            st.info("This is a grouping header. Please select a step below it to view profile details.")
                        else:

                            # Container 2b: Profiles in Step (moved up)
                            with st.container():
                                st.markdown("---")

                                # Try to find the corresponding column name
                                step_column = None

                                # For regular steps
                                if '_branch_' in step_info['step_id']:
                                    # Decision point branch
                                    parts = step_info['step_id'].split('_branch_')
                                    if len(parts) == 2:
                                        step_uuid = parts[0].replace('-', '_')
                                        segment_id = parts[1]
                                        step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
                                elif '_variant_' in step_info['step_id']:
                                    # AB test variant
                                    parts = step_info['step_id'].split('_variant_')
                                    if len(parts) == 2:
                                        step_uuid = parts[0].replace('-', '_')
                                        variant_uuid = parts[1].replace('-', '_')
                                        step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
                                else:
                                    # Regular step
                                    step_uuid = step_info['step_id'].replace('-', '_')
                                    step_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}"

                                if step_column:
                                    profiles = generator.get_profiles_in_step(step_column)

                                    if profiles:
                                        st.subheader("Profiles in this Step")

                                        # Add search functionality
                                        col1, col2, col3 = st.columns([3, 1, 4])
                                        with col1:
                                            search_term = st.text_input(
                                                "Search profile data:",
                                                placeholder="Search customer ID or any attribute...",
                                                key=f"search_{step_info['step_id']}",
                                                on_change=lambda: st.session_state.update({f"search_triggered_{step_info['step_id']}": True})
                                            )
                                        with col2:
                                            # Add some spacing to align with input
                                            st.write("")  # Empty line for alignment
                                            search_button = st.button(
                                                "🔍 Search",
                                                key=f"search_btn_{step_info['step_id']}",
                                                use_container_width=True
                                            )

                                        # Check for search trigger (Enter or button click)
                                        search_triggered = st.session_state.get(f"search_triggered_{step_info['step_id']}", False) or search_button
                                        if search_triggered:
                                            st.session_state[f"search_triggered_{step_info['step_id']}"] = False

                                        # Filter profiles if search term is provided and search is triggered
                                        if search_term and (search_triggered or search_button):
                                            # Get profile data with additional attributes for searching
                                            selected_attributes = st.session_state.get("selected_attributes", [])

                                            if selected_attributes and not generator.profile_data.empty:
                                                # Search across all columns in the profile data
                                                profile_data_subset = generator.profile_data[
                                                    generator.profile_data['cdp_customer_id'].isin(profiles)
                                                ]

                                                columns_to_search = ['cdp_customer_id'] + selected_attributes
                                                available_columns = [col for col in columns_to_search if col in profile_data_subset.columns]

                                                # Search across all available columns
                                                mask = pd.Series([False] * len(profile_data_subset))
                                                for col in available_columns:
                                                    mask = mask | profile_data_subset[col].astype(str).str.lower().str.contains(search_term.lower(), na=False)

                                                filtered_profile_data = profile_data_subset[mask]
                                                filtered_profiles = filtered_profile_data['cdp_customer_id'].tolist()
                                            else:
                                                # Fall back to searching just customer IDs
                                                filtered_profiles = [p for p in profiles if search_term.lower() in p.lower()]
                                        elif not search_term:
                                            filtered_profiles = profiles
                                        else:
                                            # Show all profiles if search hasn't been triggered yet
                                            filtered_profiles = profiles

                                        st.write(f"Showing {len(filtered_profiles)} of {len(profiles)} profiles")

                                        # Display profiles in a scrollable container
                                        if filtered_profiles:
                                            # Check if additional attributes are available
                                            selected_attributes = st.session_state.get("selected_attributes", [])

                                            if selected_attributes and not generator.profile_data.empty:
                                                # Get full profile data with additional attributes
                                                profile_data_subset = generator.profile_data[
                                                    generator.profile_data['cdp_customer_id'].isin(filtered_profiles)
                                                ]

                                                # Select columns to display
                                                columns_to_show = ['cdp_customer_id'] + selected_attributes
                                                available_columns = [col for col in columns_to_show if col in profile_data_subset.columns]

                                                if len(available_columns) > 1:  # More than just cdp_customer_id
                                                    profile_df = profile_data_subset[available_columns].copy()
                                                    st.write(f"**Showing profiles with {len(selected_attributes)} additional attributes:**")
                                                else:
                                                    profile_df = pd.DataFrame({'cdp_customer_id': filtered_profiles})
                                                    st.write("**Additional attributes not available in current data. Try reloading journey data.**")
                                            else:
                                                # Standard display with just customer IDs
                                                profile_df = pd.DataFrame({'cdp_customer_id': filtered_profiles})

                                            st.dataframe(profile_df, height=300)

                                            # Add download button
                                            csv = profile_df.to_csv(index=False)
                                            st.download_button(
                                                label="Download Profile Data",
                                                data=csv,
                                                file_name=f"profiles_{step_info['name'].replace(' ', '_')}.csv",
                                                mime="text/csv"
                                            )
                                        else:
                                            st.write("No profiles match the search criteria.")
                                    else:
                                        st.info("This step has no profiles to display.")

                            # Container 2c: Step Information (moved down)
                            with st.container():
                                st.markdown("---")
                                st.markdown("### 📊 Step Information")

                                st.write(f"**Step Type:** {step_info['step_type']}")

                                # Generate correct intime/outtime column names using the same logic as column_mapper
                                if '_branch_' in step_info['step_id']:
                                    # Decision point branch - format: intime_stage_{stage}_{step_uuid_with_underscores}_{segment_id}
                                    parts = step_info['step_id'].split('_branch_')
                                    if len(parts) == 2:
                                        step_uuid = parts[0].replace('-', '_')
                                        segment_id = parts[1]
                                        intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
                                        outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}_{segment_id}"
                                elif '_variant_' in step_info['step_id']:
                                    # AB test variant - format: intime_stage_{stage}_{step_uuid_with_underscores}_variant_{variant_uuid_with_underscores}
                                    parts = step_info['step_id'].split('_variant_')
                                    if len(parts) == 2:
                                        step_uuid = parts[0].replace('-', '_')
                                        variant_uuid = parts[1].replace('-', '_')
                                        intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
                                        outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}_variant_{variant_uuid}"
                                else:
                                    # Regular step - format: intime_stage_{stage}_{step_uuid_with_underscores}
                                    step_uuid = step_info['step_id'].replace('-', '_')
                                    intime_column = f"intime_stage_{step_info['stage_index']}_{step_uuid}"
                                    outtime_column = f"outtime_stage_{step_info['stage_index']}_{step_uuid}"

                                st.write("**Step UUID:**")
                                st.code(step_info['step_id'])

                                st.write("**Intime Column:**")
                                st.code(intime_column)

                                st.write("**Outtime Column:**")
                                st.code(outtime_column)

                                # Extract audience ID from session state
                                try:
                                    api_response = st.session_state.api_response
                                    audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId', 'YOUR_AUDIENCE_ID')
                                    journey_id = api_response.get('data', {}).get('id', 'YOUR_JOURNEY_ID')
                                except:
                                    audience_id = 'YOUR_AUDIENCE_ID'
                                    journey_id = 'YOUR_JOURNEY_ID'

                                # Generate SQL query based on step type
                                table_name = f"cdp_audience_{audience_id}.journey_{journey_id}"

                                sql_query = f"""SELECT cdp_customer_id
FROM {table_name}
WHERE {intime_column} IS NOT NULL
  AND {outtime_column} IS NULL;"""

                                st.write("**SQL Query:**")
                                st.code(sql_query, language="sql")
        else:
            st.info("No steps found in the journey data.")

    # Tab 2: Canvas (Journey Flowchart)
    with tab2:
        st.header("Journey Canvas")

        # Simple disclaimer
        st.info("ℹ️ **Note**: The canvas visualization works best with smaller, less complex journeys. For large or complex journeys, consider using the **Step Selection** tab.")

        # Generate flowchart button
        if st.button("🎨 Generate Canvas", type="primary", help="Click to generate the interactive flowchart"):
            try:
                with st.spinner("Generating interactive flowchart..."):
                    html_flowchart = create_flowchart_html(generator, column_mapper)

                # Add usage instructions above the flowchart
                st.info("💡 **Tip**: Click on any step to view profiles currently in the step.")

                # Display the HTML flowchart
                st.components.v1.html(html_flowchart, height=800, scrolling=True)

                # Simple success message
                st.success("✅ Flowchart generated successfully!")

            except Exception as e:
                st.error(f"Error creating flowchart: {str(e)}")
                st.write("**Debug Information:**")
                st.write(f"Number of stages: {len(generator.stages)}")
                st.write(f"Profile data shape: {profile_data.shape}")
                st.write(f"Profile data columns: {list(profile_data.columns)[:10]}...")  # Show first 10 columns

        else:
            # Show alternative instructions when flowchart is not generated
            st.info("""
            📊 **Canvas Features** (when generated):
            - Interactive visual flowchart of the entire journey
            - Color-coded step types for easy identification
            - Clickable step boxes that open popup modals
            - Real-time profile count display on each step
            - Hover tooltips with additional step details

            Click the button above to generate the visualization.
            """)


    # Tab 3: Data & Mappings
    with tab3:
        st.header("Data & Mappings")

        # Column mapping section
        st.subheader("Technical to Display Name Mappings")
        st.write("This shows how technical column names from the journey table are converted to human-readable display names.")

        # Show a sample of column mappings
        sample_columns = list(profile_data.columns)[:20]  # Show first 20 columns
        mappings = column_mapper.get_all_column_mappings(sample_columns)

        mapping_df = pd.DataFrame([
            {"Technical Name": tech, "Display Name": display}
            for tech, display in mappings.items()
        ])

        st.dataframe(mapping_df, height=400)

        # Raw data section
        st.subheader("Profile Data Preview")
        st.write("This shows a sample of the raw profile data from the journey table.")
        st.dataframe(profile_data.head(10))



if __name__ == "__main__":
    main()