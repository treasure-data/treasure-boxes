"""
Session State Management

This module provides utilities for managing Streamlit session state.
"""

import streamlit as st
from typing import Any, Dict, Optional


class SessionStateManager:
    """Manages Streamlit session state with default values and validation."""

    # Default session state values
    DEFAULTS = {
        'api_response': None,
        'profile_data': None,
        'journey_loaded': False,
        'config_loaded': False,
        'available_attributes': {},
        'selected_attributes': [],
        'auto_load_attempted': False,

        # Timeline-specific state
        'timeline_data': None,
        'timeline_pagination': {'page': 0, 'page_size': 50},
        'timeline_customer_id': '',
        'cached_timeline_columns': {},
        'timeline_loading': False,
        'timeline_error': None,
        'timeline_export_data': None,
        'timeline_summary': None,
    }

    @classmethod
    def initialize(cls) -> None:
        """Initialize all session state variables with default values."""
        for key, default_value in cls.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get a value from session state with optional default.

        Args:
            key: Session state key
            default: Default value if key doesn't exist

        Returns:
            Value from session state or default
        """
        if default is None:
            default = cls.DEFAULTS.get(key)
        return st.session_state.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a value in session state.

        Args:
            key: Session state key
            value: Value to set
        """
        st.session_state[key] = value

    @classmethod
    def reset_journey_data(cls) -> None:
        """Reset journey-related session state."""
        cls.set('api_response', None)
        cls.set('profile_data', None)
        cls.set('journey_loaded', False)
        cls.set('config_loaded', False)
        cls.set('available_attributes', {})
        cls.set('selected_attributes', [])

    @classmethod
    def is_config_loaded(cls) -> bool:
        """Check if journey configuration is loaded."""
        return cls.get('config_loaded', False) and cls.get('api_response') is not None

    @classmethod
    def is_journey_loaded(cls) -> bool:
        """Check if complete journey data is loaded."""
        return (cls.get('journey_loaded', False) and
                cls.get('api_response') is not None and
                cls.get('profile_data') is not None)

    @classmethod
    def get_journey_id(cls) -> Optional[str]:
        """Get journey ID from loaded configuration."""
        api_response = cls.get('api_response')
        if api_response:
            return api_response.get('data', {}).get('id')
        return None

    @classmethod
    def get_audience_id(cls) -> Optional[str]:
        """Get audience ID from loaded configuration."""
        api_response = cls.get('api_response')
        if api_response:
            return api_response.get('data', {}).get('attributes', {}).get('audienceId')
        return None

    @classmethod
    def set_config_loaded(cls, api_response: Dict, audience_id: str, available_attributes: list) -> None:
        """
        Set configuration as loaded with all required data.

        Args:
            api_response: Journey API response
            audience_id: Audience ID
            available_attributes: List of available customer attributes
        """
        cls.set('api_response', api_response)
        cls.set('config_loaded', True)

        # Store available attributes
        if 'available_attributes' not in st.session_state:
            st.session_state['available_attributes'] = {}
        st.session_state['available_attributes'][audience_id] = available_attributes

        # Reset profile-related state
        cls.set('profile_data', None)
        cls.set('journey_loaded', False)

        # Clear existing Profile Timeline data when new journey config is loaded
        cls.reset_timeline_state()

    @classmethod
    def set_profile_loaded(cls, profile_data: Any) -> None:
        """
        Set profile data as loaded.

        Args:
            profile_data: Profile DataFrame
        """
        cls.set('profile_data', profile_data)
        cls.set('journey_loaded', True)

    @classmethod
    def get_available_attributes(cls, audience_id: str) -> list:
        """
        Get available attributes for a specific audience.

        Args:
            audience_id: Audience ID

        Returns:
            List of available attributes
        """
        available_attrs = cls.get('available_attributes', {})
        return available_attrs.get(audience_id, [])

    # Timeline-specific methods

    @classmethod
    def reset_timeline_state(cls) -> None:
        """Reset all timeline-related session state."""
        timeline_keys = [k for k in cls.DEFAULTS.keys() if k.startswith('timeline_')]
        for key in timeline_keys:
            cls.set(key, cls.DEFAULTS[key])

    @classmethod
    def get_timeline_pagination(cls) -> Dict[str, int]:
        """Get current timeline pagination settings."""
        return cls.get('timeline_pagination', cls.DEFAULTS['timeline_pagination'].copy())

    @classmethod
    def set_timeline_page(cls, page: int) -> None:
        """Update timeline pagination page."""
        pagination = cls.get_timeline_pagination()
        pagination['page'] = max(0, page)
        cls.set('timeline_pagination', pagination)

    @classmethod
    def set_timeline_page_size(cls, page_size: int) -> None:
        """Update timeline pagination page size."""
        pagination = cls.get_timeline_pagination()
        pagination['page_size'] = max(1, page_size)
        pagination['page'] = 0  # Reset to first page when changing page size
        cls.set('timeline_pagination', pagination)

    @classmethod
    def is_timeline_loaded(cls) -> bool:
        """Check if timeline data is loaded."""
        return cls.get('timeline_data') is not None and not cls.get('timeline_error')

    @classmethod
    def set_timeline_loading(cls, loading: bool) -> None:
        """Set timeline loading state."""
        cls.set('timeline_loading', loading)
        if loading:
            cls.set('timeline_error', None)

    @classmethod
    def set_timeline_data(cls, timeline_data: Dict, customer_id: str) -> None:
        """
        Set timeline data as loaded.

        Args:
            timeline_data: Timeline data dictionary
            customer_id: Customer ID for this timeline
        """
        cls.set('timeline_data', timeline_data)
        cls.set('timeline_customer_id', customer_id)
        cls.set('timeline_loading', False)
        cls.set('timeline_error', None)

        # Store export data (all events for CSV export)
        if 'all_events' in timeline_data:
            cls.set('timeline_export_data', timeline_data['all_events'])

    @classmethod
    def set_timeline_error(cls, error_message: str) -> None:
        """Set timeline error state."""
        cls.set('timeline_error', error_message)
        cls.set('timeline_loading', False)
        cls.set('timeline_data', None)

    @classmethod
    def get_timeline_customer_id(cls) -> str:
        """Get current timeline customer ID."""
        return cls.get('timeline_customer_id', '')

    @classmethod
    def cache_timeline_columns(cls, journey_id: int, audience_id: int, columns: list) -> None:
        """
        Cache timeline columns for a journey/audience combination.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID
            columns: List of timeline column names
        """
        cache_key = f"timeline_columns_{journey_id}_{audience_id}"
        cached_columns = cls.get('cached_timeline_columns', {})
        cached_columns[cache_key] = columns
        cls.set('cached_timeline_columns', cached_columns)

    @classmethod
    def get_cached_timeline_columns(cls, journey_id: int, audience_id: int) -> Optional[list]:
        """
        Get cached timeline columns for a journey/audience combination.

        Args:
            journey_id: Journey ID
            audience_id: Audience ID

        Returns:
            List of cached column names or None if not cached
        """
        cache_key = f"timeline_columns_{journey_id}_{audience_id}"
        cached_columns = cls.get('cached_timeline_columns', {})
        return cached_columns.get(cache_key)


# Convenience functions for backward compatibility
def initialize_session_state():
    """Initialize session state - convenience function."""
    SessionStateManager.initialize()


def reset_journey_data():
    """Reset journey data - convenience function."""
    SessionStateManager.reset_journey_data()