#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Events Master Data Collection Script

This script collects data from CDP APIs and Engage API to create Events Master table
which serves as a reference for linking campaigns, journeys, and activations.

Required environment variables:
- TD_API_KEY: Treasure Data API key
- TD_API_SERVER: Treasure Data API server URL
- TD_PRESTO_API: TD Presto API URL
- TD_PLAZMA_API: TD Plazma API URL
- CDP_API_BASE: CDP API base URL (defaults to https://api-cdp.treasuredata.com)
- ENGAGE_API_BASE: Engage API base URL (defaults to https://engage-api.treasuredata.com)
"""

import os
import logging
import requests
import pytd
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CDP API endpoints
CDP_API_BASE = os.environ.get('CDP_API_BASE', "https://api-cdp.treasuredata.com")
CDP_PARENT_SEGMENTS_API = "/entities/parent_segments"
CDP_SEGMENT_FOLDERS_API = "/tree/audiences/{audience_id}/segment_folders"
CDP_JOURNEY_API = "/entities/journeys"

# Engage API endpoints
ENGAGE_API_BASE = os.environ.get('ENGAGE_API_BASE', "https://engage-api.treasuredata.com")
ENGAGE_CAMPAIGNS_API = "/api/campaigns"

def get_api_key():
    """Get API key from environment variable"""
    api_key = os.environ.get('TD_API_KEY')
    if not api_key:
        raise ValueError("TD_API_KEY environment variable is not set")
    return api_key

def get_headers():
    """Get headers for API requests"""
    return {
        'Authorization': f'TD1 {get_api_key()}',
        'Content-Type': 'application/json'
    }

def fetch_cdp_parent_segments():
    """Fetch all parent segments (audiences) from CDP API"""
    logger.info("Fetching parent segments (audiences) from CDP API")
    url = f"{CDP_API_BASE}{CDP_PARENT_SEGMENTS_API}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_segment_folders(audience_id):
    """Fetch segment folders for a specific audience ID"""
    logger.info(f"Fetching segment folders for audience ID {audience_id}")
    url = f"{CDP_API_BASE}{CDP_SEGMENT_FOLDERS_API}".format(audience_id=audience_id)
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_journeys(folder_id):
    """Fetch journeys for a specific folder ID"""
    logger.info(f"Fetching journeys for folder ID {folder_id}")
    url = f"{CDP_API_BASE}{CDP_JOURNEY_API}"
    params = {"folder_id": folder_id}
    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()

def fetch_engage_campaigns():
    """Fetch all campaigns from Engage API"""
    logger.info("Fetching campaigns from Engage API")
    url = f"{ENGAGE_API_BASE}{ENGAGE_CAMPAIGNS_API}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def collect_events_master_data():
    """Collect and combine data from CDP and Engage APIs to create Events Master data"""
    events_master_data = []
    
    # Fetch and process CDP journeys
    try:
        ps_response = fetch_cdp_parent_segments()
        audiences = ps_response.get('data', [])
        for audience in audiences:
            audience_id = audience.get('id')
            if not audience_id:
                continue
            
            folder_response = fetch_segment_folders(audience_id)
            folders = folder_response.get('data', [])
            for folder in folders:
                folder_id = folder.get('id')
                if not folder_id:
                    continue
                
                journey_response = fetch_journeys(folder_id)
                journeys = journey_response.get('data', [])
                for journey in journeys:
                    journey_id = journey.get('id')
                    journey_name = journey.get('name')
                    launched_at = journey.get('launched_at')
                    
                    attributes = journey.get('attributes', None)
                    if not attributes:
                        continue

                    # Process journey stages
                    stages = attributes.get('stages', [])
                    for stage in stages:
                        stage_id = stage.get('id')
                        stage_name = stage.get('name')
                        
                        events_master_data.append({
                            'journey_id': journey_id,
                            'journey_name': journey_name,
                            'journey_stage_id': stage_id,
                            'journey_stage_name': stage_name,
                            'campaign_id': None,
                            'campaign_name': None,
                            'launched_at': launched_at
                        })
    except Exception as e:
        logger.error(f"Error fetching CDP journeys: {e}")
    
    # Fetch and process Engage campaigns
    try:
        campaigns_response = fetch_engage_campaigns()
        campaigns = campaigns_response.get('data', [])
        
        for campaign in campaigns:
            attributes = campaign.get('attributes', {})
            campaign_id = campaign.get('id')
            campaign_name = attributes.get('name')
            launched_at = attributes.get('launched_at')
            
            events_master_data.append({
                'journey_id': None,
                'journey_name': None,
                'journey_stage_id': None,
                'journey_stage_name': None,
                'campaign_id': campaign_id,
                'campaign_name': campaign_name,
                'launched_at': launched_at
            })
    except Exception as e:
        logger.error(f"Error fetching Engage campaigns: {e}")
    
    return events_master_data

def update_events_master(database, events_master_table):
    """Update the Events Master table in Treasure Data"""
    logger.info(f"Updating Events Master table: {database}.{events_master_table}")
    
    # Collect events master data
    events_master_data = collect_events_master_data()
    
    if not events_master_data:
        logger.warning("No events master data collected, aborting update")
        return
    
    # Convert to DataFrame for TD import
    df = pd.DataFrame(events_master_data)
    
    # Initialize TD client
    client = pytd.Client(
        apikey=get_api_key(),
        endpoint=os.environ.get('TD_API_SERVER', 'https://api.treasuredata.com'),
        database=database
    )
    
    # Create or replace table
    logger.info(f"Writing {len(df)} records to {database}.{events_master_table}")
    client.load_table_from_dataframe(
        df, 
        f"{database}.{events_master_table}", 
        if_exists='overwrite'
    )
    
    logger.info(f"Successfully updated {database}.{events_master_table}")

if __name__ == "__main__":
    # For local testing only
    import argparse
    parser = argparse.ArgumentParser(description='Update Events Master table')
    parser.add_argument('--database', required=True, help='TD database name')
    parser.add_argument('--table', required=True, help='TD table name')
    args = parser.parse_args()
    
    update_events_master(args.database, args.table)
