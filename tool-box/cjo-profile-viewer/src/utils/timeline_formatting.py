"""
Timeline Formatting Utilities

This module provides utilities for formatting timeline events, timestamps,
and durations for the Profile Timeline feature.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple


@dataclass
class TimelineEvent:
    """Represents a single timeline event in a customer journey."""
    timestamp: Optional[int] = None  # Unix timestamp
    timestamp_iso: Optional[str] = None  # ISO format timestamp
    event_type: str = 'unknown'  # 'entry', 'exit', 'milestone', 'goal', 'cross_journey'
    display_name: str = ''  # Human-readable event name
    technical_name: str = ''  # Original column name
    stage_index: Optional[int] = None
    step_uuid: Optional[str] = None
    event_source: str = 'main_journey'  # 'main_journey', 'jump_history', etc.
    metadata: Optional[Dict] = None  # Additional event metadata
    step_intime: Optional[int] = None  # intime of this step (used for within-group ordering)
    step_outtime: Optional[int] = None  # outtime of this step (used as tiebreaker)


def format_unix_timestamp(timestamp: Optional[int]) -> str:
    """
    Convert Unix timestamp to ISO format string.

    Args:
        timestamp: Unix timestamp (seconds since epoch)

    Returns:
        ISO format timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    if timestamp is None:
        return ""

    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "Invalid timestamp"




def extract_stage_index(column_name: str) -> Optional[int]:
    """
    Extract stage index from column name.

    Args:
        column_name: Technical column name (e.g., "intime_stage_2")

    Returns:
        Stage index or None if not found
    """
    match = re.search(r'stage_(\d+)', column_name)
    if match:
        return int(match.group(1))
    return None


def extract_step_uuid(column_name: str) -> Optional[str]:
    """
    Extract step UUID from column name.

    Args:
        column_name: Technical column name (e.g., "intime_stage_0_abc123def")

    Returns:
        Step UUID or None if not found
    """
    # Look for UUID pattern after stage index
    pattern = r'stage_\d+_([a-f0-9_]+)'
    match = re.search(pattern, column_name)
    if match:
        uuid_part = match.group(1)
        # Filter out common suffixes that aren't UUIDs
        if uuid_part not in ['milestone', 'exit'] and not uuid_part.startswith('exit_'):
            return uuid_part
    return None


def get_event_icon(event_type: str) -> str:
    """
    Get appropriate icon for timeline event type.

    Args:
        event_type: Type of timeline event

    Returns:
        Unicode icon string
    """
    icon_map = {
        'journey_entry': '🏁',
        'journey_exit': '🏁',
        'stage_entry': '📍',
        'stage_exit': '📍',
        'step_entry': '▶️',
        'step_exit': '⏹️',
        'milestone': '🏆',
        'goal_achieved': '🎯',
        'cross_journey': '🔀',
        'unknown': '❓'
    }
    return icon_map.get(event_type, '❓')


def get_event_color(event_type: str) -> str:
    """
    Get color code for timeline event type.

    Args:
        event_type: Type of timeline event

    Returns:
        CSS color code
    """
    color_map = {
        'journey_entry': '#4CAF50',  # Green
        'journey_exit': '#f44336',   # Red
        'stage_entry': '#2196F3',    # Blue
        'stage_exit': '#2196F3',     # Blue
        'step_entry': '#FF9800',     # Orange
        'step_exit': '#FF9800',      # Orange
        'milestone': '#9C27B0',      # Purple
        'goal_achieved': '#4CAF50',  # Green
        'cross_journey': '#795548',  # Brown
        'unknown': '#9E9E9E'         # Grey
    }
    return color_map.get(event_type, '#9E9E9E')


def sort_timeline_events(events: List[TimelineEvent]) -> List[TimelineEvent]:
    """
    Sort timeline events chronologically.

    Args:
        events: List of timeline events

    Returns:
        Sorted list of events (earliest first)
    """
    return sorted(events, key=lambda event: event.timestamp or 0)




def create_timeline_event_from_column(
    column_name: str,
    timestamp: Optional[int],
    column_mapper,
    event_source: str = 'main_journey',
    row: Optional[Dict] = None
) -> Optional[TimelineEvent]:
    """
    Create a TimelineEvent from a database column.

    Args:
        column_name: Technical column name
        timestamp: Unix timestamp value
        column_mapper: CJOColumnMapper instance for display name conversion
        event_source: Source of the event (main_journey, jump_history, etc.)
        row: Full row dict from the journey table (used to look up step intime/outtime)

    Returns:
        TimelineEvent instance or None if invalid
    """
    if timestamp is None:
        return None

    # Determine event type from column name.
    # Stage-level columns are exactly intime_stage_N or outtime_stage_N (no UUID suffix).
    # Step-level columns have a UUID after the stage index: intime_stage_N_<uuid...>
    _is_stage_level = bool(re.match(r'^(intime|outtime)_stage_\d+$', column_name))

    event_type = 'unknown'
    if column_name.startswith('intime_'):
        if 'goal' in column_name:
            event_type = 'goal_achieved'
        elif 'milestone' in column_name:
            event_type = 'milestone'
        elif column_name == 'intime_journey':
            event_type = 'journey_entry'
        elif _is_stage_level:
            event_type = 'stage_entry'
        else:
            event_type = 'step_entry'
    elif column_name.startswith('outtime_'):
        if column_name == 'outtime_journey':
            event_type = 'journey_exit'
        elif _is_stage_level:
            event_type = 'stage_exit'
        else:
            event_type = 'step_exit'
    elif event_source != 'main_journey':
        event_type = 'cross_journey'

    # Get display name using column mapper
    try:
        display_name = column_mapper.get_timeline_display_name(column_name)
    except:
        # Fallback if mapper fails
        display_name = column_name.replace('_', ' ').title()

    # Resolve step_intime and step_outtime from the row for within-group ordering.
    # For an intime_ column, intime = timestamp itself; for an outtime_ column,
    # look up the corresponding intime_ column in the row.
    step_intime = None
    step_outtime = None
    if column_name.startswith('intime_'):
        step_intime = timestamp
        if row is not None:
            outtime_col = 'outtime_' + column_name[len('intime_'):]
            step_outtime = row.get(outtime_col)
    elif column_name.startswith('outtime_'):
        step_outtime = timestamp  # the exit IS the outtime
        if row is not None:
            intime_col = 'intime_' + column_name[len('outtime_'):]
            step_intime = row.get(intime_col)
        # If intime not found, fall back to the exit timestamp itself as a safe lower bound
        if step_intime is None:
            step_intime = timestamp

    return TimelineEvent(
        timestamp=timestamp,
        timestamp_iso=format_unix_timestamp(timestamp),
        event_type=event_type,
        display_name=display_name,
        technical_name=column_name,
        stage_index=extract_stage_index(column_name),
        step_uuid=extract_step_uuid(column_name),
        event_source=event_source,
        step_intime=step_intime,
        step_outtime=step_outtime
    )


