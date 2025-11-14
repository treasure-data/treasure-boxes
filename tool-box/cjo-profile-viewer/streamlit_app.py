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

from column_mapper import CJOColumnMapper
from flowchart_generator import CJOFlowchartGenerator


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

            # Construct the query for live profile data
            table_name = f"cdp_audience_{audience_id}.journey_{journey_id}"
            query = f"SELECT * FROM {table_name}"

            st.info(f"Querying table: {table_name}")

            # Execute the query and return as DataFrame
            query_result = client.query(query)

            # Convert the result to a pandas DataFrame
            if not query_result.get('data'):
                st.warning(f"No data found in table {table_name}")
                return pd.DataFrame()

            profile_data = pd.DataFrame(query_result['data'], columns=query_result['columns'])

            return profile_data

    except Exception as e:
        error_msg = str(e)
        st.error(f"Error querying live profile data: {error_msg}")

        # Provide helpful error messages for common issues
        if "Table not found" in error_msg or "does not exist" in error_msg:
            st.error(f"Table 'cdp_audience_{audience_id}.journey_{journey_id}' does not exist. Please verify the audience ID and journey ID.")
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
        'Activation': '#d8f3ed',           # Activation - light green
        'Jump': '#e8eaff',                 # Jump - light blue/purple
        'End': '#e8eaff',                  # End Step - light blue/purple
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
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0,0,0,0.9);
        color: white;
        padding: 8px;
        border-radius: 4px;
        font-size: 10px;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s;
        z-index: 1000;
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
        width: 80%;
        max-width: 600px;
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

            # Process each step in the path
            for step_idx, step in enumerate(path):
                # Get color for step type
                step_color = step_type_colors.get(step.step_type, step_type_colors['Unknown'])

                # Create step name (truncate if too long)
                step_name = step.name[:25] + "..." if len(step.name) > 25 else step.name

                # Create tooltip info
                tooltip = f"Type: {step.step_type} | Stage: {stage_idx} | ID: {step.step_id}"

                # Determine the count text based on step type
                if step.step_type in ['DecisionPoint_Branch', 'ABTest_Variant']:
                    # For groupings, show "Total Profiles: X" instead of "In Step: X"
                    count_text = f"Total Profiles: {step.profile_count}"
                else:
                    # For actual steps, show "In Step: X"
                    count_text = f"In Step: {step.profile_count}"

                # Get profiles for this step
                step_profiles = _get_step_profiles(generator, step)

                # Store step data for JavaScript access
                step_data_key = f"step_{stage_idx}_{path_idx}_{step_idx}"
                step_data_store[step_data_key] = {
                    'name': step.name,
                    'profiles': step_profiles
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

                # Add arrow if not the last step
                if step_idx < len(path) - 1:
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

    function showProfileModal(stepDataKey) {{
        const stepData = stepDataStore[stepDataKey];
        if (!stepData) {{
            console.error('Step data not found for key:', stepDataKey);
            return;
        }}

        const stepName = stepData.name;
        const profiles = stepData.profiles;

        allProfiles = profiles;
        currentProfiles = profiles;

        document.getElementById('modalTitle').textContent = stepName;
        document.getElementById('profileCountInfo').innerHTML =
            `<strong>Total Profiles:</strong> ${{profiles.length}}`;

        document.getElementById('searchBox').value = '';
        displayProfiles(profiles);
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
            currentProfiles = allProfiles.filter(profile =>
                profile.toLowerCase().includes(searchTerm)
            );
        }}

        displayProfiles(currentProfiles);
    }}

    function displayProfiles(profiles) {{
        const profilesList = document.getElementById('profilesList');

        if (profiles.length === 0) {{
            profilesList.innerHTML = '<div class="no-profiles">No profiles found</div>';
            return;
        }}

        let html = '';
        profiles.forEach(profile => {{
            html += `<div class="profile-item">${{profile}}</div>`;
        }});

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


def show_step_details(step_info: Dict, generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Show detailed information about a selected step."""
    st.subheader(f"Step Details: {step_info['name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Step Type:** {step_info['step_type']}")
        st.write(f"**Stage Index:** {step_info['stage_index']}")
        st.write(f"**Profiles in Step:** {step_info['profile_count']}")

    with col2:
        st.write(f"**Step ID:** {step_info['step_id']}")

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
    </style>
    """, unsafe_allow_html=True)

    st.title("🔍 CJO Profile Viewer")
    st.markdown("**Visualize Customer Journey Orchestration journeys with profile data**")

    # Check for existing API key
    existing_api_key = get_api_key()
    api_key_status = "✅ Found" if existing_api_key else "❌ Not Found"

    # Initialize session state for data
    if 'api_response' not in st.session_state:
        st.session_state.api_response = None
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
    if 'journey_loaded' not in st.session_state:
        st.session_state.journey_loaded = False

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

    # Sidebar Section
    with st.sidebar:
        # Journey ID input
        journey_id = st.text_input(
            "Journey ID",
            placeholder="e.g., 211205",
            key="sidebar_journey_id",
            on_change=lambda: st.session_state.update({"auto_load_triggered": True})
        )

        load_button = st.button(
            "🔄 Load Journey Data",
            type="primary",
            disabled=not journey_id,
            key="sidebar_load_button"
        )

        # Add spacer to push configuration to bottom
        st.markdown("<br>" * 20, unsafe_allow_html=True)

        # Configuration section at very bottom
        st.header("⚙️ Configuration")

        # Show setup instructions only if API key not found
        if not existing_api_key:
            st.error(f"""
            **TD API Key Status:** {api_key_status}

            **Setup Instructions:**
            1. **Environment Variable:** Set `TD_API_KEY`
            2. **Config File:** `~/.td/config`
            3. **Local File:** `td_config.txt`

            **Get your API key:** TD Console → Profile → API Keys
            """)
        else:
            st.success(f"**TD API Key Status:** {api_key_status}")

    # Check for auto-load trigger (when user presses Enter)
    auto_load_triggered = st.session_state.get("auto_load_triggered", False)
    if auto_load_triggered and journey_id:
        st.session_state["auto_load_triggered"] = False
        load_button = True  # Trigger the loading logic

    # Handle data loading
    if load_button and journey_id:
        if not existing_api_key:
            st.error("❌ **API Key Required**: Please set up your TD API key using one of the methods above.")
            return

        # Fetch journey data
        api_response, error = fetch_journey_data(journey_id, existing_api_key)

        if error:
            st.error(f"❌ **API Error**: {error}")
            return

        if api_response:
            st.session_state.api_response = api_response
            st.session_state.journey_loaded = True

            # Extract audience ID from API response
            audience_id = None
            try:
                audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId')
                if not audience_id:
                    st.error("❌ **API Response Error**: Audience ID not found in API response")
                    return
            except Exception as e:
                st.error(f"❌ **API Response Error**: Failed to extract audience ID: {str(e)}")
                return

            # Load profile data using pytd
            profile_data = load_profile_data(journey_id, audience_id, existing_api_key)
            if profile_data is not None:
                st.session_state.profile_data = profile_data
                st.success(f"✅ **Success**: Journey '{journey_id}' data loaded successfully!")
            else:
                st.warning("⚠️ **Profile Data**: Could not load profile data. Some features may be limited.")

    # Check if we have data to work with
    if not st.session_state.journey_loaded or st.session_state.api_response is None:
        st.info("👆 **Get Started**: Enter a Journey ID and click 'Load Journey Data' to begin visualization.")
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
    tab1, tab2, tab3 = st.tabs(["Step Selection", "Canvas", "Data & Mappings"])

    # Create list of all steps (used by both tabs)
    all_steps = []
    for stage in generator.stages:
        for path in stage.paths:
            for step in path:
                step_display = f"Stage {step.stage_index}: {step.name} ({step.profile_count} profiles)"
                all_steps.append((step_display, {
                    'step_id': step.step_id,
                    'step_type': step.step_type,
                    'stage_index': step.stage_index,
                    'profile_count': step.profile_count,
                    'name': step.name
                }))

    # Tab 1: Step Selection (Default)
    with tab1:
        st.header("Step Selection")

        if all_steps:
            selected_step_display = st.selectbox(
                "Select a step to view details:",
                options=["None"] + [step[0] for step in all_steps],
                index=0,
                key="step_selector"
            )

            if selected_step_display != "None":
                # Find the corresponding step info
                for step_display, step_info in all_steps:
                    if step_display == selected_step_display:
                        show_step_details(step_info, generator, column_mapper)
                        break
        else:
            st.info("No steps found in the journey data.")

    # Tab 2: Canvas (Journey Flowchart)
    with tab2:
        st.header("Journey Canvas")

        # Simple disclaimer
        st.info("ℹ️ **Note**: The canvas visualization works best with smaller, less complex journeys. For large or complex journeys, consider using the **Step Selection** tab for better performance.")

        # Generate flowchart button
        if st.button("🎨 Generate Canvas Visualization", type="primary", help="Click to generate the interactive flowchart"):
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

        st.subheader("API Response Summary")
        st.write("This shows the key information from the journey API response.")
        st.json({
            "journey_id": summary['journey_id'],
            "journey_name": summary['journey_name'],
            "stages": [{"name": stage.name, "id": stage.stage_id} for stage in generator.stages]
        })


if __name__ == "__main__":
    main()