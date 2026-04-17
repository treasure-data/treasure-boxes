"""
Profile Timeline Service

This module provides the ProfileTimelineService class for querying and processing
customer journey timeline data from Treasure Data.
"""

import re
import math
import pytd
from typing import Dict, List, Optional, Tuple, Any

from ..utils.timeline_formatting import (
    TimelineEvent,
    create_timeline_event_from_column,
    sort_timeline_events,
    format_unix_timestamp
)
from .td_api import TDAPIService
from ..column_mapper import CJOColumnMapper
from ..utils.session_state import SessionStateManager


class ProfileTimelineService:
    """Service for querying and processing customer journey timeline data."""

    def __init__(self, td_api_service: TDAPIService, column_mapper: CJOColumnMapper):
        """
        Initialize timeline service.

        Args:
            td_api_service: TDAPIService instance for database queries
            column_mapper: CJOColumnMapper for display name conversion
        """
        self.td_api = td_api_service
        self.mapper = column_mapper

    def get_profile_timeline(
        self,
        journey_id: int,
        audience_id: int,
        customer_id: str,
        page: int = 0,
        page_size: int = 50
    ) -> Dict[str, Any]:
        """
        Fetch complete profile timeline with server-side pagination.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID
            customer_id: Customer ID to query
            page: Page number (0-based)
            page_size: Number of events per page

        Returns:
            Dictionary containing timeline events and pagination info
        """
        try:
            # Query main journey timeline data directly (discovers columns automatically)
            main_events, timeline_columns = self._query_main_timeline_with_discovery(
                journey_id, audience_id, customer_id
            )

            if not main_events:
                return {
                    'events': [],
                    'total_count': 0,
                    'total_pages': 0,
                    'current_page': page,
                    'error': 'No timeline data found for this customer'
                }

            print(f"DEBUG: Found {len(timeline_columns)} timeline columns from direct query")
            print(f"DEBUG: Timeline columns sample: {timeline_columns[:10]}...")

            # Query auxiliary tables for historical data
            aux_events = self._query_auxiliary_tables(journey_id, audience_id, customer_id)

            # Process and combine all events
            all_events = self._process_timeline_events(main_events, aux_events)

            # Sort events chronologically
            all_events = sort_timeline_events(all_events)

            # Apply pagination to processed events (client-side for now)
            total_count = len(all_events)
            total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
            start_idx = page * page_size
            end_idx = start_idx + page_size
            paginated_events = all_events[start_idx:end_idx]

            return {
                'events': paginated_events,
                'total_count': total_count,
                'total_pages': total_pages,
                'current_page': page,
                'all_events': all_events,  # For CSV export
                'error': None
            }

        except Exception as e:
            return self._handle_timeline_error(e, journey_id, audience_id, customer_id)


    def _query_main_timeline_with_discovery(
        self,
        journey_id: int,
        audience_id: int,
        customer_id: str
    ) -> Tuple[List[Dict], List[str]]:
        """
        Query main journey table for timeline data and discover timeline columns.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID
            customer_id: Customer ID

        Returns:
            Tuple of (timeline data rows, list of timeline column names)
        """
        try:
            # Create pytd client
            client = pytd.Client(
                apikey=self.td_api.api_key,
                endpoint='https://api.treasuredata.com',
                engine='presto'
            )

            table_name = f"cdp_audience_{audience_id}.journey_{journey_id}"

            # Simple query to get all data for this customer
            query = f"""
            SELECT *
            FROM {table_name}
            WHERE cdp_customer_id = '{customer_id}'
            """

            print(f"DEBUG: Querying all columns for customer {customer_id}")

            result = client.query(query)
            if not result or not result.get('data'):
                return [], []

            # Get all column names from the result
            all_columns = result.get('columns', [])

            # Filter to only timeline columns (intime_* and outtime_*)
            timeline_columns = [col for col in all_columns if col.startswith(('intime_', 'outtime_'))]

            print(f"DEBUG: Found {len(all_columns)} total columns, {len(timeline_columns)} timeline columns")

            # Convert result data to list of dictionaries
            rows = []
            for row_data in result['data']:
                row_dict = {}
                for i, col_name in enumerate(all_columns):
                    row_dict[col_name] = row_data[i] if i < len(row_data) else None
                rows.append(row_dict)

            return rows, timeline_columns

        except Exception as e:
            if "doesn't exist" in str(e).lower() or "not found" in str(e).lower():
                raise Exception(f"Journey table not found. The journey workflow may not have been run yet.")
            raise e

    def _query_auxiliary_tables(
        self,
        journey_id: int,
        audience_id: int,
        customer_id: str
    ) -> List[Dict]:
        """
        Query auxiliary tables with graceful error handling.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID
            customer_id: Customer ID

        Returns:
            List of auxiliary event data
        """
        aux_events = []
        aux_tables = ['jump_history', 'reentry_history', 'standby']

        # Create pytd client
        try:
            client = pytd.Client(
                apikey=self.td_api.api_key,
                endpoint='https://api.treasuredata.com',
                engine='presto'
            )
        except Exception:
            return aux_events  # Return empty if client creation fails

        for table_suffix in aux_tables:
            try:
                table_name = f"cdp_audience_{audience_id}.journey_{journey_id}_{table_suffix}"
                query = f"""
                SELECT *, '{table_suffix}' as event_source
                FROM {table_name}
                WHERE cdp_customer_id = '{customer_id}'
                """

                result = client.query(query)
                if result and result.get('data'):
                    # Convert list of lists to list of dictionaries using column names
                    columns = result.get('columns', [])
                    for row_data in result['data']:
                        row_dict = {}
                        for i, col_name in enumerate(columns):
                            row_dict[col_name] = row_data[i] if i < len(row_data) else None
                        aux_events.append(row_dict)

            except Exception:
                # Table doesn't exist or other error - continue silently
                continue

        return aux_events

    def _process_timeline_events(
        self,
        main_events: List[Dict],
        aux_events: List[Dict]
    ) -> List[TimelineEvent]:
        """
        Convert raw database rows to TimelineEvent objects.

        Args:
            main_events: Main journey table results
            aux_events: Auxiliary table results

        Returns:
            List of processed timeline events
        """
        events = []

        # Process main journey events
        for row in main_events:
            # Row should now be a dictionary from our conversion above
            if not isinstance(row, dict):
                continue

            for col_name, value in row.items():
                # Skip ISO formatted columns and non-timestamp columns
                if col_name.endswith('_iso') or col_name == 'cdp_customer_id':
                    continue

                # Process timeline columns
                if col_name.startswith(('intime_', 'outtime_')) and value is not None:
                    event = create_timeline_event_from_column(
                        column_name=col_name,
                        timestamp=value,
                        column_mapper=self.mapper,
                        event_source='main_journey',
                        row=row
                    )
                    if event:
                        events.append(event)

        # Process auxiliary events
        for aux_row in aux_events:
            event_source = aux_row.get('event_source', 'unknown')
            timestamp = aux_row.get('session_unixtime')

            if timestamp:
                # Create cross-journey event
                display_name = self._format_aux_event_name(aux_row)
                event = TimelineEvent(
                    timestamp=timestamp,
                    timestamp_iso=format_unix_timestamp(timestamp),
                    event_type='cross_journey',
                    display_name=display_name,
                    technical_name=f"{event_source}_event",
                    event_source=event_source,
                    metadata=aux_row
                )
                events.append(event)

        return events

    def _format_aux_event_name(self, aux_row: Dict) -> str:
        """
        Format auxiliary event display name.

        Args:
            aux_row: Auxiliary table row data

        Returns:
            Human-readable event name
        """
        event_source = aux_row.get('event_source', 'Unknown')
        reason = aux_row.get('reason', 'Unknown')

        source_map = {
            'jump_history': 'Journey Jump',
            'reentry_history': 'Journey Re-entry',
            'standby': 'Pending Jump'
        }

        source_name = source_map.get(event_source, event_source.title())

        if reason:
            return f"{source_name}: {reason.title()}"
        else:
            return source_name

    def _handle_timeline_error(
        self,
        error: Exception,
        journey_id: int,
        audience_id: int,
        customer_id: str
    ) -> Dict[str, Any]:
        """
        Handle timeline query errors with user-friendly messages.

        Args:
            error: Exception that occurred
            journey_id: Journey ID
            audience_id: Audience ID
            customer_id: Customer ID

        Returns:
            Error response dictionary
        """
        error_message = str(error).lower()

        if "doesn't exist" in error_message or "not found" in error_message:
            message = "Missing journey tables. The journey workflow may not have been run yet."
        elif "permission" in error_message or "denied" in error_message:
            message = "Permission denied. Check API key permissions."
        elif "timeout" in error_message:
            message = "Query timeout. Try reducing the page size or contact support."
        elif "no timeline columns" in error_message:
            message = f"No timeline data found for customer ID: {customer_id}"
        else:
            message = f"Error loading timeline: {str(error)}"

        return {
            'events': [],
            'total_count': 0,
            'total_pages': 0,
            'current_page': 0,
            'error': message
        }

    def get_customer_summary(
        self,
        journey_id: int,
        audience_id: int,
        customer_id: str
    ) -> Dict[str, Any]:
        """
        Get summary information for a customer's journey.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID
            customer_id: Customer ID

        Returns:
            Dictionary with customer journey summary
        """
        try:
            # Get full timeline
            timeline_result = self.get_profile_timeline(
                journey_id, audience_id, customer_id, page=0, page_size=1000
            )

            if timeline_result.get('error'):
                return {'error': timeline_result['error']}

            events = timeline_result.get('all_events', [])

            if not events:
                return {
                    'customer_id': customer_id,
                    'total_events': 0,
                    'journey_status': 'No timeline data',
                    'first_event': None,
                    'last_event': None
                }

            # Calculate summary statistics
            first_event = events[0]
            last_event = events[-1]

            # Determine journey status
            journey_status = 'In Progress'
            for event in events:
                if event.event_type == 'goal_achieved':
                    journey_status = 'Goal Achieved'
                    break
                elif event.event_type == 'journey_exit':
                    journey_status = 'Exited'

            return {
                'customer_id': customer_id,
                'total_events': len(events),
                'journey_status': journey_status,
                'first_event': {
                    'name': first_event.display_name,
                    'timestamp': first_event.timestamp_iso,
                    'type': first_event.event_type
                },
                'last_event': {
                    'name': last_event.display_name,
                    'timestamp': last_event.timestamp_iso,
                    'type': last_event.event_type
                }
            }

        except Exception as e:
            return {'error': f"Error getting customer summary: {str(e)}"}


def _extract_stage_index(column_name: str) -> Optional[int]:
    """Extract stage index from column name."""
    match = re.search(r'stage_(\d+)', column_name)
    return int(match.group(1)) if match else None


def _extract_step_uuid(column_name: str) -> Optional[str]:
    """Extract step UUID from column name."""
    pattern = r'stage_\d+_([a-f0-9_]+)'
    match = re.search(pattern, column_name)
    if match:
        uuid_part = match.group(1)
        if uuid_part not in ['milestone', 'exit'] and not uuid_part.startswith('exit_'):
            return uuid_part
    return None