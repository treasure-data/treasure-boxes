#!/usr/bin/env python3
"""
Test script to verify breadcrumb flow for post-merge steps.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator
from src.merge_display_formatter import format_merge_hierarchy

def test_breadcrumb_flow():
    """Test that post-merge steps show proper breadcrumb progression."""

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

    print("Testing breadcrumb flow for post-merge steps...")
    print("="*60)

    # Use the formatter
    formatted_steps = format_merge_hierarchy(generator)

    print("Generated steps with breadcrumb analysis:")
    print()

    for i, (step_display, step_info) in enumerate(formatted_steps):
        breadcrumbs = step_info.get('breadcrumbs', [])
        step_name = step_info.get('name', 'Unknown')
        step_type = step_info.get('step_type', 'Unknown')

        print(f"{i+1:2d}. {step_display}")
        print(f"    Step: {step_name} ({step_type})")
        print(f"    Breadcrumbs: {' → '.join(breadcrumbs)}")

        # Check if this is a post-merge step
        if step_info.get('is_post_merge', False):
            print(f"    ✓ POST-MERGE STEP - Breadcrumbs show path from merge")
        elif step_info.get('is_merge_header', False):
            print(f"    ✓ MERGE HEADER - Starting point for post-merge breadcrumbs")
        elif step_info.get('is_merge_endpoint', False):
            print(f"    ✓ MERGE ENDPOINT - End of branch path")
        else:
            print(f"    ✓ BRANCH STEP - Individual step in branch path")

        print()

    # Verify expected breadcrumbs
    print("Expected breadcrumb flows:")
    print("1. Branch steps: Just the step name")
    print("2. Merge endpoints: 'Merge (uuid)'")
    print("3. Merge header: 'Merge (uuid)'")
    print("4. Wait 1 day step: 'Merge (uuid) → Wait 1 day'")
    print("5. End step: 'Merge (uuid) → Wait 1 day → End Step'")

    # Find the end step and check its breadcrumbs
    end_step_found = False
    for step_display, step_info in formatted_steps:
        if step_info.get('step_type') == 'End':
            breadcrumbs = step_info.get('breadcrumbs', [])
            expected_crumbs = ['Merge (5eca44ab-201f-40a7-98aa-b312449df0fe)', 'Wait 1 day', 'End Step']

            print(f"\n🔍 End step breadcrumb verification:")
            print(f"   Actual: {breadcrumbs}")
            print(f"   Expected: {expected_crumbs}")

            if breadcrumbs == expected_crumbs:
                print(f"   ✅ CORRECT! End step shows full path from merge")
                end_step_found = True
            else:
                print(f"   ❌ INCORRECT breadcrumb flow")
            break

    if not end_step_found:
        print("❌ End step not found in formatted steps")

    print("\n" + "="*60)
    print("Breadcrumb flow test completed!")

if __name__ == "__main__":
    test_breadcrumb_flow()