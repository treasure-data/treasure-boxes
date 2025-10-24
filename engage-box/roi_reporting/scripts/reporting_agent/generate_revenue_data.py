#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Revenue Sample Data Generator for ROI Dashboard

This script generates realistic sample revenue data for testing and demonstrating
the ROI Dashboard reporting agent. It can generate data in two ways:
1. Simple random data with configurable parameters
2. Realistic data based on existing email events

Usage:
    python generate_revenue_data.py --database <database_name> --sample-size 500 --days 30 [--realistic] [--overwrite]

For workflow use:
    py>: scripts.reporting_agent.generate_revenue_data.generate_revenue_data_for_workflow
    database: ${td.database}
    sample_size: ${params.sample_size}
    days: ${params.days}
    realistic: ${params.realistic}
    overwrite: ${params.overwrite}

Safety features:
- By default, the script will not overwrite existing tables in production databases
- Use the --overwrite flag to explicitly allow overwriting existing tables
"""

import os
import sys
import uuid
import random
import argparse
import logging
from datetime import datetime, timedelta
import pytd
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Revenue table name
REVENUE_TABLE = 'revenue_table'
EMAIL_EVENTS_TABLE = 'email_events'
EVENTS_MASTER_TABLE = 'events_master'

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

def get_campaign_ids(client, database):
    """
    Get campaign IDs from events master table

    Args:
        client: TD client
        database: Database name

    Returns:
        List of campaign IDs
    """
    try:
        query = f"""
        SELECT DISTINCT campaign_id
        FROM {database}.{EVENTS_MASTER_TABLE}
        WHERE campaign_id IS NOT NULL
        """
        result = client.query(query, db = database)
        campaign_ids = []
        if 'data' in result:
            campaign_ids = [row[0] for row in result['data'] if row[0]]

        # If no campaign IDs found, return default sample
        if not campaign_ids:
            return ['camp123', 'camp456']

        return campaign_ids
    except Exception as e:
        logger.warning(f"Error fetching campaign IDs: {e}")
        return ['camp123', 'camp456']

def get_email_data(client, database, days=30, limit=1000):
    """
    Get email events data from the past N days

    Args:
        client: TD client
        database: Database name
        days: Number of days to look back
        limit: Maximum number of records to fetch

    Returns:
        List of dictionaries with email_hash, campaign_id, and event_timestamp
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        query = f"""
        SELECT email_hash, campaign_id, event_timestamp
        FROM {database}.{EMAIL_EVENTS_TABLE}
        WHERE event_timestamp BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
        AND email_hash IS NOT NULL
        AND campaign_id IS NOT NULL
        LIMIT {limit}
        """
        result = client.query(query, db = database)

        email_data = []
        if 'data' in result:
            for row in result['data']:
                email_data.append({
                    'email_hash': row[0],
                    'campaign_id': row[1],
                    'event_timestamp': row[2]
                })

        # If no email data found, return empty list
        if not email_data:
            logger.warning("No email event data found. Will generate synthetic data.")

        return email_data
    except Exception as e:
        logger.warning(f"Error fetching email data: {e}")
        return []