def group_events_by_exact_timestamp(events: List[TimelineEvent]) -> Dict[str, List[TimelineEvent]]:
    """
    Group timeline events by their exact unix timestamp for hierarchical display.

    Args:
        events: List of timeline events

    Returns:
        Dictionary mapping timestamp strings to event lists, sorted hierarchically
    """
    groups = {}

    for event in events:
        if event.timestamp:
            # Group by exact timestamp
            timestamp_key = event.timestamp_iso or format_unix_timestamp(event.timestamp)

            if timestamp_key not in groups:
                groups[timestamp_key] = []
            groups[timestamp_key].append(event)

    # Sort events within each timestamp group hierarchically
    for timestamp_key in groups:
        groups[timestamp_key] = sort_events_hierarchically(groups[timestamp_key])

    return groups


def sort_events_hierarchically(events: List[TimelineEvent]) -> List[TimelineEvent]:
    """
    Sort events within a timestamp group by causal order using step timestamps.

    For exit events, the sort key is the step's intime — an exit is caused by the
    step that was entered earliest, so it comes first.

    For entry events, the sort key is the step's outtime — steps that exit sooner
    (shorter duration) come after steps that are still ongoing (null outtime = MAX),
    because ongoing steps (journey, stage) are outer containers that were entered
    first in the logical sequence. When outtime is also tied, level breaks the tie:
    journey before stage before step.

    Combined key per event: (step_intime, is_exit_as_entry_anchor, outtime_for_entries, level)

    Concretely the key is (step_intime, is_exit, step_outtime_or_MAX, level):
    - Exits sort by their step_intime first (earlier-entered steps exit first)
    - Entries sort after exits of earlier steps, then by outtime ascending so that
      instantaneous steps (same intime+outtime) group together before longer steps,
      with level as final tiebreaker for same-outtime entries.

    Args:
        events: List of timeline events with the same timestamp

    Returns:
        List of events sorted in causal order
    """
    if len(events) <= 1:
        return events

    _MAX = 2 ** 31

    def event_level(event: TimelineEvent) -> int:
        if 'journey' in event.event_type:
            return 0
        elif 'stage' in event.event_type:
            return 1
        else:
            return 2

    def sort_key(event: TimelineEvent) -> tuple:
        intime = event.step_intime if event.step_intime is not None else _MAX
        is_exit = 1 if 'exit' in event.event_type else 0
        level = event_level(event)
        outtime = event.step_outtime if event.step_outtime is not None else _MAX

        if level < 2:
            # Journey and stage events are outer containers — always sort before
            # step-level events. Use (intime, is_exit, level) only.
            return (intime, is_exit, level, 0)
        else:
            # Step-level events: pair entry+exit of the same step by using
            # (step_intime, step_outtime, is_exit) so they group together.
            # A step entered earlier (smaller intime) exits before a newer step
            # is entered; within the same intime+outtime, entry (0) before exit (1).
            return (intime, outtime, is_exit, level)

    sorted_events = sorted(events, key=sort_key)
    print(f"DEBUG sort_events_hierarchically group:")
    for e in sorted_events:
        k = sort_key(e)
        print(f"  key={k} | {e.display_name} | step_intime={e.step_intime} step_outtime={e.step_outtime}")
    return sorted_events


def group_events_by_timeframe(events: List[TimelineEvent],
                            hours: int = 24) -> Dict[str, List[TimelineEvent]]:
    """
    Group timeline events by timeframe for easier visualization.

    Args:
        events: List of timeline events
        hours: Number of hours per group (default 24 for daily grouping)

    Returns:
        Dictionary mapping date strings to event lists
    """
    groups = {}

    for event in events:
        if event.timestamp:
            dt = datetime.fromtimestamp(event.timestamp)
            # Group by date if daily grouping (24 hours)
            if hours == 24:
                date_key = dt.strftime("%Y-%m-%d")
            else:
                # Custom hour grouping
                date_key = dt.strftime(f"%Y-%m-%d %H:00")

            if date_key not in groups:
                groups[date_key] = []
            groups[date_key].append(event)

    return groups