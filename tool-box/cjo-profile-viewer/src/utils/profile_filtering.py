"""
Profile Filtering Utilities

Shared utilities for filtering step profiles consistently across all components.
This eliminates duplicate filtering logic between step selection, canvas, and flowchart generator.
"""

from typing import List
import pandas as pd


def get_step_column_name(step_id: str, stage_idx: int) -> str:
    """
    Generate step column name based on step ID and stage index.

    Args:
        step_id: The step UUID (may contain hyphens)
        stage_idx: The stage index number

    Returns:
        Column name in format: intime_stage_{stage_idx}_{step_uuid}
    """
    step_uuid = step_id.replace('-', '_')
    return f"intime_stage_{stage_idx}_{step_uuid}"


def create_step_profile_condition(profile_data: pd.DataFrame, step_column: str) -> pd.Series:
    """
    Create pandas condition for filtering profiles that are currently in a specific step.

    This applies the standard filtering logic:
    1. Profile has entered the step (intime_stage_N_stepuuid IS NOT NULL)
    2. Profile has not exited the step (outtime_stage_N_stepuuid IS NULL)
    3. Profile has not left the journey (outtime_journey IS NULL)

    Args:
        profile_data: DataFrame containing profile data
        step_column: The intime column name for the step

    Returns:
        Boolean Series for filtering profiles
    """
    # Base condition: profile has entered the step
    condition = profile_data[step_column].notna()

    # Exclude profiles that have exited this specific step
    step_outtime_column = step_column.replace('intime_', 'outtime_')
    if step_outtime_column in profile_data.columns:
        condition = condition & profile_data[step_outtime_column].isna()

    # Exclude profiles that have left the journey
    if 'outtime_journey' in profile_data.columns:
        condition = condition & profile_data['outtime_journey'].isna()

    return condition


def get_step_profiles(profile_data: pd.DataFrame, step_id: str, stage_idx: int) -> List[str]:
    """
    Get list of customer IDs for profiles currently in a specific step.

    Args:
        profile_data: DataFrame containing profile data
        step_id: The step UUID
        stage_idx: The stage index number

    Returns:
        List of customer IDs (cdp_customer_id values)
    """
    if profile_data.empty:
        return []

    step_column = get_step_column_name(step_id, stage_idx)
    if step_column not in profile_data.columns:
        return []

    condition = create_step_profile_condition(profile_data, step_column)
    return profile_data[condition]['cdp_customer_id'].tolist()


def get_step_profile_count(profile_data: pd.DataFrame, step_id: str, stage_idx: int) -> int:
    """
    Get count of profiles currently in a specific step.

    Args:
        profile_data: DataFrame containing profile data
        step_id: The step UUID
        stage_idx: The stage index number

    Returns:
        Number of profiles currently in the step
    """
    if profile_data.empty:
        return 0

    step_column = get_step_column_name(step_id, stage_idx)
    if step_column not in profile_data.columns:
        return 0

    condition = create_step_profile_condition(profile_data, step_column)
    return condition.sum()


def get_filtered_profile_data(profile_data: pd.DataFrame, step_id: str, stage_idx: int,
                             selected_attributes: List[str] = None) -> pd.DataFrame:
    """
    Get filtered profile data for profiles currently in a specific step.

    Args:
        profile_data: DataFrame containing profile data
        step_id: The step UUID
        stage_idx: The stage index number
        selected_attributes: List of additional attributes to include

    Returns:
        Filtered DataFrame with profiles currently in the step
    """
    if profile_data.empty:
        return pd.DataFrame()

    step_column = get_step_column_name(step_id, stage_idx)
    if step_column not in profile_data.columns:
        return pd.DataFrame()

    condition = create_step_profile_condition(profile_data, step_column)
    filtered_data = profile_data[condition]

    if selected_attributes:
        # Include cdp_customer_id and selected attributes
        columns_to_show = ['cdp_customer_id'] + [attr for attr in selected_attributes
                                                 if attr in filtered_data.columns]
        if len(columns_to_show) > 1:
            return filtered_data[columns_to_show].copy()

    # Default: just return customer IDs
    return filtered_data[['cdp_customer_id']].copy()