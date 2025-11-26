"""
Flowchart Generator Module for CJO Profile Viewer

This module implements flowchart generation logic from guides/cjo_flowchart_generation_guide.md
to create visual representations of customer journeys.
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd


class FlowchartStep:
    """Represents a single step in the journey flowchart."""

    def __init__(self, step_id: str, step_type: str, name: str, stage_index: int, profile_count: int = 0):
        self.step_id = step_id
        self.step_type = step_type
        self.name = name
        self.stage_index = stage_index
        self.profile_count = profile_count
        self.next_steps = []

    def add_next_step(self, step: 'FlowchartStep'):
        """Add a next step in the flow."""
        self.next_steps.append(step)


class JourneyStage:
    """Represents a journey stage with its steps."""

    def __init__(self, stage_id: str, name: str, index: int, entry_criteria: str = None, milestone: str = None):
        self.stage_id = stage_id
        self.name = name
        self.index = index
        self.entry_criteria = entry_criteria
        self.milestone = milestone
        self.root_step = None
        self.paths = []


class CJOFlowchartGenerator:
    """Generates flowchart representations of CJO journeys."""

    def __init__(self, api_response: dict, profile_data: pd.DataFrame):
        """
        Initialize the flowchart generator.

        Args:
            api_response: Journey API response
            profile_data: DataFrame with profile journey data
        """
        self.api_response = api_response
        self.profile_data = profile_data
        self.journey_data = api_response.get('data', {})
        self.attributes = self.journey_data.get('attributes', {})
        self.stages_data = self.attributes.get('journeyStages', [])

        # Parse journey structure
        self.journey_id = self.journey_data.get('id', '')
        self.journey_name = self.attributes.get('name', '')
        self.audience_id = self.attributes.get('audienceId', '')

        # Build stages
        self.stages = self._build_stages()

    def _build_stages(self) -> List[JourneyStage]:
        """Build journey stages from API response."""
        stages = []

        for stage_idx, stage_data in enumerate(self.stages_data):
            stage_id = stage_data.get('id', '')
            stage_name = stage_data.get('name', f'Stage {stage_idx}')

            entry_criteria = stage_data.get('entryCriteria', {})
            entry_criteria_name = entry_criteria.get('name') if entry_criteria else None

            milestone = stage_data.get('milestone', {})
            milestone_name = milestone.get('name') if milestone else None

            stage = JourneyStage(
                stage_id=stage_id,
                name=stage_name,
                index=stage_idx,
                entry_criteria=entry_criteria_name,
                milestone=milestone_name
            )

            # Build paths for this stage
            stage.paths = self._build_stage_paths(stage_data, stage_idx)
            stages.append(stage)

        return stages

    def _build_stage_paths(self, stage_data: dict, stage_idx: int) -> List[List[FlowchartStep]]:
        """Build all possible paths through a stage."""
        steps = stage_data.get('steps', {})
        root_step_id = stage_data.get('rootStep')

        if not root_step_id or root_step_id not in steps:
            return []

        root_step_data = steps[root_step_id]
        paths = []

        if root_step_data.get('type') == 'DecisionPoint':
            # Create separate path for each branch
            branches = root_step_data.get('branches', [])
            for branch in branches:
                path = []
                # Add decision point step
                decision_step = self._create_step_from_branch(root_step_id, root_step_data, branch, stage_idx)
                path.append(decision_step)

                # Follow the path from this branch
                if branch.get('next'):
                    self._follow_path(steps, branch['next'], path, stage_idx)

                paths.append(path)

        elif root_step_data.get('type') == 'ABTest':
            # Create separate path for each variant
            variants = root_step_data.get('variants', [])
            for variant in variants:
                path = []
                # Add AB test variant step
                variant_step = self._create_step_from_variant(root_step_id, root_step_data, variant, stage_idx)
                path.append(variant_step)

                # Follow the path from this variant
                if variant.get('next'):
                    self._follow_path(steps, variant['next'], path, stage_idx)

                paths.append(path)

        else:
            # Linear path starting from root
            path = []
            self._follow_path(steps, root_step_id, path, stage_idx)
            paths.append(path)

        return paths

    def _follow_path(self, steps: dict, step_id: str, path: List[FlowchartStep], stage_idx: int):
        """Follow a path through the steps."""
        if step_id not in steps:
            return

        step_data = steps[step_id]
        step = self._create_step_from_data(step_id, step_data, stage_idx)
        path.append(step)

        # Continue to next step if it exists
        next_step = step_data.get('next')
        if next_step:
            self._follow_path(steps, next_step, path, stage_idx)

    def _create_step_from_data(self, step_id: str, step_data: dict, stage_idx: int) -> FlowchartStep:
        """Create a FlowchartStep from step data."""
        step_type = step_data.get('type', 'Unknown')
        name = self._get_step_display_name(step_data)
        profile_count = self._get_step_profile_count(step_id, stage_idx, step_type)

        return FlowchartStep(
            step_id=step_id,
            step_type=step_type,
            name=name,
            stage_index=stage_idx,
            profile_count=profile_count
        )

    def _create_step_from_branch(self, step_id: str, step_data: dict, branch: dict, stage_idx: int) -> FlowchartStep:
        """Create a FlowchartStep from a decision point branch."""
        if branch.get('excludedPath'):
            name = 'Excluded Profiles'
        else:
            name = branch.get('name', f"Branch {branch.get('segmentId', '')}")

        # Get profile count for this branch
        profile_count = self._get_branch_profile_count(step_id, branch.get('segmentId'), stage_idx)

        return FlowchartStep(
            step_id=f"{step_id}_branch_{branch.get('segmentId', '')}",
            step_type='DecisionPoint_Branch',
            name=name,
            stage_index=stage_idx,
            profile_count=profile_count
        )

    def _create_step_from_variant(self, step_id: str, step_data: dict, variant: dict, stage_idx: int) -> FlowchartStep:
        """Create a FlowchartStep from an AB test variant."""
        name = variant.get('name', 'Unknown Variant')
        percentage = variant.get('percentage', 0)
        display_name = f"{name} ({percentage}%)"

        # Get profile count for this variant
        profile_count = self._get_variant_profile_count(step_id, variant.get('id'), stage_idx)

        return FlowchartStep(
            step_id=f"{step_id}_variant_{variant.get('id', '')}",
            step_type='ABTest_Variant',
            name=display_name,
            stage_index=stage_idx,
            profile_count=profile_count
        )

    def _get_step_display_name(self, step_data: dict) -> str:
        """Get display name for a step based on its type."""
        step_type = step_data.get('type', 'Unknown')

        if step_type == 'WaitStep':
            # Check the wait step type
            wait_step_type = step_data.get('waitStepType', 'Duration')

            if wait_step_type == 'Condition':
                step_name = step_data.get('name', 'Unknown Condition')
                return f'Wait: {step_name}'

            elif wait_step_type == 'Date':
                wait_until_date = step_data.get('waitUntilDate', 'Unknown Date')
                return f'Wait Until {wait_until_date}'

            elif wait_step_type == 'DaysOfTheWeek':
                days_of_week = step_data.get('waitUntilDaysOfTheWeek', [])
                if days_of_week:
                    # Map day numbers to day names (1=Monday, 2=Tuesday, etc.)
                    day_names = {
                        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
                        5: 'Friday', 6: 'Saturday', 7: 'Sunday'
                    }
                    day_list = [day_names.get(day, f'Day{day}') for day in days_of_week]
                    days_str = ', '.join(day_list)
                    return f'Wait Until {days_str}'
                else:
                    return 'Wait Until (No Days Specified)'

            else:
                # Duration-based wait step (default/legacy)
                wait_step = step_data.get('waitStep', 1)
                wait_unit = step_data.get('waitStepUnit', 'day')
                return f'Wait {wait_step} {wait_unit}'
        elif step_type == 'Activation':
            return step_data.get('name', 'Activation')
        elif step_type == 'Jump':
            return step_data.get('name', 'Jump')
        elif step_type == 'End':
            return 'End Step'
        elif step_type == 'DecisionPoint':
            return 'Decision Point'
        elif step_type == 'ABTest':
            return step_data.get('name', 'AB Test')
        else:
            return step_data.get('name', step_type)

    def _get_step_profile_count(self, step_id: str, stage_idx: int, step_type: str) -> int:
        """Get the number of profiles currently in a specific step."""
        # Convert step UUID format for column matching
        step_uuid = step_id.replace('-', '_')

        # Look for entry column for this step
        entry_column = f'intime_stage_{stage_idx}_{step_uuid}'

        if entry_column in self.profile_data.columns:
            # Get the corresponding outtime column
            outtime_column = entry_column.replace('intime_', 'outtime_')

            # Count profiles that have entered but not exited
            condition = self.profile_data[entry_column].notna()

            if outtime_column in self.profile_data.columns:
                # Exclude profiles that have exited (outtime is not null)
                condition = condition & self.profile_data[outtime_column].isna()

            return condition.sum()

        return 0

    def _get_branch_profile_count(self, step_id: str, segment_id: str, stage_idx: int) -> int:
        """Get the number of profiles currently in a decision point branch."""
        if not segment_id:
            return 0

        # Convert step UUID format for column matching
        step_uuid = step_id.replace('-', '_')

        # Look for branch entry column
        branch_column = f'intime_stage_{stage_idx}_{step_uuid}_{segment_id}'

        if branch_column in self.profile_data.columns:
            # Get the corresponding outtime column
            outtime_column = branch_column.replace('intime_', 'outtime_')

            # Count profiles that have entered but not exited
            condition = self.profile_data[branch_column].notna()

            if outtime_column in self.profile_data.columns:
                # Exclude profiles that have exited (outtime is not null)
                condition = condition & self.profile_data[outtime_column].isna()

            return condition.sum()

        return 0

    def _get_variant_profile_count(self, step_id: str, variant_id: str, stage_idx: int) -> int:
        """Get the number of profiles currently in an AB test variant."""
        if not variant_id:
            return 0

        # Convert UUIDs format for column matching
        step_uuid = step_id.replace('-', '_')
        variant_uuid = variant_id.replace('-', '_')

        # Look for variant entry column
        variant_column = f'intime_stage_{stage_idx}_{step_uuid}_variant_{variant_uuid}'

        if variant_column in self.profile_data.columns:
            # Get the corresponding outtime column
            outtime_column = variant_column.replace('intime_', 'outtime_')

            # Count profiles that have entered but not exited
            condition = self.profile_data[variant_column].notna()

            if outtime_column in self.profile_data.columns:
                # Exclude profiles that have exited (outtime is not null)
                condition = condition & self.profile_data[outtime_column].isna()

            return condition.sum()

        return 0

    def get_stage_profile_counts(self) -> Dict[int, int]:
        """Get profile counts for each stage (profiles currently in the stage)."""
        stage_counts = {}

        for stage_idx in range(len(self.stages)):
            entry_column = f'intime_stage_{stage_idx}'
            if entry_column in self.profile_data.columns:
                # Get the corresponding outtime column
                outtime_column = f'outtime_stage_{stage_idx}'

                # Count profiles that have entered but not exited the stage
                condition = self.profile_data[entry_column].notna()

                if outtime_column in self.profile_data.columns:
                    # Exclude profiles that have exited the stage (outtime is not null)
                    condition = condition & self.profile_data[outtime_column].isna()

                stage_counts[stage_idx] = condition.sum()
            else:
                stage_counts[stage_idx] = 0

        return stage_counts

    def get_journey_summary(self) -> Dict:
        """Get summary information about the journey."""
        total_profiles = len(self.profile_data) if not self.profile_data.empty else 0

        # Count profiles that entered the journey
        journey_entry_count = 0
        if 'intime_journey' in self.profile_data.columns:
            journey_entry_count = self.profile_data['intime_journey'].notna().sum()

        return {
            'journey_id': self.journey_id,
            'journey_name': self.journey_name,
            'audience_id': self.audience_id,
            'total_profiles': total_profiles,
            'journey_entry_count': journey_entry_count,
            'stage_count': len(self.stages),
            'stage_counts': self.get_stage_profile_counts()
        }

    def get_profiles_in_step(self, step_column: str) -> List[str]:
        """Get list of customer IDs for profiles currently in a specific step."""
        if step_column not in self.profile_data.columns:
            return []

        # Get the corresponding outtime column
        outtime_column = step_column.replace('intime_', 'outtime_')

        # Filter profiles that have entered (intime not null) but not exited (outtime is null)
        condition = self.profile_data[step_column].notna()

        if outtime_column in self.profile_data.columns:
            # Exclude profiles that have exited (outtime is not null)
            condition = condition & self.profile_data[outtime_column].isna()

        profiles_in_step = self.profile_data[condition]['cdp_customer_id'].tolist()

        return profiles_in_step