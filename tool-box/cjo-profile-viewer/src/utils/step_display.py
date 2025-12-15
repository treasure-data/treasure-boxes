"""
Step Display Utilities

Shared utilities for calculating step display names consistently across components.
"""

from typing import Dict


def get_step_display_name(step_data: Dict) -> str:
    """
    Get display name for a step based on its type.

    This function provides consistent step naming logic used by both
    the flowchart generator and the step selection dropdown.

    Args:
        step_data: Dictionary containing step configuration data

    Returns:
        Human-readable display name for the step
    """
    step_type = step_data.get('type', 'Unknown')

    if step_type == 'WaitStep':
        return _get_wait_step_display_name(step_data)
    elif step_type == 'Activation':
        return step_data.get('name', 'Activation')
    elif step_type == 'Jump':
        return step_data.get('name', 'Jump')
    elif step_type == 'End':
        return 'End Step'
    elif step_type == 'DecisionPoint':
        return 'Decision Point'
    elif step_type == 'ABTest':
        return step_data.get('name', 'AB Test')
    elif step_type == 'Merge':
        return step_data.get('name', 'Merge Step')
    else:
        return step_data.get('name', step_type)


def _get_wait_step_display_name(step_data: Dict) -> str:
    """
    Get display name for WaitStep type with specific wait logic.

    Args:
        step_data: Dictionary containing wait step configuration

    Returns:
        Formatted wait step display name
    """
    wait_step_type = step_data.get('waitStepType', 'Duration')

    if wait_step_type == 'Condition':
        step_name = step_data.get('name', 'Unknown Condition')
        return f'Wait: {step_name}'

    elif wait_step_type == 'Date':
        wait_until_date = step_data.get('waitUntilDate', 'Unknown Date')
        return f'Wait Until {wait_until_date}'

    elif wait_step_type == 'DaysOfTheWeek':
        days_of_week = step_data.get('waitUntilDaysOfTheWeek', [])
        if days_of_week:
            # Map day numbers to day names (1=Monday, 2=Tuesday, etc.)
            day_names = {
                1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday', 7: 'Sunday'
            }
            day_list = [day_names.get(day, f'Day{day}') for day in days_of_week]
            days_str = ', '.join(day_list)
            return f'Wait Until {days_str}'
        else:
            return 'Wait Until (No Days Specified)'

    else:
        # Duration-based wait step (default/legacy)
        wait_step = step_data.get('waitStep', 1)
        wait_unit = step_data.get('waitStepUnit', 'day')
        return f'Wait {wait_step} {wait_unit}'