"""
Timeline Renderer Components

This module provides components for rendering customer journey timelines
in the Profile Timeline feature.
"""

import streamlit as st
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..utils.timeline_formatting import (
    TimelineEvent,
    get_event_icon,
    get_event_color,
    group_events_by_exact_timestamp
)


def render_timeline_events(
    events: List[TimelineEvent],
    show_technical_names: bool = False
) -> None:
    """
    Render timeline events as a styled timeline grouped by exact timestamp.

    Args:
        events: List of timeline events to render
        show_technical_names: Whether to show technical column names
    """
    if not events:
        st.info("No timeline events found for this customer.")
        return

    # Group events by exact timestamp
    grouped_events = group_events_by_exact_timestamp(events)

    # Create timeline HTML
    timeline_html = create_grouped_timeline_html(
        grouped_events,
        show_technical_names=show_technical_names
    )

    # Render with custom CSS
    st.markdown(get_timeline_css(), unsafe_allow_html=True)
    st.markdown(timeline_html, unsafe_allow_html=True)


def create_grouped_timeline_html(
    grouped_events: Dict[str, List[TimelineEvent]],
    show_technical_names: bool = False
) -> str:
    """
    Generate HTML for grouped timeline visualization.

    Args:
        grouped_events: Dictionary mapping timestamps to event lists
        show_technical_names: Whether to show technical column names

    Returns:
        HTML string for grouped timeline visualization
    """
    if not grouped_events:
        return '<div class="timeline-container">No events to display</div>'

    html_parts = ['<div class="timeline-container">']

    # Sort timestamp keys chronologically
    sorted_timestamps = sorted(grouped_events.keys(), key=lambda ts: _parse_timestamp_for_sorting(ts))

    for timestamp in sorted_timestamps:
        events = grouped_events[timestamp]
        if not events:
            continue

        # Add timestamp header
        html_parts.append(f'<div class="timestamp-group">')
        html_parts.append(f'<div class="timestamp-header">{timestamp}</div>')
        html_parts.append('<div class="events-list">')

        # Add each event in hierarchical order (already sorted by group_events_by_exact_timestamp)
        for i, event in enumerate(events):
            event_html = create_grouped_event_html(
                event,
                show_technical_name=show_technical_names,
                is_first_in_group=i == 0
            )
            html_parts.append(event_html)

        html_parts.append('</div>')  # Close events-list
        html_parts.append('</div>')  # Close timestamp-group

    html_parts.append('</div>')  # Close timeline-container
    return '\n'.join(html_parts)


def _parse_timestamp_for_sorting(timestamp_str: str) -> int:
    """Parse timestamp string for sorting purposes."""
    try:
        # Try to parse as datetime and convert to unix timestamp
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except:
        # Fallback: return 0 for sorting
        return 0


def create_timeline_html(
    events: List[TimelineEvent],
    show_technical_names: bool = False
) -> str:
    """
    Generate HTML for timeline visualization (legacy function for backward compatibility).

    Args:
        events: List of timeline events
        show_technical_names: Whether to show technical column names

    Returns:
        HTML string for timeline visualization
    """
    html_parts = ['<div class="timeline-container">']

    for i, event in enumerate(events):
        event_html = create_event_html(
            event,
            show_technical_name=show_technical_names,
            is_first=i == 0,
            is_last=i == len(events) - 1
        )
        html_parts.append(event_html)

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def create_grouped_event_html(
    event: TimelineEvent,
    show_technical_name: bool = False,
    is_first_in_group: bool = False
) -> str:
    """
    Create HTML for a single timeline event in a grouped display.

    Args:
        event: Timeline event to render
        show_technical_name: Whether to show technical column name in parentheses
        is_first_in_group: Whether this is the first event in the timestamp group

    Returns:
        HTML string for the event
    """
    # Split "Enter - ..." or "Exit - ..." into styled prefix and label
    display_name = event.display_name
    if display_name.startswith("Enter - "):
        prefix_html = '<span class="event-prefix event-enter">Enter</span>'
        label = display_name[len("Enter - "):]
    elif display_name.startswith("Exit - "):
        prefix_html = '<span class="event-prefix event-exit">Exit</span>'
        label = display_name[len("Exit - "):]
    else:
        prefix_html = ""
        label = display_name

    technical_html = ""
    if show_technical_name and event.technical_name:
        technical_html = f' <code class="event-technical">{event.technical_name}</code>'

    event_text = f'{prefix_html}<span class="event-label"> - {label}</span>{technical_html}' if prefix_html else f'<span class="event-label">{label}</span>{technical_html}'

    html_parts = [
        '<div class="grouped-event">',
        f'  <span class="event-bullet">•</span>',
        f'  <span class="event-text">{event_text}</span>',
        '</div>'
    ]

    return '\n'.join(html_parts)


