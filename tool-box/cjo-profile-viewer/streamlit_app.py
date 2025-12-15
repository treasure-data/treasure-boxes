"""
CJO Profile Viewer - Streamlit Application (Refactored)

A tool for visualizing Customer Journey Orchestration (CJO) journeys with profile data.
This refactored version uses modular components for better maintainability.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional

# Import refactored modules
from src.services.td_api import TDAPIService
from src.column_mapper import CJOColumnMapper
from src.flowchart_generator import CJOFlowchartGenerator
from src.components.flowchart_renderer import create_flowchart_html
from src.styles import load_all_styles
from src.utils.session_state import SessionStateManager
from src.utils.step_display import get_step_display_name


def render_configuration_panel():
    """Render the journey configuration input panel."""
    st.header("🔧 Journey Configuration")

    with st.container():
        col1, col2 = st.columns([2, 1])

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

        return journey_id, load_config_button


def render_attribute_selector():
    """Render the customer attribute selection interface."""
    load_profile_button = False

    if SessionStateManager.is_config_loaded():
        st.markdown("**Step 2: Select Additional Customer Attributes**")
        st.caption("Select additional customer attributes to include when viewing step profiles. cdp_customer_id is included by default.")

        try:
            audience_id = SessionStateManager.get_audience_id()
            if audience_id:
                available_attributes = SessionStateManager.get_available_attributes(audience_id)

                if available_attributes:
                    selected_attributes = st.multiselect(
                        "Select customer attributes:",
                        options=available_attributes,
                        default=SessionStateManager.get("selected_attributes", []),
                        key="attribute_selector",
                        help="These attributes will be joined from the customers table",
                        label_visibility="collapsed"
                    )

                    # Store selected attributes in session state
                    SessionStateManager.set("selected_attributes", selected_attributes)

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
        except Exception as e:
            st.warning(f"Could not load customer attributes: {str(e)}")
    else:
        st.caption("Load journey configuration first to see available customer attributes.")

    return load_profile_button


def handle_config_loading(journey_id: str, load_config_button: bool, api_service: TDAPIService):
    """Handle the journey configuration loading process."""
    # Check for auto-load trigger (when user presses Enter)
    auto_load_triggered = SessionStateManager.get("auto_load_triggered", False)
    if auto_load_triggered and journey_id:
        SessionStateManager.set("auto_load_triggered", False)
        load_config_button = True  # Trigger the loading logic

    # Handle Step 1: Load Journey Configuration
    if load_config_button:
        if not journey_id or journey_id.strip() == "":
            st.toast("Please enter a Journey ID", icon="⚠️")
            st.stop()

        if not api_service.api_key:
            st.error("❌ **API Key Required**: Please set up your TD API key (TD_API_KEY environment variable, ~/.td/config, or td_config.txt file)")
            st.stop()

        # Fetch journey data
        api_response, error = api_service.fetch_journey_data(journey_id)

        if error:
            st.toast(f"API Error: {error}", icon="❌", duration=30)
            st.stop()

        if api_response:
            # Extract audience ID from API response
            try:
                audience_id = api_response.get('data', {}).get('attributes', {}).get('audienceId')
                if not audience_id:
                    st.error("❌ **API Response Error**: Audience ID not found in API response")
                    st.stop()
            except Exception as e:
                st.error(f"❌ **API Response Error**: Failed to extract audience ID: {str(e)}")
                st.stop()

            # Load available customer attributes
            available_attributes = api_service.get_available_attributes(audience_id)

            # Store configuration in session state
            SessionStateManager.set_config_loaded(api_response, audience_id, available_attributes)

            st.toast(f"Journey configuration for '{journey_id}' loaded successfully! Now select attributes and load profile data.", icon="✅")
            st.rerun()


def handle_profile_loading(load_profile_button: bool, api_service: TDAPIService):
    """Handle the profile data loading process."""
    if load_profile_button:
        if not SessionStateManager.is_config_loaded():
            st.toast("Please load journey configuration first", icon="⚠️")
            st.stop()

        if not api_service.api_key:
            st.error("❌ **API Key Required**: Please set up your TD API key")
            st.stop()

        # Get journey and audience info from session state
        journey_id = SessionStateManager.get_journey_id()
        audience_id = SessionStateManager.get_audience_id()

        if not journey_id or not audience_id:
            st.error("❌ Missing journey or audience ID from configuration")
            st.stop()

        # Get selected attributes
        selected_attributes = SessionStateManager.get("selected_attributes", [])

        # Load profile data
        profile_data = api_service.load_profile_data(journey_id, audience_id, selected_attributes)
        if profile_data is not None:
            SessionStateManager.set_profile_loaded(profile_data)
            st.toast(f"Profile data loaded successfully! {len(profile_data)} profiles found.", icon="✅")
        else:
            st.toast("Could not load profile data. Some features may be limited.", icon="⚠️")

        st.rerun()


def render_journey_tabs():
    """Render the main journey visualization tabs."""
    if not SessionStateManager.is_journey_loaded():
        if not SessionStateManager.is_config_loaded():
            st.info("👆 **Step 1**: Enter a Journey ID and click 'Load Journey Config' to begin.")
        else:
            st.info("👆 **Step 2**: Select customer attributes (if desired) and click 'Load Profile Data' to begin visualization.")
        return

    # Initialize components
    try:
        api_response = SessionStateManager.get('api_response')
        profile_data = SessionStateManager.get('profile_data')

        column_mapper = CJOColumnMapper(api_response)

        # Handle profile data safely
        if profile_data is not None and not profile_data.empty:
            flowchart_generator = CJOFlowchartGenerator(api_response, profile_data)
        else:
            # Create generator with empty DataFrame
            flowchart_generator = CJOFlowchartGenerator(api_response, pd.DataFrame())
            st.warning("⚠️ Profile data is empty or unavailable. Some features may be limited.")

    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        return

    # Create tabs
    step_tab, canvas_tab, data_tab = st.tabs(["📋 Step Selection", "🎨 Canvas", "📊 Data & Mappings"])

    with step_tab:
        render_step_selection_tab(flowchart_generator, column_mapper)

    with canvas_tab:
        render_canvas_tab(flowchart_generator, column_mapper)

    with data_tab:
        render_data_tab(flowchart_generator, column_mapper)


def render_step_selection_tab(generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Render the step selection tab."""
    st.subheader("Step Selection & Profile View")

    if generator.profile_data.empty:
        st.warning("No profile data available. Please load profile data to use this feature.")
        return

    # Get all steps for dropdown using the stages_data property
    stages_data = generator.stages_data
    if not stages_data:
        st.warning("No steps found in the journey configuration.")
        return

    # Add helpful description
    st.markdown("**How to use:** First select a stage from the journey, then choose a specific step within that stage to view profile details.")

    # Create two-column layout for stage and step selection
    col1, col2 = st.columns(2)

    with col1:
        # Stage selector
        stage_options = {}
        for stage_idx, stage_data in enumerate(stages_data):
            stage_name = stage_data.get('name', f'Stage {stage_idx + 1}')
            stage_options[stage_name] = {
                'idx': stage_idx,
                'name': stage_name,
                'data': stage_data
            }

        if not stage_options:
            st.warning("No stages available for selection.")
            return

        selected_stage_name = st.selectbox(
            "1. Select a stage:",
            options=list(stage_options.keys()),
            key="stage_selector",
            index=0,  # Default to first stage
            help="Choose a stage from the customer journey"
        )

        # Show stage info
        if selected_stage_name:
            selected_stage = stage_options[selected_stage_name]
            stage_data = selected_stage['data']
            steps_count = len(stage_data.get('steps', {}))
            st.caption(f"Stage has {steps_count} step{'s' if steps_count != 1 else ''}")

    with col2:
        # Step selector (updates based on selected stage)
        if selected_stage_name:
            selected_stage = stage_options[selected_stage_name]
            stage_idx = selected_stage['idx']
            stage_data = selected_stage['data']
            steps = stage_data.get('steps', {})

            if not steps:
                st.warning("No steps found in the selected stage.")
                return

            # Create step options for the selected stage
            step_options = {}
            for step_id, step_data in steps.items():
                # Use shared utility for consistent step naming (without stage name prefix)
                step_name = get_step_display_name(step_data)
                step_type = step_data.get('type', 'Unknown')

                # Create step info dict
                step_info = {
                    'id': step_id,
                    'name': step_name,
                    'type': step_type,
                    'stage_idx': stage_idx,
                    'stage_name': selected_stage_name
                }
                step_options[step_name] = step_info

            selected_step_name = st.selectbox(
                "2. Select a step:",
                options=list(step_options.keys()),
                key=f"step_selector_{stage_idx}",  # Unique key per stage
                help="Choose a specific step to view customer profiles"
            )

            # Show step type info and render details
            if selected_step_name:
                selected_step = step_options[selected_step_name]
                step_type = selected_step.get('type', 'Unknown')
                st.caption(f"Step type: {step_type}")

                st.markdown("---")
                render_step_details(selected_step, generator, column_mapper)


