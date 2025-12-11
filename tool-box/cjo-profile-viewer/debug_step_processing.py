#!/usr/bin/env python3

"""
Debug test to check if the new step processing logic works correctly
"""

import pandas as pd
import json

# Test data structure
test_api_response = {
    'data': {
        'id': 'test_journey',
        'attributes': {
            'name': 'Test Journey',
            'audienceId': 'test_audience',
            'journeyStages': [
                {
                    'id': 'stage1',
                    'name': 'Test Stage 1',
                    'rootStep': 'step1',
                    'steps': {
                        'step1': {
                            'type': 'WaitStep',
                            'name': 'Wait 2 days',
                            'waitStep': 2,
                            'waitStepUnit': 'day',
                            'waitStepType': 'Duration',
                            'next': 'step2'
                        },
                        'step2': {
                            'type': 'End',
                            'name': 'End Step'
                        }
                    }
                }
            ]
        }
    }
}

# Test profile data
test_profile_data = pd.DataFrame({
    'cdp_customer_id': ['cust1', 'cust2', 'cust3'],
    'intime_stage_0_step1': [1, 1, None],
    'outtime_stage_0_step1': [None, 1, None]
})

def _process_steps_from_root_test(steps, root_step_id, stage_idx, generator):
    """Test version of the step processing function with debug output."""
    print(f"Processing steps from root: {root_step_id}")
    print(f"Available steps: {list(steps.keys())}")

    processed_steps = []

    def _get_step_profile_count(step_id, step_type=''):
        """Get profile count for a step using existing generator logic."""
        count = generator._get_step_profile_count(step_id, stage_idx, step_type)
        print(f"Profile count for {step_id}: {count}")
        return count

    def _create_step_display(step_id, step_data, step_type_override=None, name_override=None, profile_count_override=None):
        """Create step display info following the comprehensive rules."""
        print(f"Creating step display for: {step_id}, type: {step_data.get('type')}")

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
        elif step_type == 'End':
            display_name = 'End Step'

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

        print(f"Created step display: '{step_display}'")
        return (step_display, step_info)

    def _process_step(step_id, visited=None, indent_level=0):
        """Process a single step and its children recursively."""
        if visited is None:
            visited = set()

        print(f"Processing step: {step_id}, visited: {visited}")

        if step_id in visited or step_id not in steps:
            print(f"Skipping {step_id} - already visited or not found")
            return

        visited.add(step_id)
        step_data = steps[step_id]
        step_type = step_data.get('type', 'Unknown')

        print(f"Step {step_id} type: {step_type}")

        if step_type in ['WaitStep', 'Activation', 'Jump', 'End']:
            # Regular steps
            regular_step = _create_step_display(step_id, step_data)
            processed_steps.append(regular_step)

            # Process next step
            next_step_id = step_data.get('next')
            if next_step_id:
                print(f"Following next step: {next_step_id}")
                _process_step(next_step_id, visited.copy(), indent_level)
            else:
                print(f"No next step for {step_id}")

    # Start processing from root step
    print(f"Starting processing from root: {root_step_id}")
    _process_step(root_step_id)

    print(f"Final processed steps count: {len(processed_steps)}")
    for i, (display, info) in enumerate(processed_steps):
        print(f"  {i+1}. {display}")

    return processed_steps

try:
    from flowchart_generator import CJOFlowchartGenerator

    print("Creating generator...")
    generator = CJOFlowchartGenerator(test_api_response, test_profile_data)

    print("Testing step processing...")
    stage_idx = 0
    stage_data = generator.stages_data[stage_idx]
    steps = stage_data.get('steps', {})
    root_step_id = stage_data.get('rootStep')

    processed_steps = _process_steps_from_root_test(steps, root_step_id, stage_idx, generator)

    print(f"Processing completed. Total steps: {len(processed_steps)}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()