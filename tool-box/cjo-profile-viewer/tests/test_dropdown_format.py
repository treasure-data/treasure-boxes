#!/usr/bin/env python3
"""
Test script to verify dropdown format treats merges as grouping headers.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator
from src.merge_display_formatter import format_merge_hierarchy

def test_dropdown_format():
    """Test that merge steps are treated as grouping headers in dropdown format."""

    # API response with merge steps
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
        'cdp_customer_id': ['user1', 'user2', 'user3'],
        'intime_journey': ['2023-01-01 10:00:00'] * 3,
    })

    # Initialize the generator
    generator = CJOFlowchartGenerator(api_response, profile_data)

    print("Testing dropdown format for merge grouping headers...")
    print("="*60)

    # Use the formatter
    formatted_steps = format_merge_hierarchy(generator)

    print("Generated dropdown format:")
    print()

    merge_header_found = False
    post_merge_steps = []

    for i, (step_display, step_info) in enumerate(formatted_steps):
        step_type = step_info.get('step_type', 'Unknown')
        is_grouping_header = step_info.get('is_grouping_header', False)
        is_merge_header = step_info.get('is_merge_header', False)
        is_post_merge = step_info.get('is_post_merge', False)

        print(f"{i+1:2d}. {step_display}")

        # Analyze the step
        if is_merge_header:
            merge_header_found = True
            # Check that merge header shows profile count like Decision/AB Test headers
            if "profiles)" in step_display:
                print(f"    ✅ MERGE HEADER - Shows profile count (like Decision/AB Test)")
            else:
                print(f"    ❌ MERGE HEADER - Missing profile count")

        elif is_post_merge:
            post_merge_steps.append((step_display, step_info))
            # Check that post-merge steps are indented
            if step_display.startswith("Stage") and "--- " in step_display:
                print(f"    ✅ POST-MERGE STEP - Properly indented with ---")
            else:
                print(f"    ❌ POST-MERGE STEP - Not properly indented")

        else:
            print(f"    ✓ REGULAR STEP")

        print()

    print("Verification Summary:")
    print()

    # Check merge header format
    if merge_header_found:
        print("✅ Merge header found and treated as grouping header")
    else:
        print("❌ Merge header not found or not marked as grouping header")

    # Check post-merge step indentation
    if len(post_merge_steps) > 0:
        all_indented = all("--- " in display for display, info in post_merge_steps)
        if all_indented:
            print(f"✅ All {len(post_merge_steps)} post-merge steps properly indented with ---")
        else:
            print(f"❌ Some post-merge steps not properly indented")
    else:
        print("⚠️  No post-merge steps found to verify indentation")

    # Expected format example
    print()
    print("Expected dropdown format:")
    print("1. Decision: country is japan (X profiles)      ← Grouping header with profile count")
    print("2. --- Wait 3 day (X profiles)                  ← Indented under Decision")
    print("3. --- Merge (5eca44ab) (X profiles)            ← Branch endpoint")
    print("4. Decision: Excluded Profiles (X profiles)     ← Grouping header with profile count")
    print("5. --- Merge (5eca44ab) (X profiles)            ← Branch endpoint")
    print("6. Merge (5eca44ab) (X profiles)                ← Grouping header with profile count (like Decision/AB Test)")
    print("7. --- Wait 1 day (X profiles)                  ← Indented under Merge")
    print("8. --- End Step (X profiles)                    ← Indented under Merge")

    print("\n" + "="*60)
    print("Dropdown format test completed!")

if __name__ == "__main__":
    test_dropdown_format()