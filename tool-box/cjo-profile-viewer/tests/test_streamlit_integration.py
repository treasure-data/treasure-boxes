#!/usr/bin/env python3
"""
Test to verify the Streamlit integration works without errors.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator
from src.merge_display_formatter import format_merge_hierarchy

def test_streamlit_integration():
    """Test that the formatter produces step_info dictionaries that work with Streamlit app."""

    # Simple API response with merge
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
                        "rootStep": "c2652bb1-4ffd-43fd-87d0-88e4408ca774",
                        "entryCriteria": {
                            "name": "userid > 100",
                            "segmentId": "1738226"
                        },
                        "steps": {
                            "c2652bb1-4ffd-43fd-87d0-88e4408ca774": {
                                "type": "DecisionPoint",
                                "branches": [
                                    {
                                        "id": "07a8699e-208e-45ae-aae6-b538817e258e",
                                        "name": "country is japan",
                                        "segmentId": "1738227",
                                        "excludedPath": False,
                                        "next": "5eca44ab-201f-40a7-98aa-b312449df0fe"
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
                            "5eca44ab-201f-40a7-98aa-b312449df0fe": {
                                "type": "Merge",
                                "next": "571472d5-853f-4be7-a4ae-6ee41ba0140e"
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

    print("Testing Streamlit integration...")
    print("="*50)

    # Use the formatter
    formatted_steps = format_merge_hierarchy(generator)

    # Test that all required fields are present
    required_fields = ['step_id', 'step_type', 'stage_index', 'profile_count', 'name', 'breadcrumbs', 'stage_entry_criteria']

    all_good = True
    for i, (step_display, step_info) in enumerate(formatted_steps):
        print(f"Step {i+1}: {step_display}")

        # Check for required fields
        for field in required_fields:
            if field not in step_info:
                print(f"  ❌ Missing required field: {field}")
                all_good = False
            else:
                print(f"  ✓ Has {field}: {step_info[field]}")

        # Test the breadcrumbs access that was causing the error
        try:
            breadcrumbs = step_info['breadcrumbs']
            print(f"  ✓ Breadcrumbs accessible: {breadcrumbs}")

            # Test enumeration over breadcrumbs (the failing operation)
            for j, crumb in enumerate(breadcrumbs):
                print(f"    Crumb {j}: {crumb}")
        except Exception as e:
            print(f"  ❌ Breadcrumb access failed: {e}")
            all_good = False

        print()

    if all_good:
        print("✅ All steps have required fields for Streamlit integration!")
    else:
        print("❌ Some steps are missing required fields!")

    return all_good

if __name__ == "__main__":
    success = test_streamlit_integration()
    if success:
        print("\n🎉 Streamlit integration test PASSED!")
    else:
        print("\n❌ Streamlit integration test FAILED!")