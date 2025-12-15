#!/usr/bin/env python3
"""
Special formatter for merge step hierarchy display.
"""

from typing import List, Tuple, Dict, Any

def format_merge_hierarchy(generator) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Format steps with merge hierarchy in the exact format requested:

    Decision: country is japan
    --- Wait 3 days
    --- Merge (merge uuid)

    Decision: Excluded profiles
    --- Merge (merge uuid)

    Merge: (merge uuid) - this is a grouping header
    --- wait 1 day
    --- end
    """

    def get_short_uuid(uuid_string: str) -> str:
        """Extract the first part of a UUID (before first hyphen)."""
        return uuid_string.split('-')[0] if uuid_string else uuid_string

    formatted_steps = []
    processed_step_ids = set()  # Track processed steps to avoid duplicates

    for stage in generator.stages:
        stage_idx = stage.index

        # Check if this stage has merge points
        merge_points = set()
        for path in stage.paths:
            for step in path:
                if getattr(step, 'is_merge_header', False) or getattr(step, 'is_merge_endpoint', False):
                    merge_points.add(step.step_id)

        if not merge_points:
            # No merge points - use regular display logic
            for path_idx, path in enumerate(stage.paths):
                for step_idx, step in enumerate(path):
                    # Skip if this step has already been processed
                    if step.step_id in processed_step_ids:
                        continue

                    profile_text = f"({step.profile_count} profiles)"
                    step_display = f"{step.name} {profile_text}"

                    formatted_steps.append((step_display, {
                        'step_id': step.step_id,
                        'step_type': step.step_type,
                        'stage_index': step.stage_index,
                        'profile_count': step.profile_count,
                        'name': step.name,
                        'path_index': path_idx,
                        'step_index': step_idx,
                        'breadcrumbs': [step.name],
                        'stage_entry_criteria': stage.entry_criteria
                    }))
                    processed_step_ids.add(step.step_id)  # Mark as processed
        else:
            # Has merge points - use special hierarchy formatting
            branch_paths = []
            merge_header_path = None

            # Separate branch paths from merge header path
            for path in stage.paths:
                has_merge_header = any(getattr(step, 'is_merge_header', False) for step in path)
                if has_merge_header:
                    merge_header_path = path
                else:
                    branch_paths.append(path)

            # Format all paths with unified step processing
            for path_idx, path in enumerate(branch_paths):
                branch_breadcrumbs = []

                # Build breadcrumb trail for this entire path
                for step in path:
                    if step.step_type == 'DecisionPoint_Branch':
                        branch_breadcrumbs.append(f"Decision: {step.name}")
                    elif step.step_type == 'ABTest_Variant':
                        ab_test_name = "ABTest"  # Could be enhanced to extract from API
                        branch_breadcrumbs.append(f"ABTest ({ab_test_name}): {step.name}")
                    elif not getattr(step, 'is_merge_endpoint', False):
                        branch_breadcrumbs.append(step.name)

                # Process each step in the path uniformly
                path_has_grouping_header = False

                for step_idx, step in enumerate(path):
                    # Skip if this step has already been processed
                    if step.step_id in processed_step_ids:
                        continue

                    is_merge_endpoint = getattr(step, 'is_merge_endpoint', False)
                    profile_text = f"({step.profile_count} profiles)"

                    # Handle grouping header steps (DecisionPoint_Branch, ABTest_Variant)
                    if step.step_type == 'DecisionPoint_Branch':
                        # Decision point grouping header
                        decision_uuid = step.step_id.split('_branch_')[0] if '_branch_' in step.step_id else step.step_id
                        short_uuid = get_short_uuid(decision_uuid)
                        step_display = f"Decision: {step.name} ({short_uuid})"
                        step_breadcrumbs = [f"Decision: {step.name} ({short_uuid})"]
                        is_grouping_header = True
                        path_has_grouping_header = True

                    elif step.step_type == 'ABTest_Variant':
                        # AB test variant grouping header
                        ab_test_uuid = step.step_id.split('_variant_')[0] if '_variant_' in step.step_id else step.step_id
                        short_uuid = get_short_uuid(ab_test_uuid)
                        ab_test_name = "ABTest"  # Could be enhanced to extract from API
                        step_display = f"ABTest ({ab_test_name}): {step.name} ({short_uuid})"
                        step_breadcrumbs = [f"ABTest ({ab_test_name}): {step.name} ({short_uuid})"]
                        is_grouping_header = True
                        path_has_grouping_header = True

                    elif is_merge_endpoint:
                        # Merge endpoint step
                        short_uuid = get_short_uuid(step.step_id)
                        step_display = f"--- Merge ({short_uuid}) {profile_text}" if path_has_grouping_header else f"Merge ({short_uuid}) {profile_text}"
                        merge_breadcrumbs = branch_breadcrumbs + [f"Merge ({short_uuid})"]
                        step_breadcrumbs = merge_breadcrumbs
                        is_grouping_header = False

                    else:
                        # Regular step (any type: WaitStep, ActivationStep, etc.)
                        step_display = f"--- {step.name} {profile_text}" if path_has_grouping_header else f"{step.name} {profile_text}"

                        # Build breadcrumb trail up to this step
                        step_breadcrumbs = []
                        for i, path_step in enumerate(path):
                            if path_step.step_type == 'DecisionPoint_Branch':
                                step_breadcrumbs.append(f"Decision: {path_step.name}")
                            elif path_step.step_type == 'ABTest_Variant':
                                ab_test_name = "ABTest"
                                step_breadcrumbs.append(f"ABTest ({ab_test_name}): {path_step.name}")
                            elif not getattr(path_step, 'is_merge_endpoint', False):
                                step_breadcrumbs.append(path_step.name)
                                if path_step.step_id == step.step_id:
                                    break
                        is_grouping_header = False

                    # Add empty line before grouping headers for visual separation
                    if step.step_type in ['DecisionPoint_Branch', 'ABTest_Variant'] and formatted_steps:
                        formatted_steps.append(("", {
                            'step_id': '',
                            'step_type': 'Empty',
                            'stage_index': stage_idx,
                            'profile_count': 0,
                            'name': '',
                            'is_empty_line': True
                        }))

                    # Add the step to formatted output
                    step_info = {
                        'step_id': step.step_id,
                        'step_type': step.step_type,
                        'stage_index': step.stage_index,
                        'profile_count': step.profile_count,
                        'name': step.name,
                        'path_index': path_idx,
                        'step_index': step_idx,
                        'breadcrumbs': step_breadcrumbs,
                        'stage_entry_criteria': stage.entry_criteria
                    }

                    # Add type-specific metadata
                    if step.step_type in ['DecisionPoint_Branch', 'ABTest_Variant']:
                        step_info['is_branch_header'] = True
                    elif is_merge_endpoint:
                        step_info['is_merge_endpoint'] = True
                    elif path_has_grouping_header:
                        step_info['is_indented'] = True

                    formatted_steps.append((step_display, step_info))
                    processed_step_ids.add(step.step_id)  # Mark as processed

            # Format merge header and post-merge steps using unified approach
            # Also check for any remaining unprocessed steps that should be included
            if merge_header_path:
                post_merge_breadcrumbs = []
                merge_header_processed = False

                for step_idx, step in enumerate(merge_header_path):
                    # Skip if this step has already been processed
                    if step.step_id in processed_step_ids:
                        continue

                    is_merge_header = getattr(step, 'is_merge_header', False)
                    profile_text = f"({step.profile_count} profiles)"

                    if is_merge_header:
                        # Merge grouping header
                        short_uuid = get_short_uuid(step.step_id)
                        post_merge_breadcrumbs = [f"Merge ({short_uuid})"]
                        step_display = f"Merge ({short_uuid})"
                        merge_header_processed = True

                        # Add empty line before merge grouping header
                        if formatted_steps:
                            formatted_steps.append(("", {
                                'step_id': '',
                                'step_type': 'Empty',
                                'stage_index': stage_idx,
                                'profile_count': 0,
                                'name': '',
                                'is_empty_line': True
                            }))

                        step_info = {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': f"Merge ({short_uuid})",
                            'path_index': len(branch_paths),
                            'step_index': step_idx,
                            'is_merge_header': True,
                            'is_branch_header': True,
                            'breadcrumbs': post_merge_breadcrumbs.copy(),
                            'stage_entry_criteria': stage.entry_criteria
                        }

                    else:
                        # Post-merge step (any type: WaitStep, ActivationStep, etc.)
                        post_merge_breadcrumbs.append(step.name)
                        step_display = f"--- {step.name} {profile_text}" if merge_header_processed else f"{step.name} {profile_text}"

                        step_info = {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': len(branch_paths),
                            'step_index': step_idx,
                            'breadcrumbs': post_merge_breadcrumbs.copy(),
                            'stage_entry_criteria': stage.entry_criteria
                        }

                        # Add indentation flag if there was a merge header
                        if merge_header_processed:
                            step_info['is_indented'] = True
                            step_info['is_post_merge'] = True

                    formatted_steps.append((step_display, step_info))
                    processed_step_ids.add(step.step_id)  # Mark as processed

            # Ensure all steps from all paths are included (fallback for missing merge header paths)
            # First, collect all unprocessed steps
            unprocessed_steps = []
            for path_idx, path in enumerate(stage.paths):
                for step_idx, step in enumerate(path):
                    if step.step_id not in processed_step_ids:
                        unprocessed_steps.append((step, path_idx, step_idx))

            # If we have merge points and unprocessed steps, they are likely post-merge steps
            if merge_points and unprocessed_steps:
                # Add merge grouping header if we have post-merge steps
                first_merge_id = next(iter(merge_points))  # Get first merge ID
                short_uuid = get_short_uuid(first_merge_id)

                # Add empty line before merge grouping header
                formatted_steps.append(("", {
                    'step_id': '',
                    'step_type': 'Empty',
                    'stage_index': stage_idx,
                    'profile_count': 0,
                    'name': '',
                    'is_empty_line': True
                }))

                # Add merge grouping header
                formatted_steps.append((f"Merge ({short_uuid})", {
                    'step_id': first_merge_id + "_header",
                    'step_type': 'Merge',
                    'stage_index': stage_idx,
                    'profile_count': 0,  # Grouping headers don't show profile counts
                    'name': f"Merge ({short_uuid})",
                    'path_index': len(stage.paths),
                    'step_index': 0,
                    'is_merge_header': True,
                    'is_branch_header': True,
                    'breadcrumbs': [f"Merge ({short_uuid})"],
                    'stage_entry_criteria': stage.entry_criteria,
                    'is_fallback_merge_header': True  # Mark as fallback
                }))

            # Now add all unprocessed steps (indented if post-merge)
            for step, path_idx, step_idx in unprocessed_steps:
                profile_text = f"({step.profile_count} profiles)"
                is_post_merge = bool(merge_points)  # Indent if there are merge points

                step_display = f"--- {step.name} {profile_text}" if is_post_merge else f"{step.name} {profile_text}"

                formatted_steps.append((step_display, {
                    'step_id': step.step_id,
                    'step_type': step.step_type,
                    'stage_index': step.stage_index,
                    'profile_count': step.profile_count,
                    'name': step.name,
                    'path_index': path_idx,
                    'step_index': step_idx,
                    'breadcrumbs': [step.name],
                    'stage_entry_criteria': stage.entry_criteria,
                    'is_indented': is_post_merge,
                    'is_fallback_processed': True  # Mark as fallback for debugging
                }))
                processed_step_ids.add(step.step_id)

    return formatted_steps