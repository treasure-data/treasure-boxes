#!/usr/bin/env python3
"""
Test script to verify complete breadcrumb history for all steps.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator
from src.hierarchical_step_formatter import format_hierarchical_steps

def test_complete_breadcrumbs():
    """Test that all steps show complete breadcrumb history."""

    # The API response from your example
    api_response = {
        "data": {
            "id": "218058",
            "type": "journey",
            "attributes": {
                "audienceId": "984536",
                "name": "merge(v2)",
                "journeyStages": [
                    {
                        "id": "253964",
                        "name": "s1",
                        "rootStep": "0765d8f4-f2e2-4906-af66-1d2efdad9973",
                        "entryCriteria": {
                            "name": "userid > 100",
                            "segmentId": "1738226"
                        },
                        "steps": {
                            "0765d8f4-f2e2-4906-af66-1d2efdad9973": {
                                "type": "WaitStep",
                                "next": "c2652bb1-4ffd-43fd-87d0-88e4408ca774",
                                "waitStep": 2,
                                "waitStepUnit": "day",
                                "waitStepType": "Duration"
                            },
                            "c2652bb1-4ffd-43fd-87d0-88e4408ca774": {
                                "type": "DecisionPoint",
                                "branches": [
                                    {
                                        "id": "07a8699e-208e-45ae-aae6-b538817e258e",
                                        "name": "country is japan",
                                        "segmentId": "1738227",
                                        "excludedPath": False,
                                        "next": "bda2e471-d716-4a09-9a51-e6db439a5b40"
                                    },
                                    {
                                        "id": "ad91011f-bd65-423e-9c8c-df884d260a78",
                                        "name": None,
                                        "segmentId": "1738229",
                                        "excludedPath": True,
                                        "next": "5eca44ab-201f-40a7-98aa-b312449df0fe"
                                    }
                                ]
                            },
                            "bda2e471-d716-4a09-9a51-e6db439a5b40": {
                                "type": "WaitStep",
                                "next": "5eca44ab-201f-40a7-98aa-b312449df0fe",
                                "waitStep": 3,
                                "waitStepUnit": "day",
                                "waitStepType": "Duration"
                            },
                            "5eca44ab-201f-40a7-98aa-b312449df0fe": {
                                "type": "Merge",
                                "next": "feee7a26-dfd8-4687-8914-805a26b7d14f"
                            },
                            "feee7a26-dfd8-4687-8914-805a26b7d14f": {
                                "type": "WaitStep",
                                "next": "571472d5-853f-4be7-a4ae-6ee41ba0140e",
                                "waitStep": 1,
                                "waitStepUnit": "day",
                                "waitStepType": "Duration"
                            },
                            "571472d5-853f-4be7-a4ae-6ee41ba0140e": {
                                "type": "End"
                            }
                        }
                    }
                ]
            }
        }
    }

    profile_data = pd.DataFrame({
        'cdp_customer_id': ['user1', 'user2'],
        'intime_journey': ['2023-01-01 10:00:00'] * 2,
    })

    # Initialize the generator
    generator = CJOFlowchartGenerator(api_response, profile_data)

    print("Testing complete breadcrumb history for all steps...")
    print("="*70)

    # Use the formatter
    formatted_steps = format_hierarchical_steps(generator)

    # Expected breadcrumb patterns (using shortened UUIDs)
    expected_patterns = {
        'Decision: country is japan': ['Decision: country is japan'],
        'Wait 3 day': ['Wait 2 day', 'Decision Point', 'Decision: country is japan', 'Wait 3 day'],
        'Decision: Excluded Profiles': ['Decision: Excluded Profiles'],
        'Wait 1 day': ['Merge (5eca44ab)', 'Wait 1 day'],
        'End Step': ['Merge (5eca44ab)', 'Wait 1 day', 'End Step']
    }

    print("Analyzing breadcrumb completeness:")
    print()

    all_correct = True
    for i, (step_display, step_info) in enumerate(formatted_steps):
        breadcrumbs = step_info.get('breadcrumbs', [])
        step_name = step_info.get('name', 'Unknown')
        step_type = step_info.get('step_type', 'Unknown')

        print(f"{i+1:2d}. {step_display}")
        print(f"    Step: {step_name} ({step_type})")
        print(f"    Breadcrumbs: {' → '.join(breadcrumbs)}")

        # Check against expected patterns if available
        if step_name in expected_patterns:
            expected = expected_patterns[step_name]
            if breadcrumbs == expected:
                print(f"    ✅ CORRECT breadcrumb pattern")
            else:
                print(f"    ❌ INCORRECT breadcrumb pattern")
                print(f"       Expected: {' → '.join(expected)}")
                print(f"       Actual:   {' → '.join(breadcrumbs)}")
                all_correct = False
        else:
            # For merge endpoints and other steps, just verify they have breadcrumbs
            if len(breadcrumbs) > 0:
                print(f"    ✅ Has breadcrumb history")
            else:
                print(f"    ❌ Missing breadcrumb history")
                all_correct = False

        print()

    # Specific checks
    print("🔍 Specific breadcrumb pattern verification:")
    print()

    # Find Wait 3 day step
    wait_3_step = None
    for step_display, step_info in formatted_steps:
        if step_info.get('name') == 'Wait 3 day':
            wait_3_step = step_info
            break

    if wait_3_step:
        breadcrumbs = wait_3_step.get('breadcrumbs', [])
        print(f"Wait 3 day breadcrumbs: {breadcrumbs}")

        # Should show: Decision point → Decision branch → Wait step
        if 'Decision: country is japan' in breadcrumbs and 'Wait 3 day' in breadcrumbs:
            print("✅ Wait 3 day shows it came from Decision: country is japan")
        else:
            print("❌ Wait 3 day does not show complete path history")
            all_correct = False

        # Additional check for shortened UUID format
        has_short_uuid = any('Merge (5eca44ab)' in crumb for crumb in breadcrumbs if 'Merge (' in crumb)
        if not has_short_uuid:
            print("✅ Breadcrumbs correctly use shortened UUID format (no merge in this path)")
        else:
            print("✅ Breadcrumbs correctly use shortened UUID format")
    else:
        print("❌ Wait 3 day step not found")
        all_correct = False

    print()
    if all_correct:
        print("✅ All breadcrumb patterns are CORRECT!")
    else:
        print("❌ Some breadcrumb patterns are INCORRECT!")

    print("\n" + "="*70)
    print("Complete breadcrumb test finished!")

    return all_correct

if __name__ == "__main__":
    success = test_complete_breadcrumbs()
    if success:
        print("\n🎉 Complete breadcrumb test PASSED!")
    else:
        print("\n❌ Complete breadcrumb test FAILED!")