def get_step_column_name(step_id: str, stage_idx: int) -> str:
    """Generate step column name based on step ID and stage index."""
    # Convert step_id with hyphens to underscore format for column names
    step_uuid = step_id.replace('-', '_')
    return f"intime_stage_{stage_idx}_{step_uuid}"


def render_step_details(step_info: Dict, generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Render details for a selected step."""
    step_name = step_info.get('name', 'Unknown Step')
    step_type = step_info.get('type', 'Unknown')
    step_id = step_info.get('id', '')
    stage_idx = step_info.get('stage_idx', 0)

    # Display step information
    st.markdown(f"**Step:** {step_name}")
    st.markdown(f"**Type:** {step_type}")
    if step_id:
        st.markdown(f"**ID:** {step_id}")

    # Get profiles for this step
    try:
        step_column = get_step_column_name(step_id, stage_idx)
        if step_column not in generator.profile_data.columns:
            st.warning("No profile data available for this step.")
            return

        step_profiles = generator.profile_data[
            generator.profile_data[step_column].notna()
        ]['cdp_customer_id'].tolist()

        st.markdown(f"**Profile Count:** {len(step_profiles)}")

        if step_profiles:
            # Show profiles with search functionality
            search_term = st.text_input("Filter profiles by customer ID:", key=f"search_{step_id}")

            if search_term:
                filtered_profiles = [p for p in step_profiles if search_term.lower() in str(p).lower()]
            else:
                filtered_profiles = step_profiles

            st.write(f"Showing {len(filtered_profiles)} of {len(step_profiles)} profiles")

            # Display profiles
            if filtered_profiles:
                selected_attributes = SessionStateManager.get("selected_attributes", [])

                if selected_attributes and not generator.profile_data.empty:
                    # Show full profile data with additional attributes
                    profile_subset = generator.profile_data[
                        generator.profile_data['cdp_customer_id'].isin(filtered_profiles)
                    ]

                    columns_to_show = ['cdp_customer_id'] + selected_attributes
                    available_columns = [col for col in columns_to_show if col in profile_subset.columns]

                    if len(available_columns) > 1:
                        profile_df = profile_subset[available_columns].copy()
                        st.dataframe(profile_df, use_container_width=True)

                        # Download button
                        csv = profile_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name=f"step_{step_id}_profiles.csv",
                            mime="text/csv"
                        )
                    else:
                        st.write("Additional attributes not available in current data.")
                else:
                    # Simple profile list
                    profile_df = pd.DataFrame({'cdp_customer_id': filtered_profiles})
                    st.dataframe(profile_df, use_container_width=True)

                    # Download button
                    csv = profile_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"step_{step_id}_profiles.csv",
                        mime="text/csv"
                    )

    except Exception as e:
        st.error(f"Error loading step details: {str(e)}")


def render_canvas_tab(generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Render the canvas (flowchart) tab."""
    st.subheader("Interactive Journey Flowchart")

    if generator.profile_data.empty:
        st.warning("Profile data is not available. The flowchart will show journey structure without profile counts.")

    # Performance note
    st.info("💡 **Performance Note**: For better performance with large journeys, consider using the Step Selection tab for detailed analysis.")

    # Generate button
    if st.button("🎨 Generate Canvas Visualization", type="primary"):
        with st.spinner("Generating interactive flowchart..."):
            try:
                flowchart_html = create_flowchart_html(generator, column_mapper)
                st.components.v1.html(flowchart_html, height=800, scrolling=True)
            except Exception as e:
                st.error(f"Error generating flowchart: {str(e)}")
    else:
        st.info("Click the button above to generate the interactive flowchart visualization.")


def render_data_tab(generator: CJOFlowchartGenerator, column_mapper: CJOColumnMapper):
    """Render the data and mappings tab."""
    st.subheader("Data & Mappings")

    # Journey API Response Summary
    st.markdown("### 📋 Journey Configuration")
    api_response = SessionStateManager.get('api_response')
    if api_response:
        journey_summary = generator.get_journey_summary()
        st.json({
            "journey_id": journey_summary.get('journey_id'),
            "journey_name": journey_summary.get('journey_name'),
            "audience_id": journey_summary.get('audience_id'),
            "stages_count": len(journey_summary.get('stages', [])),
            "total_profiles": journey_summary.get('total_profiles', 0)
        })

    # Column Mappings
    st.markdown("### 🗂️ Column Mappings")
    st.caption("Technical column names → Display names")

    profile_data = SessionStateManager.get('profile_data')
    if profile_data is not None and not profile_data.empty:
        # Show sample of column mappings
        sample_columns = profile_data.columns.tolist()[:10]
        mapping_data = []
        for col in sample_columns:
            display_name = column_mapper.map_column_to_display_name(col)
            mapping_data.append({
                "Technical Name": col,
                "Display Name": display_name
            })

        st.dataframe(pd.DataFrame(mapping_data), use_container_width=True)

        # Profile Data Preview
        st.markdown("### 📊 Profile Data Preview")
        st.caption(f"Showing first 5 rows of {len(profile_data)} total profiles")
        st.dataframe(profile_data.head(), use_container_width=True)

        # Data Info
        st.markdown("### ℹ️ Data Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Profiles", len(profile_data))
        with col2:
            st.metric("Total Columns", len(profile_data.columns))
        with col3:
            st.metric("Selected Attributes", len(SessionStateManager.get("selected_attributes", [])))
    else:
        st.info("Load profile data to see column mappings and data preview.")


def main():
    """Main application function."""
    st.set_page_config(
        page_title="CJO Profile Viewer",
        page_icon="🎯",
        layout="wide"
    )

    # Load styles
    load_all_styles()

    # Initialize session state
    SessionStateManager.initialize()

    # Initialize API service
    api_service = TDAPIService()

    st.title("🎯 CJO Profile Viewer")
    st.markdown("Visualize Customer Journey Orchestration journeys with profile data")

    # Render configuration panel
    journey_id, load_config_button = render_configuration_panel()

    # Render attribute selector
    load_profile_button = render_attribute_selector()

    # Handle button clicks
    handle_config_loading(journey_id, load_config_button, api_service)
    handle_profile_loading(load_profile_button, api_service)

    st.markdown("---")

    # Render main content
    render_journey_tabs()


if __name__ == "__main__":
    main()