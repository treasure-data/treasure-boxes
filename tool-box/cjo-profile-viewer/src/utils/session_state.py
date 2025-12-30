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


# Convenience functions for backward compatibility
def initialize_session_state():
    """Initialize session state - convenience function."""
    SessionStateManager.initialize()


def reset_journey_data():
    """Reset journey data - convenience function."""
    SessionStateManager.reset_journey_data()