def generate_random_date(days_ago):
    """
    Generate a random date within the past N days

    Args:
        days_ago: Number of days to go back

    Returns:
        Random datetime string
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)

    # Generate random date in range
    random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
    random_date = start_date + timedelta(seconds=random_seconds)

    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_conversion_timestamp(email_timestamp, min_delay_hours=1, max_delay_hours=72):
    """
    Generate conversion timestamp after email event with realistic delay

    Args:
        email_timestamp: Original email timestamp
        min_delay_hours: Minimum delay in hours
        max_delay_hours: Maximum delay in hours

    Returns:
        Conversion timestamp string
    """
    if isinstance(email_timestamp, str):
        email_dt = datetime.strptime(email_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    else:
        email_dt = email_timestamp

    # Add random delay (weighted towards shorter delays)
    delay_hours = min_delay_hours + (max_delay_hours - min_delay_hours) * random.random() ** 2
    conversion_dt = email_dt + timedelta(hours=delay_hours)

    return conversion_dt.strftime('%Y-%m-%d %H:%M:%S')

def generate_random_revenue(min_amount=10.0, max_amount=500.0, mean=100.0, std_dev=75.0):
    """
    Generate a random revenue amount with realistic distribution

    Args:
        min_amount: Minimum revenue amount
        max_amount: Maximum revenue amount
        mean: Mean revenue amount
        std_dev: Standard deviation of revenue

    Returns:
        Random revenue amount
    """
    # Use normal distribution capped at min/max values
    revenue = np.random.normal(mean, std_dev)
    revenue = max(min_amount, min(max_amount, revenue))
    return round(revenue, 2)

def get_attribution_type(direct_probability=0.7):
    """
    Return attribution type based on configured probability

    Args:
        direct_probability: Probability of direct attribution

    Returns:
        Attribution type string ('direct' or 'contributed')
    """
    return 'direct' if random.random() < direct_probability else 'contributed'

def generate_simple_revenue_samples(campaign_ids, count=100, days=30):
    """
    Generate simple random revenue samples

    Args:
        campaign_ids: List of campaign IDs to choose from
        count: Number of samples to generate
        days: Number of days to distribute data over

    Returns:
        List of sample data dictionaries
    """
    samples = []

    # Generate email hashes
    email_hashes = [f'hash{i:04d}' for i in range(1, count+1)]

    for i in range(count):
        # Generate random values
        email_hash = random.choice(email_hashes)
        campaign_id = random.choice(campaign_ids)

        samples.append({
            'conversion_id': f'conv{uuid.uuid4().hex[:8]}',
            'email_hash': email_hash,
            'conversion_timestamp': generate_random_date(days),
            'total_revenue': generate_random_revenue(),
            'attribution_type': get_attribution_type(),
            'campaign_id': campaign_id,
            'custom_event_id': campaign_id
        })

    return samples

def generate_realistic_revenue_samples(email_data, conversion_rate=0.05):
    """
    Generate realistic revenue samples based on email events

    Args:
        email_data: List of dictionaries with email_hash and campaign_id
        conversion_rate: Percentage of email events to convert to revenue

    Returns:
        List of sample data dictionaries
    """
    samples = []

    # For each email, decide if it converts
    for email in email_data:
        if random.random() <= conversion_rate:
            # Generate conversion with correlation to original email
            samples.append({
                'conversion_id': f'conv{uuid.uuid4().hex[:8]}',
                'email_hash': email['email_hash'],
                'conversion_timestamp': generate_conversion_timestamp(email['event_timestamp']),
                'total_revenue': generate_random_revenue(),
                'attribution_type': get_attribution_type(),
                'campaign_id': email['campaign_id'],
                'custom_event_id': email['campaign_id']
            })

    return samples

def create_revenue_table(client, database, sample_size=100, days=30, realistic=False, overwrite=False):
    """
    Create Revenue table with sample data

    Args:
        client: TD client instance
        database: Database name
        sample_size: Number of sample records to generate
        days: Number of days to generate data for
        realistic: Whether to generate realistic data based on email events
        overwrite: Whether to overwrite existing table if it exists
    """
    logger.info(f"Creating Revenue table: {database}.{REVENUE_TABLE}")

    # Check if table exists
    if table_exists(client, database, REVENUE_TABLE):
        if not overwrite:
            logger.warning(f"Table {database}.{REVENUE_TABLE} already exists and overwrite not specified. Skipping.")
            return False
        else:
            logger.warning(f"Table {database}.{REVENUE_TABLE} already exists. Overwriting as requested.")

    # Get campaign IDs
    campaign_ids = get_campaign_ids(client, database)

    sample_data = []

    if realistic:
        # Try to get email data for realistic generation
        email_data = get_email_data(client, database, days, limit=int(sample_size * 10))

        if email_data:
            # Calculate conversion rate to achieve target sample size
            conversion_rate = min(1.0, sample_size / len(email_data))
            sample_data = generate_realistic_revenue_samples(email_data, conversion_rate)
            logger.info(f"Generated {len(sample_data)} realistic revenue samples")

    # Fall back to simple generation if realistic data not available or not enough
    if not sample_data or len(sample_data) < sample_size:
        count_needed = sample_size - len(sample_data)
        simple_samples = generate_simple_revenue_samples(campaign_ids, count=count_needed, days=days)
        sample_data.extend(simple_samples)
        logger.info(f"Added {len(simple_samples)} simple revenue samples")

    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Create table
    client.load_table_from_dataframe(
        df,
        f"{database}.{REVENUE_TABLE}",
        if_exists='overwrite'
    )

    logger.info(f"Successfully created {database}.{REVENUE_TABLE} with {len(sample_data)} samples")
    return True

# for workflow
def generate_revenue_data_for_workflow(database, sample_size=100, days=30, realistic=False, overwrite=False):
    """
    Workflow entry point function to generate revenue data

    Args:
        database: Database name
        sample_size: Number of sample records to generate
        days: Number of days to generate data for
        realistic: Whether to generate realistic data based on email events
        overwrite: Whether to overwrite existing table if it exists
    """
    logger.info(f"Starting revenue data generation for workflow (database={database})")

    # Convert parameters from workflow format if needed
    if isinstance(sample_size, str):
        sample_size = int(sample_size)
    if isinstance(days, str):
        days = int(days)
    if isinstance(realistic, str):
        realistic = realistic.lower() == 'true'
    if isinstance(overwrite, str):
        overwrite = overwrite.lower() == 'true'

    try:
        # Initialize TD client
        client = get_td_client(database)

        # Create revenue table with sample data
        create_revenue_table(
            client,
            database,
            sample_size=sample_size,
            days=days,
            realistic=realistic,
            overwrite=overwrite
        )

        logger.info("Revenue sample data generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error generating revenue sample data: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Generate sample revenue data for ROI Dashboard')
    parser.add_argument('--database', required=True, help='TD database name')
    parser.add_argument('--sample-size', type=int, default=100, help='Number of revenue samples to generate')
    parser.add_argument('--days', type=int, default=30, help='Number of days to generate data for')
    parser.add_argument('--realistic', action='store_true', help='Generate realistic data based on email events')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting existing tables (defaults to false)')
    args = parser.parse_args()

    try:
        # Initialize TD client
        client = get_td_client(args.database)

        # Create revenue table with sample data
        create_revenue_table(
            client,
            args.database,
            sample_size=args.sample_size,
            days=args.days,
            realistic=args.realistic,
            overwrite=args.overwrite
        )

        logger.info("Revenue sample data generation complete")

    except Exception as e:
        logger.error(f"Error generating revenue sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
