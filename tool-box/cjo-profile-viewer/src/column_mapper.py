"""
Column Mapping Module for CJO Profile Viewer

This module implements the column mapping logic from guides/journey_column_mapping.md
to convert technical column names from journey tables to human-readable display names.
"""

import re
from typing import Dict, List, Optional, Tuple


class CJOColumnMapper:
    """Maps CJO table column names to human-readable display names using API response data."""

    def __init__(self, api_response: dict):
        """
        Initialize the mapper with journey API response.

        Args:
            api_response: Journey API response containing stage and step definitions
        """
        self.api_response = api_response
        self.journey_data = api_response.get('data', {})
        self.attributes = self.journey_data.get('attributes', {})
        self.stages = self.attributes.get('journeyStages', [])

        # Build lookup maps for efficient mapping
        self._build_lookup_maps()

    def _build_lookup_maps(self):
        """Build lookup maps for steps, variants, and branches."""
        self.step_map = {}
        self.variant_map = {}
        self.branch_map = {}

        for stage_idx, stage in enumerate(self.stages):
            steps = stage.get('steps', {})

            for step_uuid, step_data in steps.items():
                # Convert UUID format (API uses hyphens, columns use underscores)
                converted_uuid = step_uuid.replace('-', '_')
                self.step_map[converted_uuid] = {
                    'stage_index': stage_idx,
                    'uuid': step_uuid,
                    'data': step_data
                }

                # Map AB test variants
                if step_data.get('type') == 'ABTest':
                    variants = step_data.get('variants', [])
                    for variant in variants:
                        variant_uuid = variant['id'].replace('-', '_')
                        self.variant_map[variant_uuid] = {
                            'stage_index': stage_idx,
                            'step_uuid': converted_uuid,
                            'data': variant
                        }

                # Map decision point branches
                if step_data.get('type') == 'DecisionPoint':
                    branches = step_data.get('branches', [])
                    for branch in branches:
                        segment_id = str(branch.get('segmentId', ''))
                        self.branch_map[segment_id] = {
                            'stage_index': stage_idx,
                            'step_uuid': converted_uuid,
                            'data': branch
                        }

    def map_column_to_display_name(self, column_name: str) -> str:
        """
        Map a technical column name to a human-readable display name.

        Args:
            column_name: Technical column name from journey table

        Returns:
            Human-readable display name following the guide's formatting rules
        """
        # Core journey columns
        if column_name == 'cdp_customer_id':
            return 'Customer ID'
        if column_name == 'intime_journey':
            return 'Journey (Entry)'
        if column_name == 'outtime_journey':
            return 'Journey (Exit)'
        if column_name == 'intime_goal':
            return 'Goal Achievement (Entry)'
        if column_name == 'time':
            return 'Timestamp'

        # Stage columns
        stage_match = re.match(r'^(intime|outtime)_stage_(\d+)$', column_name)
        if stage_match:
            time_type, stage_index = stage_match.groups()
            time_label = 'Entry' if time_type == 'intime' else 'Exit'
            return f'Stage {stage_index} ({time_label})'

        # Milestone columns
        milestone_match = re.match(r'^intime_stage_(\d+)_milestone$', column_name)
        if milestone_match:
            stage_index = int(milestone_match.group(1))
            milestone = self._get_milestone_name(stage_index)
            if milestone:
                return f'Stage {stage_index} Milestone: {milestone} (Entry)'
            return f'Stage {stage_index} Milestone (Entry)'

        # Step columns - extract components
        step_match = re.match(r'^(intime|outtime)_stage_(\d+)_(.+)$', column_name)
        if step_match:
            time_type, stage_index, step_part = step_match.groups()
            time_label = 'Entry' if time_type == 'intime' else 'Exit'

            # Handle AB test variants
            variant_match = re.match(r'^(.+)_variant_(.+)$', step_part)
            if variant_match:
                step_uuid, variant_uuid = variant_match.groups()
                variant_info = self.variant_map.get(variant_uuid)
                if variant_info:
                    variant_name = variant_info['data'].get('name', f'Variant {variant_uuid}')
                    return f'ABTest: {variant_name} ({time_label})'
                return f'ABTest: Unknown Variant ({time_label})'

            # Handle decision point branches (with segment ID)
            if re.match(r'^[a-f0-9_]+_\d+$', step_part):
                segment_id = step_part.split('_')[-1]
                branch_info = self.branch_map.get(segment_id)
                if branch_info:
                    branch_data = branch_info['data']
                    if branch_data.get('excludedPath'):
                        branch_name = 'Excluded Path'
                    else:
                        branch_name = branch_data.get('name', f'Branch {segment_id}')
                    return f'Decision Branch: {branch_name} ({time_label})'
                return f'Decision Branch: Branch {segment_id} ({time_label})'

            # Handle regular steps
            step_info = self.step_map.get(step_part)
            if step_info:
                step_data = step_info['data']
                step_type = step_data.get('type', 'Unknown')

                if step_type == 'Activation':
                    step_name = step_data.get('name', 'Activation')
                    return f'Activation: {step_name} ({time_label})'
                elif step_type == 'WaitStep':
                    wait_step = step_data.get('waitStep', 1)
                    wait_unit = step_data.get('waitStepUnit', 'day')
                    return f'Wait {wait_step} {wait_unit} ({time_label})'
                elif step_type == 'Jump':
                    step_name = step_data.get('name', 'Jump')
                    return f'Jump: {step_name} ({time_label})'
                elif step_type == 'End':
                    return f'End Step ({time_label})'
                elif step_type == 'DecisionPoint':
                    return f'Decision Point ({time_label})'
                elif step_type == 'ABTest':
                    step_name = step_data.get('name', 'AB Test')
                    return f'ABTest: {step_name} ({time_label})'
                else:
                    step_name = step_data.get('name', step_type)
                    return f'{step_name} ({time_label})'

        return 'Unknown'

    def get_timeline_display_name(self, column_name: str) -> str:
        """
        Enhanced mapping for timeline-specific display with better formatting.

        All events use the format: Enter|Exit (event name)

        Args:
            column_name: Technical column name from timeline query

        Returns:
            Human-readable timeline event name in "Enter|Exit (event)" format
        """
        # Determine direction prefix
        if column_name.startswith('intime_'):
            prefix = 'Enter'
        elif column_name.startswith('outtime_'):
            prefix = 'Exit'
        else:
            prefix = None

        # Handle auxiliary table columns (no intime/outtime prefix)
        if any(aux in column_name for aux in ['jump_history', 'reentry_history', 'standby']):
            if 'jump_history' in column_name:
                return 'Cross-Journey Jump'
            elif 'reentry_history' in column_name:
                return 'Re-entry'
            elif 'standby' in column_name:
                return 'Pending Jump'

        # Get the base display name from the standard mapper
        display_name = self.map_column_to_display_name(column_name)

        if display_name == 'Unknown':
            event_label = column_name
        else:
            # Strip the trailing "(Entry)" / "(Exit)" that map_column_to_display_name adds
            event_label = re.sub(r'\s*\((Entry|Exit)\)$', '', display_name).strip()

            # Special labels for journey/goal/milestone
            if column_name == 'intime_journey':
                event_label = 'Journey'
            elif column_name == 'outtime_journey':
                event_label = 'Journey'
            elif column_name == 'intime_goal':
                event_label = 'Goal'
            elif re.match(r'^(intime|outtime)_stage_\d+$', column_name):
                stage_match = re.search(r'stage_(\d+)', column_name)
                stage_num = stage_match.group(1) if stage_match else '?'
                event_label = f'Stage {stage_num}'
            elif re.match(r'^intime_stage_\d+_milestone$', column_name):
                event_label = re.sub(r'\s*\((Entry|Exit)\)$', '', display_name).strip()

        if prefix:
            return f'{prefix} - {event_label}'
        return event_label

    def is_timeline_column(self, column_name: str) -> bool:
        """
        Check if column represents a timeline event.

        Args:
            column_name: Technical column name

        Returns:
            True if column is a timeline event column
        """
        # Check for standard timeline columns
        if column_name.startswith(('intime_', 'outtime_')):
            return True

        # Check for auxiliary table columns
        if any(aux in column_name for aux in ['jump_history', 'reentry_history', 'standby']):
            return True

        return False

    def get_event_type_from_column(self, column_name: str) -> str:
        """
        Determine timeline event type from column name.

        Args:
            column_name: Technical column name

        Returns:
            Event type string for timeline categorization
        """
        if column_name.startswith('intime_'):
            if 'goal' in column_name:
                return 'goal_achieved'
            elif 'milestone' in column_name:
                return 'milestone'
            elif 'journey' in column_name:
                return 'journey_entry'
            elif 'stage' in column_name and not any(x in column_name for x in ['milestone', 'exit']):
                return 'stage_entry'
            else:
                return 'step_entry'

        elif column_name.startswith('outtime_'):
            if 'journey' in column_name:
                return 'journey_exit'
            elif 'stage' in column_name:
                return 'stage_exit'
            else:
                return 'step_exit'

        elif any(aux in column_name for aux in ['jump_history', 'reentry_history', 'standby']):
            return 'cross_journey'

        else:
            return 'unknown'

    def get_timeline_stage_name(self, stage_index: int) -> str:
        """
        Get human-readable stage name for timeline display.

        Args:
            stage_index: Stage index number

        Returns:
            Human-readable stage name
        """
        if stage_index < len(self.stages):
            stage = self.stages[stage_index]
            stage_name = stage.get('name', f'Stage {stage_index}')
            return stage_name
        return f'Stage {stage_index}'

    def get_timeline_step_name(self, step_uuid: str, stage_index: Optional[int] = None) -> str:
        """
        Get human-readable step name for timeline display.

        Args:
            step_uuid: Step UUID (with underscores)
            stage_index: Optional stage index for context

        Returns:
            Human-readable step name
        """
        step_info = self.step_map.get(step_uuid)
        if step_info:
            step_data = step_info['data']
            step_type = step_data.get('type', 'Unknown')

            # Use existing step display logic from utils
            from .utils.step_display import get_step_display_name
            try:
                return get_step_display_name(step_data)
            except:
                # Fallback if import fails
                return step_data.get('name', f'{step_type} Step')

        return f'Step {step_uuid[:8]}...'  # Show first 8 chars of UUID

    def _get_milestone_name(self, stage_index: int) -> Optional[str]:
        """Get milestone name for a stage."""
        if stage_index < len(self.stages):
            milestone = self.stages[stage_index].get('milestone')
            if milestone:
                return milestone.get('name')
        return None

    def get_step_info(self, column_name: str) -> Optional[Dict]:
        """
        Get detailed step information for a column.

        Args:
            column_name: Technical column name

        Returns:
            Dictionary with step information or None if not a step column
        """
        step_match = re.match(r'^(intime|outtime)_stage_(\d+)_(.+)$', column_name)
        if not step_match:
            return None

        time_type, stage_index, step_part = step_match.groups()

        # Handle AB test variants
        variant_match = re.match(r'^(.+)_variant_(.+)$', step_part)
        if variant_match:
            step_uuid, variant_uuid = variant_match.groups()
            variant_info = self.variant_map.get(variant_uuid)
            if variant_info:
                return {
                    'type': 'ABTest_Variant',
                    'stage_index': int(stage_index),
                    'step_uuid': step_uuid,
                    'variant_uuid': variant_uuid,
                    'variant_data': variant_info['data'],
                    'time_type': time_type
                }

        # Handle decision point branches
        if re.match(r'^[a-f0-9_]+_\d+$', step_part):
            segment_id = step_part.split('_')[-1]
            branch_info = self.branch_map.get(segment_id)
            if branch_info:
                return {
                    'type': 'DecisionPoint_Branch',
                    'stage_index': int(stage_index),
                    'step_uuid': branch_info['step_uuid'],
                    'segment_id': segment_id,
                    'branch_data': branch_info['data'],
                    'time_type': time_type
                }

        # Handle regular steps
        step_info = self.step_map.get(step_part)
        if step_info:
            return {
                'type': step_info['data'].get('type', 'Unknown'),
                'stage_index': int(stage_index),
                'step_uuid': step_part,
                'step_data': step_info['data'],
                'time_type': time_type
            }

        return None

    def get_all_column_mappings(self, columns: List[str]) -> Dict[str, str]:
        """
        Get mappings for all columns in a list.

        Args:
            columns: List of technical column names

        Returns:
            Dictionary mapping technical names to display names
        """
        return {col: self.map_column_to_display_name(col) for col in columns}