def create_event_html(
    event: TimelineEvent,
    show_technical_name: bool = False,
    is_first: bool = False,
    is_last: bool = False
) -> str:
    """
    Create HTML for a single timeline event (legacy format for backward compatibility).

    Args:
        event: Timeline event to render
        show_technical_name: Whether to show technical column name
        is_first: Whether this is the first event
        is_last: Whether this is the last event

    Returns:
        HTML string for the event
    """
    icon = get_event_icon(event.event_type)
    color = get_event_color(event.event_type)
    timestamp_str = event.timestamp_iso or "Unknown time"

    # Build display name with technical name in parentheses if requested
    display_name = event.display_name
    if show_technical_name and event.technical_name:
        display_name = f"{event.display_name} ({event.technical_name})"

    # Build event HTML
    html_parts = [
        f'<div class="timeline-event {event.event_type}">',
        f'  <div class="timeline-marker" style="background-color: {color};">',
        f'    <span class="timeline-icon">{icon}</span>',
        '  </div>',
        '  <div class="timeline-content">',
        f'    <div class="timeline-title">{display_name}</div>',
        f'    <div class="timeline-timestamp">{timestamp_str}</div>'
    ]

    # Add metadata for cross-journey events
    if event.event_source != 'main_journey' and event.metadata:
        metadata_html = create_metadata_html(event.metadata)
        if metadata_html:
            html_parts.append(f'    <div class="timeline-metadata">{metadata_html}</div>')

    html_parts.extend([
        '  </div>',
        '</div>'
    ])

    return '\n'.join(html_parts)


def create_metadata_html(metadata: Dict[str, Any]) -> str:
    """
    Create HTML for event metadata.

    Args:
        metadata: Event metadata dictionary

    Returns:
        HTML string for metadata display
    """
    if not metadata:
        return ""

    html_parts = []

    # Show relevant metadata fields
    if metadata.get('reason'):
        html_parts.append(f"Reason: {metadata['reason']}")

    if metadata.get('target_journey_id'):
        html_parts.append(f"Target Journey: {metadata['target_journey_id']}")

    if metadata.get('source_journey_id'):
        html_parts.append(f"Source Journey: {metadata['source_journey_id']}")

    if html_parts:
        return '<br>'.join(html_parts)

    return ""


