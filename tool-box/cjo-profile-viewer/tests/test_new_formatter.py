#!/usr/bin/env python3
"""
Test the new merge hierarchy formatter.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator
from src.hierarchical_step_formatter import format_hierarchical_steps

def test_new_formatter():
    """Test the new formatter with the provided API response."""

    # The exact API response provided by the user
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

    # Sample profile data with some profiles
    profile_data = pd.DataFrame({
        'cdp_customer_id': ['user1', 'user2', 'user3'],
        'intime_journey': ['2023-01-01 10:00:00'] * 3,
        'intime_stage_0': ['2023-01-01 10:00:00'] * 3,
        # Add some sample profile counts
        'intime_stage_0_c2652bb1_4ffd_43fd_87d0_88e4408ca774_1738227': ['2023-01-01'] * 2 + [None],  # 2 in Japan branch
        'intime_stage_0_c2652bb1_4ffd_43fd_87d0_88e4408ca774_1738229': [None, None, '2023-01-01'],  # 1 in excluded branch
        'intime_stage_0_5eca44ab_201f_40a7_98aa_b312449df0fe': ['2023-01-01'] * 3,  # 3 in merge
    })

    # Initialize the generator
    generator = CJOFlowchartGenerator(api_response, profile_data)

    print("Testing new merge hierarchy formatter...")
    print("="*60)

    # Use the new formatter
    formatted_steps = format_hierarchical_steps(generator)

    print("Generated step list with new formatter:")
    print("")
    for i, (step_display, step_info) in enumerate(formatted_steps):
        print(f"{i+1:2d}. {step_display}")

    print("")
    print("Expected format:")
    print("Decision: country is japan")
    print("--- Wait 3 days")
    print("--- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe)")
    print("")
    print("Decision: Excluded profiles")
    print("--- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe)")
    print("")
    print("Merge: (5eca44ab-201f-40a7-98aa-b312449df0fe) - this is a grouping header")
    print("--- wait 1 day")
    print("--- end")

    print("\n" + "="*60)
    print("New formatter test completed!")

if __name__ == "__main__":
    test_new_formatter()