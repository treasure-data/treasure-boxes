#!/usr/bin/env python3

"""
Debug test to check if the step processing works correctly
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

try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.flowchart_generator import CJOFlowchartGenerator

    print("Creating generator...")
    generator = CJOFlowchartGenerator(test_api_response, test_profile_data)

    print(f"Generator created successfully!")
    print(f"Stages count: {len(generator.stages)}")
    print(f"Stages data count: {len(generator.stages_data)}")

    if generator.stages:
        stage = generator.stages[0]
        print(f"First stage name: {stage.name}")
        print(f"First stage paths count: {len(stage.paths)}")

        stage_data = generator.stages_data[0]
        print(f"First stage data steps: {list(stage_data.get('steps', {}).keys())}")
        print(f"First stage root step: {stage_data.get('rootStep')}")

        # Test our step processing logic would work
        steps = stage_data.get('steps', {})
        root_step_id = stage_data.get('rootStep')

        if root_step_id and root_step_id in steps:
            print(f"Root step exists and is accessible: {root_step_id}")
            print(f"Root step data: {steps[root_step_id]}")
        else:
            print(f"ERROR: Root step {root_step_id} not found in steps: {list(steps.keys())}")

    print("Test completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()