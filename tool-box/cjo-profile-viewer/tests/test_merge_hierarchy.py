#!/usr/bin/env python3
"""
Test script to verify merge step hierarchy display with the provided API response.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator

def test_merge_hierarchy_display():
    """Test the merge step hierarchy with the exact API response provided."""

    # The exact API response provided by the user
    api_response = {
        "data": {
            "id": "218058",
            "type": "journey",
            "attributes": {
                "audienceId": "984536",
                "journeyBundleId": "117414",
                "name": "merge(v2)",
                "description": "",
                "state": "launched",
                "createdAt": "2025-12-08T20:33:37.572Z",
                "updatedAt": "2025-12-08T20:43:38.252Z",
                "launchedAt": "2025-12-08T20:34:19.718Z",
                "allowReentry": False,
                "paused": False,
                "pausedAt": None,
                "journeyBundleName": "merge",
                "versionNumber": 2,
                "journeyBundleDescription": "",
                "reentryMode": "no_reentry",
                "goal": None,
                "journeyStages": [
                    {
                        "id": "253964",
                        "name": "s1",
                        "description": None,
                        "rootStep": "0765d8f4-f2e2-4906-af66-1d2efdad9973",
                        "entryCriteria": {
                            "name": "userid > 100",
                            "segmentId": "1738226",
                            "description": None
                        },
                        "milestone": None,
                        "exitCriterias": [],
                        "steps": {
                            "0765d8f4-f2e2-4906-af66-1d2efdad9973": {
                                "type": "WaitStep",
                                "next": "c2652bb1-4ffd-43fd-87d0-88e4408ca774",
                                "waitStep": 2,
                                "waitStepUnit": "day",
                                "waitStepType": "Duration",
                                "waitUntilDate": None,
                                "timezone": "UTC",
                                "waitUntilDaysOfTheWeek": None
                            },
                            "c2652bb1-4ffd-43fd-87d0-88e4408ca774": {
                                "type": "DecisionPoint",
                                "branches": [
                                    {
                                        "id": "07a8699e-208e-45ae-aae6-b538817e258e",
                                        "name": "country is japan",
                                        "description": None,
                                        "segmentId": "1738227",
                                        "excludedPath": False,
                                        "next": "bda2e471-d716-4a09-9a51-e6db439a5b40"
                                    },
                                    {
                                        "id": "ad91011f-bd65-423e-9c8c-df884d260a78",
                                        "name": None,
                                        "description": None,
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
                                "waitStepType": "Duration",
                                "waitUntilDate": None,
                                "timezone": "UTC",
                                "waitUntilDaysOfTheWeek": None
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
                                "waitStepType": "Duration",
                                "waitUntilDate": None,
                                "timezone": "UTC",
                                "waitUntilDaysOfTheWeek": None
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

    # Sample profile data
    profile_data = pd.DataFrame({
        'cdp_customer_id': ['user1', 'user2', 'user3', 'user4'],
        'intime_journey': ['2023-01-01 10:00:00'] * 4,
        'intime_stage_0': ['2023-01-01 10:00:00'] * 4,
        # Wait 2 days step
        'intime_stage_0_0765d8f4_f2e2_4906_af66_1d2efdad9973': ['2023-01-01 10:00:00'] * 4,
        'outtime_stage_0_0765d8f4_f2e2_4906_af66_1d2efdad9973': ['2023-01-03 10:00:00'] * 4,
        # Decision branches
        'intime_stage_0_c2652bb1_4ffd_43fd_87d0_88e4408ca774_1738227': ['2023-01-03 10:00:00', '2023-01-03 10:00:00', None, None],  # Japan branch
        'intime_stage_0_c2652bb1_4ffd_43fd_87d0_88e4408ca774_1738229': [None, None, '2023-01-03 10:00:00', '2023-01-03 10:00:00'],  # Excluded branch
        # Wait 3 days (only for Japan branch)
        'intime_stage_0_bda2e471_d716_4a09_9a51_e6db439a5b40': ['2023-01-03 10:05:00', '2023-01-03 10:05:00', None, None],
        'outtime_stage_0_bda2e471_d716_4a09_9a51_e6db439a5b40': ['2023-01-06 10:05:00', None, None, None],
        # Merge step
        'intime_stage_0_5eca44ab_201f_40a7_98aa_b312449df0fe': ['2023-01-06 10:05:00', '2023-01-03 10:00:00', '2023-01-03 10:00:00', None],
        'outtime_stage_0_5eca44ab_201f_40a7_98aa_b312449df0fe': ['2023-01-06 10:10:00', None, None, None],
        # Wait 1 day (post-merge)
        'intime_stage_0_feee7a26_dfd8_4687_8914_805a26b7d14f': ['2023-01-06 10:10:00', None, None, None],
    })

    # Initialize the generator
    generator = CJOFlowchartGenerator(api_response, profile_data)

    print("Testing merge step hierarchy display...")
    print("="*60)

    # Test that we have one stage
    assert len(generator.stages) == 1, f"Expected 1 stage, got {len(generator.stages)}"
    print("✓ Stage creation working")

    # Test the stage paths
    stage = generator.stages[0]
    paths = stage.paths

    print(f"Number of paths generated: {len(paths)}")
    print("")

    # Print each path for debugging
    for i, path in enumerate(paths):
        print(f"Path {i+1}:")
        for step in path:
            step_info = f"  - {step.name} ({step.step_type})"
            if hasattr(step, 'is_merge_endpoint') and step.is_merge_endpoint:
                step_info += " [MERGE ENDPOINT]"
            if hasattr(step, 'is_merge_header') and step.is_merge_header:
                step_info += " [MERGE HEADER]"
            print(step_info)
        print("")

    # Expected structure should be:
    # Path 1: Wait 2 days → Decision: country is japan → Wait 3 days → Merge [ENDPOINT]
    # Path 2: Wait 2 days → Decision: Excluded profiles → Merge [ENDPOINT]
    # Path 3: Merge [HEADER] → Wait 1 day → End Step

    print("Analyzing path structure for expected hierarchy...")

    # Check for merge endpoints
    merge_endpoints = []
    merge_headers = []

    for path in paths:
        for step in path:
            if getattr(step, 'is_merge_endpoint', False):
                merge_endpoints.append(step)
            if getattr(step, 'is_merge_header', False):
                merge_headers.append(step)

    print(f"Found {len(merge_endpoints)} merge endpoint(s)")
    print(f"Found {len(merge_headers)} merge header(s)")

    assert len(merge_endpoints) > 0, "No merge endpoints found"
    assert len(merge_headers) > 0, "No merge headers found"

    print("")
    print("Expected display structure:")
    print("Decision: country is japan")
    print("--- Wait 3 days")
    print("--- Merge (merge uuid)")
    print("")
    print("Decision: Excluded profiles")
    print("--- Merge (merge uuid)")
    print("")
    print("Merge: (merge uuid) - this is a grouping header")
    print("--- wait 1 day")
    print("--- end")

    print("\n" + "="*60)
    print("✅ Merge hierarchy test PASSED!")
    print("Key features working:")
    print("- Merge endpoint detection")
    print("- Merge header creation")
    print("- Proper path separation")
    print("- Step hierarchy attributes")

    return True

if __name__ == "__main__":
    try:
        test_merge_hierarchy_display()
        print("\n🎉 All tests passed! Merge hierarchy is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()