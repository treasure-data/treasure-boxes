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
                    profile_text = f"({step.profile_count} profiles)"
                    step_display = f"Stage {stage_idx + 1}: {step.name} {profile_text}"

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

            # Format branch paths
            for path_idx, path in enumerate(branch_paths):
                current_branch_name = None
                found_branch = False
                branch_breadcrumbs = []

                # First, build the complete breadcrumb trail for this path
                for step in path:
                    if step.step_type == 'DecisionPoint_Branch':
                        branch_breadcrumbs.append(f"Decision: {step.name}")
                    elif not getattr(step, 'is_merge_endpoint', False):
                        branch_breadcrumbs.append(step.name)

                # Now format each step with its proper breadcrumb trail
                for step_idx, step in enumerate(path):
                    is_merge_endpoint = getattr(step, 'is_merge_endpoint', False)

                    if step.step_type == 'DecisionPoint_Branch':
                        # This is the branch decision
                        found_branch = True
                        current_branch_name = step.name
                        profile_text = f"({step.profile_count} profiles)"

                        branch_display = f"Stage {stage_idx + 1}: Decision: {step.name} {profile_text}"

                        # Breadcrumb is just the decision itself
                        step_breadcrumbs = [f"Decision: {step.name}"]

                        formatted_steps.append((branch_display, {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': path_idx,
                            'step_index': step_idx,
                            'is_branch_header': True,
                            'breadcrumbs': step_breadcrumbs,
                            'stage_entry_criteria': stage.entry_criteria
                        }))

                    elif is_merge_endpoint:
                        # This is the merge at the end of this branch
                        profile_text = f"({step.profile_count} profiles)"
                        short_uuid = get_short_uuid(step.step_id)
                        merge_display = f"Stage {stage_idx + 1}: --- Merge ({short_uuid}) {profile_text}"

                        # Breadcrumb shows path up to merge
                        short_uuid = get_short_uuid(step.step_id)
                        merge_breadcrumbs = branch_breadcrumbs + [f"Merge ({short_uuid})"]

                        formatted_steps.append((merge_display, {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': path_idx,
                            'step_index': step_idx,
                            'is_merge_endpoint': True,
                            'breadcrumbs': merge_breadcrumbs,
                            'stage_entry_criteria': stage.entry_criteria
                        }))

                    elif step.step_type not in ['DecisionPoint', 'WaitStep'] or found_branch:
                        # Regular step in this branch (should be indented)
                        # Skip WaitSteps that come before the decision branch
                        if step.step_type == 'WaitStep' and not found_branch:
                            continue

                        profile_text = f"({step.profile_count} profiles)"
                        step_display = f"Stage {stage_idx + 1}: --- {step.name} {profile_text}"

                        # Build breadcrumb trail up to this step
                        step_breadcrumbs = []
                        for i, path_step in enumerate(path):
                            if path_step.step_type == 'DecisionPoint_Branch':
                                step_breadcrumbs.append(f"Decision: {path_step.name}")
                            elif not getattr(path_step, 'is_merge_endpoint', False):
                                step_breadcrumbs.append(path_step.name)
                                if path_step.step_id == step.step_id:
                                    break

                        formatted_steps.append((step_display, {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': path_idx,
                            'step_index': step_idx,
                            'is_indented': True,
                            'breadcrumbs': step_breadcrumbs,
                            'stage_entry_criteria': stage.entry_criteria
                        }))

            # Format merge header and post-merge steps
            if merge_header_path:
                post_merge_breadcrumbs = []
                merge_step_id = None

                for step_idx, step in enumerate(merge_header_path):
                    is_merge_header = getattr(step, 'is_merge_header', False)

                    if is_merge_header:
                        # This is the merge grouping header - no profile count for grouping headers
                        merge_step_id = step.step_id
                        short_uuid = get_short_uuid(step.step_id)
                        post_merge_breadcrumbs = [f"Merge ({short_uuid})"]

                        # No profile count for grouping headers in dropdown
                        merge_header_display = f"Stage {stage_idx + 1}: Merge: ({short_uuid})"

                        formatted_steps.append((merge_header_display, {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': len(branch_paths),  # Use a different path index
                            'step_index': step_idx,
                            'is_merge_header': True,
                            'is_grouping_header': True,  # Mark as grouping header for dropdown
                            'breadcrumbs': post_merge_breadcrumbs.copy(),
                            'stage_entry_criteria': stage.entry_criteria
                        }))

                    else:
                        # Post-merge step (should be indented)
                        # Add this step to the post-merge breadcrumb trail
                        post_merge_breadcrumbs.append(step.name)

                        profile_text = f"({step.profile_count} profiles)"
                        step_display = f"Stage {stage_idx + 1}: --- {step.name} {profile_text}"

                        formatted_steps.append((step_display, {
                            'step_id': step.step_id,
                            'step_type': step.step_type,
                            'stage_index': step.stage_index,
                            'profile_count': step.profile_count,
                            'name': step.name,
                            'path_index': len(branch_paths),  # Use a different path index
                            'step_index': step_idx,
                            'is_indented': True,
                            'is_post_merge': True,
                            'breadcrumbs': post_merge_breadcrumbs.copy(),
                            'stage_entry_criteria': stage.entry_criteria
                        }))

    return formatted_steps