def get_timeline_css() -> str:
    """
    Get CSS styles for timeline visualization.

    Returns:
        CSS string for timeline styling
    """
    return """
    <style>
    .timeline-container {
        padding: 20px 0;
        margin: 20px 0;
        width: fit-content;
        min-width: 300px;
    }

    /* Grouped timeline styles */
    .timestamp-group {
        display: block;
        width: 100%;
        margin-bottom: 30px;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #007bff;
        box-sizing: border-box;
    }

    .timestamp-header {
        font-weight: 600;
        font-size: 16px;
        color: #495057;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #dee2e6;
    }

    .events-list {
        margin-left: 16px;
    }

    .grouped-event {
        display: flex;
        align-items: flex-start;
        margin-bottom: 6px;
        padding: 4px 0;
    }

    .event-bullet {
        color: #007bff;
        font-weight: bold;
        margin-right: 8px;
        margin-top: 2px;
        font-size: 16px;
        line-height: 1;
    }

    .event-text {
        color: #495057;
        line-height: 1.4;
        flex: 1;
    }

    .event-prefix {
        font-weight: bold;
    }

    .event-enter {
        color: #2e7d32;
    }

    .event-exit {
        color: #c62828;
    }

    .event-label {
        color: #495057;
    }

    .event-technical {
        font-size: 11px;
        font-family: monospace;
        background: #e9ecef;
        color: #6c757d;
        padding: 1px 5px;
        border-radius: 3px;
        font-weight: normal;
    }

    /* Legacy timeline styles for backward compatibility */
    .timeline-event {
        position: relative;
        display: flex;
        align-items: flex-start;
        margin-bottom: 30px;
        padding-left: 60px;
    }

    .timeline-event:not(:last-child)::after {
        content: '';
        position: absolute;
        left: 19px;
        top: 40px;
        bottom: -30px;
        width: 2px;
        background-color: #e0e0e0;
    }

    .timeline-marker {
        position: absolute;
        left: 0;
        top: 0;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 2;
    }

    .timeline-icon {
        font-size: 16px;
        line-height: 1;
    }

    .timeline-content {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-left: 20px;
        flex: 1;
    }

    .timeline-title {
        font-weight: 600;
        font-size: 16px;
        color: #333;
        margin-bottom: 6px;
    }

    .timeline-timestamp {
        font-size: 14px;
        color: #666;
        font-family: monospace;
        margin-bottom: 4px;
    }


    .timeline-technical {
        font-size: 12px;
        color: #999;
        font-family: monospace;
        margin-top: 6px;
        background: #f5f5f5;
        padding: 4px 8px;
        border-radius: 4px;
    }

    .timeline-metadata {
        font-size: 12px;
        color: #666;
        margin-top: 8px;
        padding: 8px;
        background: #f9f9f9;
        border-radius: 4px;
        border-left: 3px solid #ddd;
    }

    /* Event type specific colors */
    .timeline-event.journey_entry .timeline-marker {
        background-color: #4CAF50;
    }

    .timeline-event.journey_exit .timeline-marker {
        background-color: #f44336;
    }

    .timeline-event.stage_entry .timeline-marker {
        background-color: #2196F3;
    }

    .timeline-event.stage_exit .timeline-marker {
        background-color: #2196F3;
    }

    .timeline-event.step_entry .timeline-marker {
        background-color: #FF9800;
    }

    .timeline-event.step_exit .timeline-marker {
        background-color: #FF9800;
    }

    .timeline-event.milestone .timeline-marker {
        background-color: #9C27B0;
    }

    .timeline-event.goal_achieved .timeline-marker {
        background-color: #4CAF50;
    }

    .timeline-event.cross_journey .timeline-marker {
        background-color: #795548;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .timeline-event {
            padding-left: 50px;
        }

        .timeline-marker {
            width: 32px;
            height: 32px;
        }

        .timeline-icon {
            font-size: 14px;
        }

        .timeline-content {
            margin-left: 15px;
            padding: 12px;
        }

        .timeline-title {
            font-size: 15px;
        }

        .timeline-timestamp {
            font-size: 13px;
        }

        .timestamp-group {
            padding: 12px;
        }

        .timestamp-header {
            font-size: 15px;
        }

        .events-list {
            margin-left: 12px;
        }
    }
    </style>
    """


def render_timeline_summary(
    events: List[TimelineEvent],
    customer_id: str
) -> None:
    """
    Render a summary of the timeline.

    Args:
        events: List of timeline events
        customer_id: Customer ID
    """
    if not events:
        return

    # Calculate summary statistics
    first_event = events[0]
    last_event = events[-1]

    # Determine journey status
    journey_status = "In Progress"
    status_color = "🟡"

    for event in events:
        if event.event_type == 'goal_achieved':
            journey_status = "Goal Achieved"
            status_color = "🟢"
            break
        elif event.event_type == 'journey_exit':
            journey_status = "Exited"
            status_color = "🔴"

    # Display summary in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Customer ID", customer_id)

    with col2:
        st.metric("Total Events", len(events))

    with col3:
        st.metric("Journey Status", f"{status_color} {journey_status}")

    # Show first and last events
    if len(events) > 1:
        st.markdown("### Timeline Range")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**First Event**")
            st.write(f"📅 {first_event.timestamp_iso}")
            st.write(f"🎯 {first_event.display_name}")

        with col2:
            st.markdown("**Last Event**")
            st.write(f"📅 {last_event.timestamp_iso}")
            st.write(f"🎯 {last_event.display_name}")


