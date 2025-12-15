"""
Treasure Data API Service

This module handles all interactions with the Treasure Data APIs including:
- Journey configuration retrieval
- Profile data querying
- Customer attribute discovery
- API key management
"""

import streamlit as st
import pandas as pd
import requests
import os
import pytd
from typing import Dict, List, Optional, Tuple


class TDAPIService:
    """Service class for Treasure Data API interactions."""

    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self) -> Optional[str]:
        """Get TD API key from environment variable or config file."""
        # First try environment variable
        api_key = os.getenv('TD_API_KEY')
        if api_key:
            return api_key

        # Try to read from config file
        config_paths = [
            os.path.expanduser('~/.td/config'),
            'td_config.txt',
            '.env'
        ]

        for config_path in config_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        for line in f:
                            if line.startswith('TD_API_KEY=') or line.startswith('apikey='):
                                return line.split('=', 1)[1].strip()
            except Exception:
                continue

        return None

    def fetch_journey_data(self, journey_id: str) -> Tuple[Optional[dict], Optional[str]]:
        """Fetch journey data from TD API."""
        if not journey_id or not self.api_key:
            return None, "Journey ID and API key are required"

        url = f"https://api-cdp.treasuredata.com/entities/journeys/{journey_id}"
        headers = {
            'Authorization': f'TD1 {self.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            with st.spinner(f"Fetching journey data for ID: {journey_id}..."):
                response = requests.get(url, headers=headers, timeout=30)

                if response.status_code == 200:
                    return response.json(), None
                elif response.status_code == 401:
                    return None, "Authentication failed. Please check your API key."
                elif response.status_code == 404:
                    return None, f"Journey ID '{journey_id}' not found."
                else:
                    return None, f"API request failed with status {response.status_code}: {response.text}"

        except requests.exceptions.Timeout:
            return None, "Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return None, "Unable to connect to TD API. Please check your internet connection."
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    def get_available_attributes(self, audience_id: str) -> List[str]:
        """Get list of available customer attributes from the customers table."""
        if not audience_id or not self.api_key:
            return []

        try:
            with st.spinner("Loading available customer attributes..."):
                client = pytd.Client(
                    apikey=self.api_key,
                    endpoint='https://api.treasuredata.com',
                    engine='presto'
                )

                # Query to describe the customers table
                describe_query = f"DESCRIBE cdp_audience_{audience_id}.customers"
                result = client.query(describe_query)

                if result and result.get('data'):
                    # Extract column names, excluding 'time' and 'cdp_customer_id'
                    columns = [row[0] for row in result['data'] if row[0] not in ['time', 'cdp_customer_id']]
                    return sorted(columns)

        except Exception as e:
            st.toast(f"Could not load customer attributes: {str(e)}", icon="⚠️")

        return []

    def load_profile_data(self, journey_id: str, audience_id: str, selected_attributes: List[str] = None) -> Optional[pd.DataFrame]:
        """Load profile data using pytd from live Treasure Data tables."""
        if not journey_id or not audience_id or not self.api_key:
            st.error("Journey ID, Audience ID, and API key are required for live data query")
            return None

        if selected_attributes is None:
            selected_attributes = []

        try:
            # Initialize pytd client with presto engine and api.treasuredata.com endpoint
            with st.spinner(f"Connecting to Treasure Data and querying profile data..."):
                client = pytd.Client(
                    apikey=self.api_key,
                    endpoint='https://api.treasuredata.com',
                    engine='presto'
                )

                # Construct the query for live profile data
                table_name = f"cdp_audience_{audience_id}.journey_{journey_id}"

                if selected_attributes:
                    # JOIN query with additional attributes from customers table
                    attributes_str = ", ".join([f"c.{attr}" for attr in selected_attributes])
                    query = f"""
                    SELECT j.cdp_customer_id, {attributes_str}
                    FROM {table_name} j
                    JOIN cdp_audience_{audience_id}.customers c
                    ON c.cdp_customer_id = j.cdp_customer_id
                    """
                    st.toast(f"Querying journey table with {len(selected_attributes)} additional attributes", icon="🔍")
                else:
                    # Standard query without JOIN
                    query = f"SELECT * FROM {table_name}"
                    st.toast(f"Querying table: {table_name}", icon="🔍")

                # Execute the query and return as DataFrame
                query_result = client.query(query)

                # Convert the result to a pandas DataFrame
                if not query_result.get('data'):
                    st.toast(f"No data found in table {table_name}", icon="⚠️")
                    return pd.DataFrame()

                profile_data = pd.DataFrame(query_result['data'], columns=query_result['columns'])

                # If we used JOIN query, we need to merge back with the full journey data
                if selected_attributes and not profile_data.empty:
                    # Get the full journey data for journey step information
                    full_journey_query = f"SELECT * FROM {table_name}"
                    full_result = client.query(full_journey_query)

                    if full_result and full_result.get('data'):
                        full_journey_data = pd.DataFrame(full_result['data'], columns=full_result['columns'])

                        # Merge the customer attributes with the full journey data
                        profile_data = full_journey_data.merge(
                            profile_data,
                            on='cdp_customer_id',
                            how='left'
                        )

                return profile_data

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error querying live profile data: {error_msg}")

            # Provide helpful error messages for common issues
            if "Table not found" in error_msg or "does not exist" in error_msg:
                st.error(f"Table 'cdp_audience_{audience_id}.journey_{journey_id}' does not exist. Please verify the audience ID and journey ID. Note: The journey workflow may not have been run yet and the audience needs to be built first.")
            elif "Authentication" in error_msg or "401" in error_msg:
                st.error("Authentication failed. Please check your TD API key.")
            elif "Permission denied" in error_msg or "403" in error_msg:
                st.error("Permission denied. Please ensure your API key has access to the audience data.")

            return None


# Convenience functions for backward compatibility
def get_api_key() -> Optional[str]:
    """Get TD API key - convenience function."""
    service = TDAPIService()
    return service.api_key


def fetch_journey_data(journey_id: str, api_key: str) -> Tuple[Optional[dict], Optional[str]]:
    """Fetch journey data - convenience function."""
    service = TDAPIService()
    service.api_key = api_key
    return service.fetch_journey_data(journey_id)


def get_available_attributes(audience_id: str, api_key: str) -> List[str]:
    """Get available attributes - convenience function."""
    service = TDAPIService()
    service.api_key = api_key
    return service.get_available_attributes(audience_id)


def load_profile_data(journey_id: str, audience_id: str, api_key: str) -> Optional[pd.DataFrame]:
    """Load profile data - convenience function."""
    service = TDAPIService()
    service.api_key = api_key
    selected_attributes = st.session_state.get("selected_attributes", [])
    return service.load_profile_data(journey_id, audience_id, selected_attributes)