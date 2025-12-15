#!/usr/bin/env python3
"""
Test script to verify the exact display format matches what was requested.
"""

import pandas as pd
from src.flowchart_generator import CJOFlowchartGenerator

def simulate_streamlit_display():
    """Simulate the Streamlit display format to verify it matches the expected output."""

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

    # Sample profile data
    profile_data = pd.DataFrame({
        'cdp_customer_id': ['user1', 'user2', 'user3'],
        'intime_journey': ['2023-01-01 10:00:00'] * 3,
        'intime_stage_0': ['2023-01-01 10:00:00'] * 3,
    })

    # Initialize the generator
    generator = CJOFlowchartGenerator(api_response, profile_data)

    print("Simulating Streamlit display format...")
    print("="*60)

    # Simulate the step display logic from streamlit_app.py
    all_steps = []
    for stage in generator.stages:
        for path_idx, path in enumerate(stage.paths):
            breadcrumbs = []
            display_breadcrumbs = []

            # Add stage entry criteria as root if it exists (for detail view only)
            stage_entry_criteria = stage.entry_criteria
            if stage_entry_criteria:
                breadcrumbs.append(stage_entry_criteria)

            for step_idx, step in enumerate(path):
                # Check if this is a merge step with special hierarchy handling
                is_merge_endpoint = getattr(step, 'is_merge_endpoint', False)
                is_merge_header = getattr(step, 'is_merge_header', False)

                # Handle merge endpoint (merge at the end of a branch)
                if is_merge_endpoint:
                    profile_text = f"({step.profile_count} profiles)"
                    merge_display = f"Stage {step.stage_index + 1}: {'--- Merge (' + step.step_id + ')'} {profile_text}"
                    all_steps.append((merge_display, {
                        'step_id': step.step_id,
                        'step_type': step.step_type,
                        'is_merge_endpoint': True
                    }))
                    continue

                # Handle merge header (grouping header for post-merge steps)
                if is_merge_header:
                    profile_text = f"({step.profile_count} profiles)"
                    merge_header_display = f"Stage {step.stage_index + 1}: Merge: ({step.step_id}) - this is a grouping header {profile_text}"
                    all_steps.append((merge_header_display, {
                        'step_id': step.step_id,
                        'step_type': step.step_type,
                        'is_merge_header': True
                    }))
                    # Reset breadcrumbs for post-merge steps
                    breadcrumbs = []
                    display_breadcrumbs = []
                    if stage_entry_criteria:
                        breadcrumbs.append(stage_entry_criteria)
                    continue

                # Regular step processing
                breadcrumbs.append(step.name)
                display_breadcrumbs.append(step.name)

                # Check if this step should be indented (post-merge steps)
                indent_prefix = ""
                if len(path) > 0 and step_idx > 0:
                    prev_step = path[step_idx - 1]
                    if getattr(prev_step, 'is_merge_header', False):
                        indent_prefix = "--- "

                breadcrumb_trail = " → ".join(display_breadcrumbs)
                profile_text = f"({step.profile_count} profiles)"

                step_display = f"Stage {step.stage_index + 1}: {indent_prefix}{breadcrumb_trail} {profile_text}"

                all_steps.append((step_display, {
                    'step_id': step.step_id,
                    'step_type': step.step_type,
                    'is_indented': bool(indent_prefix)
                }))

    print("Generated step list for dropdown:")
    print("")
    for i, (step_display, step_info) in enumerate(all_steps):
        print(f"{i+1:2d}. {step_display}")

    print("")
    print("Expected format:")
    print("1. Wait 2 days")
    print("2. Decision: country is japan")
    print("3. --- Wait 3 days")
    print("4. --- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe)")
    print("5. Decision: Excluded profiles")
    print("6. --- Merge (5eca44ab-201f-40a7-98aa-b312449df0fe)")
    print("7. Merge: (5eca44ab-201f-40a7-98aa-b312449df0fe) - this is a grouping header")
    print("8. --- Wait 1 day")
    print("9. --- End Step")

    print("\n" + "="*60)
    print("Display format test completed!")

if __name__ == "__main__":
    simulate_streamlit_display()