def render_pagination_controls(
    current_page: int,
    total_pages: int,
    page_size: int,
    total_count: int,
    on_page_change: callable,
    on_page_size_change: callable
) -> None:
    """
    Render pagination controls for timeline.

    Args:
        current_page: Current page number (0-based)
        total_pages: Total number of pages
        page_size: Current page size
        total_count: Total number of events
        on_page_change: Callback for page change
        on_page_size_change: Callback for page size change
    """
    if total_pages <= 1:
        return

    st.markdown("---")

    # Create pagination controls
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    with col1:
        if st.button("← Previous", disabled=(current_page == 0)):
            on_page_change(current_page - 1)

    with col2:
        st.write(f"Page {current_page + 1} of {total_pages}")

    with col3:
        # Show total count
        start_idx = current_page * page_size + 1
        end_idx = min((current_page + 1) * page_size, total_count)
        st.write(f"Showing {start_idx}-{end_idx} of {total_count} events")

    with col4:
        if st.button("Next →", disabled=(current_page >= total_pages - 1)):
            on_page_change(current_page + 1)

    with col5:
        new_page_size = st.selectbox(
            "Per page",
            options=[25, 50, 100, 200],
            index=[25, 50, 100, 200].index(page_size) if page_size in [25, 50, 100, 200] else 1,
            key="timeline_page_size_select"
        )
        if new_page_size != page_size:
            on_page_size_change(new_page_size)


def render_timeline_filters(
    events: List[TimelineEvent],
    on_filter_change: callable
) -> Dict[str, Any]:
    """
    Render timeline filtering controls.

    Args:
        events: All timeline events for filter options
        on_filter_change: Callback when filters change

    Returns:
        Dictionary of current filter values
    """
    if not events:
        return {}

    st.markdown("### Timeline Filters")

    # Get unique event types
    event_types = list(set(event.event_type for event in events))
    event_sources = list(set(event.event_source for event in events))

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_types = st.multiselect(
            "Event Types",
            options=event_types,
            default=event_types,
            key="timeline_event_type_filter"
        )

    with col2:
        selected_sources = st.multiselect(
            "Event Sources",
            options=event_sources,
            default=event_sources,
            key="timeline_event_source_filter"
        )

    with col3:
        # Date range filter
        timestamps = [event.timestamp for event in events if event.timestamp]
        if timestamps:
            min_date = datetime.fromtimestamp(min(timestamps)).date()
            max_date = datetime.fromtimestamp(max(timestamps)).date()

            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="timeline_date_filter"
            )
        else:
            date_range = None

    filters = {
        'event_types': selected_types,
        'event_sources': selected_sources,
        'date_range': date_range
    }

    # Call filter change callback
    on_filter_change(filters)

    return filters


def apply_timeline_filters(
    events: List[TimelineEvent],
    filters: Dict[str, Any]
) -> List[TimelineEvent]:
    """
    Apply filters to timeline events.

    Args:
        events: List of timeline events
        filters: Filter criteria dictionary

    Returns:
        Filtered list of timeline events
    """
    if not events or not filters:
        return events

    filtered_events = events

    # Filter by event types
    if filters.get('event_types'):
        filtered_events = [
            event for event in filtered_events
            if event.event_type in filters['event_types']
        ]

    # Filter by event sources
    if filters.get('event_sources'):
        filtered_events = [
            event for event in filtered_events
            if event.event_source in filters['event_sources']
        ]

    # Filter by date range
    date_range = filters.get('date_range')
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())
        end_timestamp = int(datetime.combine(end_date, datetime.max.time()).timestamp())

        filtered_events = [
            event for event in filtered_events
            if event.timestamp and start_timestamp <= event.timestamp <= end_timestamp
        ]

    return filtered_events