#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test Setup Script for Reporting Agent Workflow

This script creates test tables and sample data for testing the reporting agent workflow.
It sets up:
1. Events Master table
2. Email Events table structure
3. Revenue table structure
4. Daily Summary table structure

Usage:
    python setup_test_tables.py --database <database_name> --create-tables [--revenue-samples 500] [--days 30] [--realistic-revenue] [--overwrite]

Required environment variables:
- TD_API_KEY: Treasure Data API key
- TD_API_SERVER: Treasure Data API server URL

Safety features:
- By default, the script will not overwrite existing tables in production databases
- Use the --overwrite flag to explicitly allow overwriting existing tables
"""

import os
import sys
import argparse
import logging
import pytd
import pandas as pd

# Import revenue data generation functions
from generate_revenue_data import create_revenue_table as create_revenue_samples

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test table names
EVENTS_MASTER_TABLE = 'events_master'
EMAIL_EVENTS_TABLE = 'email_events'
REVENUE_TABLE = 'revenue_table'
DAILY_SUMMARY_TABLE = 'daily_summary'

def get_api_key():
    """Get API key from environment variable"""
    api_key = os.environ.get('TD_API_KEY')
    if not api_key:
        raise ValueError("TD_API_KEY environment variable is not set")
    return api_key

def get_td_client(database):
    """Get Treasure Data client"""
    return pytd.Client(
        apikey=get_api_key(),
        endpoint=os.environ.get('TD_API_SERVER', 'https://api.treasuredata.com'),
        database=database
    )

def table_exists(client, database, table_name):
    """Check if a table exists in the database"""
    try:
        # Try to get table metadata - if it fails, the table does not exist
        client.query(f"SELECT 1 FROM {table_name} LIMIT 1", db=database)
        return True
    except Exception:
        # Table doesn't exist or is inaccessible
        return False

def create_events_master_table(client, database, overwrite=False):
    """Create Events Master table with sample data"""
    logger.info(f"Creating Events Master table: {database}.{EVENTS_MASTER_TABLE}")

    # Check if table exists
    if table_exists(client, database, EVENTS_MASTER_TABLE):
        if not overwrite:
            logger.warning(f"Table {database}.{EVENTS_MASTER_TABLE} already exists and --overwrite not specified. Skipping.")
            return False
        else:
            logger.warning(f"Table {database}.{EVENTS_MASTER_TABLE} already exists. Overwriting as requested.")

    # Sample data for Events Master table
    sample_data = [
        {
            'campaign_id': 'camp123',
            'campaign_name': 'Summer Sale 2025',
            'journey_id': None,
            'journey_name': None,
            'journey_stage_id': None,
            'journey_stage_name': None,
            'launched_at': '2025-09-01'
        },
        {
            'campaign_id': 'camp456',
            'campaign_name': 'New Product Launch',
            'journey_id': None,
            'journey_name': None,
            'journey_stage_id': None,
            'journey_stage_name': None,
            'launched_at': '2025-09-05'
        },
        {
            'campaign_id': None,
            'campaign_name': None,
            'journey_id': 'jour789',
            'journey_name': 'Customer Onboarding',
            'journey_stage_id': 'stage1',
            'journey_stage_name': 'Welcome Email',
            'launched_at': '2025-09-02'
        },
        {
            'campaign_id': None,
            'campaign_name': None,
            'journey_id': 'jour789',
            'journey_name': 'Customer Onboarding',
            'journey_stage_id': 'stage2',
            'journey_stage_name': 'Setup Guide',
            'launched_at': '2025-09-02'
        }
    ]

    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Create or replace table
    client.load_table_from_dataframe(
        df,
        f"{database}.{EVENTS_MASTER_TABLE}",
        if_exists='overwrite'
    )

    logger.info(f"Successfully created {database}.{EVENTS_MASTER_TABLE} with sample data")
    return True

def create_email_events_table(client, database, overwrite=False):
    """Create Email Events table structure and populate it with approximately 50 sample records for testing."""
    logger.info(f"Creating Email Events table structure: {database}.{EMAIL_EVENTS_TABLE}")

    # Check if table exists
    if table_exists(client, database, EMAIL_EVENTS_TABLE):
        if not overwrite:
            logger.warning(f"Table {database}.{EMAIL_EVENTS_TABLE} already exists and --overwrite not specified. Skipping.")
            return False
        else:
            logger.warning(f"Table {database}.{EMAIL_EVENTS_TABLE} already exists. Overwriting as requested.")

    # Generate about 50 sample email events with proper ISO 8601 format timestamps
    import datetime
    import random
    import uuid

    # Event types with their probability weights
    event_types = [
        ('Send', 0.25),
        ('Delivery', 0.3),
        ('Open', 0.2),
        ('Click', 0.15),
        ('Bounce', 0.05),
        ('Complaint', 0.05)
    ]

    # Campaign and journey configurations
    campaigns = [
        {'id': 'camp123', 'name': 'Summer Sale 2025', 'title': 'Summer Sale 50% Off'},
        {'id': 'camp456', 'name': 'New Product Launch', 'title': 'Check Out Our Latest Products!'}
    ]
    journeys = [
        {'id': 'jour789', 'name': 'Customer Onboarding', 'stages': [
            {'id': 'stage1', 'name': 'Welcome Email', 'title': 'Welcome to Our Service'},
            {'id': 'stage2', 'name': 'Setup Guide', 'title': 'How to Set Up Your Account'}
        ]}
    ]

    # Generate sample data
    base_date = datetime.datetime(2025, 9, 1)
    sample_data = []

    for i in range(50):
        # Select event type based on weights
        event_type = random.choices(
            [et[0] for et in event_types],
            weights=[et[1] for et in event_types],
            k=1
        )[0]

        # Generate a random timestamp within a 30-day period
        days_offset = random.randint(0, 29)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        seconds_offset = random.randint(0, 59)

        event_time = base_date + datetime.timedelta(
            days=days_offset,
            hours=hours_offset,
            minutes=minutes_offset,
            seconds=seconds_offset
        )

        # Format as ISO 8601 with Z suffix for UTC timezone
        iso8601_timestamp = event_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Decide if this is a campaign or journey event
        is_campaign = random.random() < 0.7  # 70% chance of being a campaign

        if is_campaign:
            campaign = random.choice(campaigns)
            event = {
                'message_id': f'msg{uuid.uuid4().hex[:8]}',
                'event_timestamp': iso8601_timestamp,
                'email_hash': f'hash{i:03d}',
                'activation_id': f'act{random.randint(100, 999)}',
                'activation_name': f'{campaign["name"]} Batch',
                'campaign_id': campaign['id'],
                'journey_id': None,
                'journey_stage_id': None,
                'email_title': campaign['title'],
                'event_type': event_type,
                'bounce_type': 'Permanent' if event_type == 'Bounce' and random.random() < 0.7 else ('Transient' if event_type == 'Bounce' else None),
                'bounce_subtype': 'General' if event_type == 'Bounce' else None,
                'custom_event_id': campaign['id']
            }
        else:
            journey = random.choice(journeys)
            stage = random.choice(journey['stages'])
            event = {
                'message_id': f'msg{uuid.uuid4().hex[:8]}',
                'event_timestamp': iso8601_timestamp,
                'email_hash': f'hash{i:03d}',
                'activation_id': f'act{random.randint(100, 999)}',
                'activation_name': f'{journey["name"]} Automated',
                'campaign_id': None,
                'journey_id': journey['id'],
                'journey_stage_id': stage['id'],
                'email_title': stage['title'],
                'event_type': event_type,
                'bounce_type': 'Permanent' if event_type == 'Bounce' and random.random() < 0.7 else ('Transient' if event_type == 'Bounce' else None),
                'bounce_subtype': 'General' if event_type == 'Bounce' else None,
                'custom_event_id': journey['id']
            }

        sample_data.append(event)

    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Create table
    client.load_table_from_dataframe(
        df,
        f"{database}.{EMAIL_EVENTS_TABLE}",
        if_exists='overwrite'
    )

    logger.info(f"Successfully created {database}.{EMAIL_EVENTS_TABLE} structure")
    return True

def create_revenue_table(client, database, overwrite=False):
    """Create Revenue table with sample data"""
    logger.info(f"Creating Revenue table structure: {database}.{REVENUE_TABLE}")

    # Check if table exists
    if table_exists(client, database, REVENUE_TABLE):
        if not overwrite:
            logger.warning(f"Table {database}.{REVENUE_TABLE} already exists and --overwrite not specified. Skipping.")
            return False
        else:
            logger.warning(f"Table {database}.{REVENUE_TABLE} already exists. Overwriting as requested.")

    # Create table structure with minimal sample data
    sample_data = [
        {
            'conversion_id': 'conv123',
            'email_hash': 'abc123hash',
            'conversion_timestamp': '2025-09-01 15:30:00',
            'total_revenue': 199.99,
            'attribution_type': 'direct',
            'campaign_id': 'camp123',
            'custom_event_id': 'camp123'
        }
    ]

    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Create table
    client.load_table_from_dataframe(
        df,
        f"{database}.{REVENUE_TABLE}",
        if_exists='overwrite'
    )

    logger.info(f"Successfully created {database}.{REVENUE_TABLE} structure")
    return True

def create_daily_summary_table(client, database, overwrite=False):
    """Create Daily Summary table with sample data"""
    logger.info(f"Creating Daily Summary table structure: {database}.{DAILY_SUMMARY_TABLE}")

    # Check if table exists
    if table_exists(client, database, DAILY_SUMMARY_TABLE):
        if not overwrite:
            logger.warning(f"Table {database}.{DAILY_SUMMARY_TABLE} already exists and --overwrite not specified. Skipping.")
            return False
        else:
            logger.warning(f"Table {database}.{DAILY_SUMMARY_TABLE} already exists. Overwriting as requested.")

    # Create table structure with minimal sample data
    sample_data = [
        {
            'summary_date': '2025-09-01',
            'campaign_id': 'camp123',
            'campaign_name': 'Summer Sale 2025',
            'journey_id': '',
            'journey_name': '',
            'total_sends': 100,
            'total_deliveries': 95,
            'total_opens': 45,
            'total_clicks': 20,
            'total_hard_bounces': 2,
            'total_soft_bounces': 3,
            'total_unsubscribes': 1,
            'total_revenue_direct': 199.99,
            'total_revenue_contributed': 199.99,
            'total_conversions': 1
        }
    ]

    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Create table
    client.load_table_from_dataframe(
        df,
        f"{database}.{DAILY_SUMMARY_TABLE}",
        if_exists='overwrite'
    )

    logger.info(f"Successfully created {database}.{DAILY_SUMMARY_TABLE} structure")
    return True


def main():
    parser = argparse.ArgumentParser(description='Setup test tables for reporting agent workflow')
    parser.add_argument('--database', required=True, help='TD database name')
    parser.add_argument('--create-tables', action='store_true', help='Create tables with test data')
    parser.add_argument('--revenue-samples', type=int, default=1, help='Number of revenue samples to generate')
    parser.add_argument('--days', type=int, default=30, help='Number of days to generate data for')
    parser.add_argument('--realistic-revenue', action='store_true', help='Generate realistic revenue data based on email events')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting existing tables (defaults to false)')
    args = parser.parse_args()

    try:
        # Initialize TD client
        client = get_td_client(args.database)

        if args.create_tables:
            # Create all tables with overwrite parameter
            tables_created = []

            # Track success of each table creation
            events_master_created = create_events_master_table(client, args.database, args.overwrite)
            if events_master_created:
                tables_created.append(EVENTS_MASTER_TABLE)

            email_events_created = create_email_events_table(client, args.database, args.overwrite)
            if email_events_created:
                tables_created.append(EMAIL_EVENTS_TABLE)

            # Handle revenue data creation based on arguments
            revenue_created = False
            if args.revenue_samples > 1 or args.realistic_revenue:
                # Use enhanced revenue data generation with overwrite flag
                revenue_created = create_revenue_samples(
                    client,
                    args.database,
                    sample_size=args.revenue_samples,
                    days=args.days,
                    realistic=args.realistic_revenue,
                    overwrite=args.overwrite
                )
                if revenue_created:
                    tables_created.append(REVENUE_TABLE)
            else:
                # Use original simple revenue table creation
                revenue_created = create_revenue_table(client, args.database, args.overwrite)
                if revenue_created:
                    tables_created.append(REVENUE_TABLE)

            daily_summary_created = create_daily_summary_table(client, args.database, args.overwrite)
            if daily_summary_created:
                tables_created.append(DAILY_SUMMARY_TABLE)

            if tables_created:
                logger.info(f"Setup complete: created tables: {', '.join(tables_created)}")
            else:
                logger.warning("No tables were created. All tables already exist and --overwrite not specified.")
        else:
            logger.info("No action specified. Use --create-tables to set up test environment.")

    except Exception as e:
        logger.error(f"Error setting up test tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
