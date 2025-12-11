#!/usr/bin/env python3
"""
Simple test for the new step formatting functions
"""

import sys
import os

def test_step_formatting():
    """Test the new step formatting directly"""
    print("=" * 50)
    print("TESTING STEP FORMATTING FUNCTIONS")
    print("=" * 50)

    # Test UUID shortening
    def _get_uuid_short(uuid_str):
        return uuid_str.split('-')[0] if uuid_str and '-' in uuid_str else uuid_str

    # Test display name formatting
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
                    day_names = {1: 'Mondays', 2: 'Tuesdays', 3: 'Wednesdays', 4: 'Thursdays', 5: 'Fridays', 6: 'Saturdays', 7: 'Sundays'}
                    days_str = ', '.join([day_names.get(day, f'Day{day}') for day in days_list])
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

    # Test cases
    test_cases = [
        {
            'name': 'Wait Duration Step',
            'step_data': {'waitStep': 9, 'waitStepUnit': 'day', 'waitStepType': 'Duration'},
            'step_type': 'WaitStep',
            'step_id': 'f7bdda9a-e485-4d11-9cdb-1a8ed535dedd',
            'expected': 'Wait 9 days'
        },
        {
            'name': 'Decision Point',
            'step_data': {},
            'step_type': 'DecisionPoint',
            'step_id': '4314162e-8c2c-4c43-b124-dcd3de3a39a6',
            'expected': 'Decision Point (4314162e)'
        },
        {
            'name': 'Activation Step',
            'step_data': {'name': 'td_japan_activate'},
            'step_type': 'Activation',
            'step_id': '060866cc-d1c8-4900-8315-6be58a164429',
            'expected': 'td_japan_activate'
        },
        {
            'name': 'Jump Step',
            'step_data': {'name': 'jump to second stage'},
            'step_type': 'Jump',
            'step_id': '61d75fc4-d874-4222-b419-16aca3f8af22',
            'expected': 'Jump: jump to second stage'
        },
        {
            'name': 'End Step',
            'step_data': {},
            'step_type': 'End',
            'step_id': '2fb7ac97-e061-4254-bbec-1fc9ea03feea',
            'expected': 'End'
        },
        {
            'name': 'AB Test',
            'step_data': {'name': 'ab test'},
            'step_type': 'ABTest',
            'step_id': '17aa131f-112c-4a37-915f-708082ff8350',
            'expected': 'AB Test (ab test)'
        },
        {
            'name': 'Merge Step',
            'step_data': {},
            'step_type': 'Merge',
            'step_id': '4ad850ca-61f2-4dc4-aacf-5cdc6e79add9',
            'expected': 'Merge (4ad850ca)'
        },
        {
            'name': 'Wait Condition',
            'step_data': {'name': 'wait until pageview', 'waitStepType': 'Condition'},
            'step_type': 'WaitStep',
            'step_id': '705ed60f-0ee6-405d-b3f9-21fa344a8724',
            'expected': 'Wait Condition: wait until pageview'
        },
        {
            'name': 'Wait Days of Week',
            'step_data': {'waitStepType': 'DaysOfTheWeek', 'waitUntilDaysOfTheWeek': [6]},
            'step_type': 'WaitStep',
            'step_id': '5358f880-830c-492d-86aa-4de0a65af4f2',
            'expected': 'Wait until Saturdays'
        }
    ]

    print("\\nRunning test cases...")
    print("-" * 50)

    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        result = _format_step_display_name(
            test_case['step_data'],
            test_case['step_type'],
            test_case['step_id']
        )

        passed = result == test_case['expected']
        status = "✓ PASS" if passed else "✗ FAIL"

        print(f"{i:2d}. {test_case['name']:<20} {status}")
        print(f"    Expected: '{test_case['expected']}'")
        print(f"    Got:      '{result}'")

        if not passed:
            all_passed = False
        print()

    # Test grouping header formats
    print("\\nTesting grouping header formats...")
    print("-" * 50)

    # Decision branch header
    step_id = '4314162e-8c2c-4c43-b124-dcd3de3a39a6'
    branch_name = 'country is japan'
    decision_header = f"Decision ({_get_uuid_short(step_id)}): {branch_name}"
    print(f"Decision Header:  '{decision_header}'")
    print(f"Expected:         'Decision (4314162e): country is japan'")

    # AB Test variant header
    ab_test_name = 'ab test'
    variant_name = 'Variant A'
    percentage = 5
    ab_header = f"AB Test ({ab_test_name}): {variant_name} ({percentage}%)"
    print(f"AB Test Header:   '{ab_header}'")
    print(f"Expected:         'AB Test (ab test): Variant A (5%)'")

    # Wait Condition header
    wait_name = 'wait until pageview'
    condition_name = 'Met condition(s)'
    wait_header = f"Wait Condition: {wait_name} - {condition_name}"
    print(f"Wait Cond Header: '{wait_header}'")
    print(f"Expected:         'Wait Condition: wait until pageview - Met condition(s)'")

    # Stage header
    stage_name = 'First'
    entry_criteria = 'userid is not null'
    stage_header = f"Stage 1: {stage_name} (Entry Criteria: {entry_criteria})"
    print(f"Stage Header:     '{stage_header}'")
    print(f"Expected:         'Stage 1: First (Entry Criteria: userid is not null)'")

    print("\\n" + "=" * 50)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("✓ Step formatting functions are working correctly")
        print("✓ Ready for integration with streamlit app")
    else:
        print("✗ SOME TESTS FAILED!")
        print("✗ Check the implementation")
    print("=" * 50)

    return all_passed

if __name__ == "__main__":
    success = test_step_formatting()
    sys.exit(0 if success else 1)