# Report Preparation Workflow

This workflow provides dig files and SQL queries for preparing data for the ROI dashboard.

## Overview

The report preparation workflow performs the following tasks:

1. Collects data from CDP API and Engage API to update the Events Master table
2. Collects data from Email Events tables across multiple domains and aggregates them
3. Creates a Daily Summary table to provide data for reporting

## File Structure

```
reporting_agent/
├── README.md                 # This document
├── config.yaml               # Configuration file
├── report_preparation.dig    # Main workflow file (includes revenue generation)
└── queries/                  # SQL query files
    ├── daily_summary.sql           # Daily Summary table query
    ├── deduplicate_email_events.sql # Email events deduplication query
    ├── email_events.sql            # Email Events collection query
    └── merge_summary_data.sql      # Summary data merge query
```

## Configuration

The `config.yaml` file allows you to configure:

- Database name
- Table names (Events Master, Email Events, Daily Summary, etc.)
- List of email domains
- API endpoints
- Revenue generation settings

## Workflow Execution

### Prerequisites

- Access to Treasure Data environment
- API keys required for workflow execution
- User defined workflow setup for execution

### Setup

1. Ensure the following tables exist:
   - events_master (Event master table)
   - email_events (Email events table)
   - revenue_table (Revenue data table)
   - daily_summary (Daily summary table)

2. Edit the `config.yaml` file to match your environment

### Scheduled Execution

The workflow is configured to run daily at 2:00 AM (UTC). Edit the `report_preparation.dig` file to change the schedule.

## Module Details

### 1. Events Master Update

Fetches data from CDP's Parent Segments, Segment Folders, Journey APIs and Engage's Campaign API to update the Events Master table.

```python
# Python script for Events Master update
scripts/reporting_agent/events_master.py
```

### 2. Email Events Collection

Extracts and aggregates data from multiple `${domain}.events` tables.

```sql
-- SQL query for Email Events collection
queries/email_events.sql
```

After collection, duplicate entries are removed using:

```sql
-- SQL query for deduplicating email events
queries/deduplicate_email_events.sql
```

### 3. Daily Summary Creation

Combines data from the Email Events table and Revenue table to create the Daily Summary table.

```sql
-- SQL query for Daily Summary creation
queries/daily_summary.sql
```

The daily summary data is then merged with existing data:

```sql
-- SQL query for merging summary data
queries/merge_summary_data.sql
```

## Revenue Sample Data Generation

The workflow includes functionality to generate realistic sample revenue data for testing and demonstration purposes.

### Stand-alone Revenue Generation

A dedicated workflow is provided for revenue data generation:

```
# Revenue generation is now integrated into the main workflow
$ td wf run report_preparation.dig -p td.revenue_generation.sample_size=500 -p td.revenue_generation.days=30 -p td.revenue_generation.realistic=true
```

Parameters:
- `sample_size`: Number of revenue records to generate (default: 500)
- `days`: Number of days to distribute data across (default: 30)
- `realistic`: Generate data based on existing email events if available (default: true)

### Test Environment Setup

#### Prerequisites

Before running the test scripts, you need to set up a Python environment with the required dependencies:

1. **Python Requirements**
   - Python 3.6 or later
   - virtualenv or venv module

2. **Environment Setup**

   ```bash
   # Create a virtual environment
   python -m venv reporting_agent_env

   # Activate the virtual environment
   # On macOS/Linux:
   source reporting_agent_env/bin/activate
   # On Windows (Note: Windows commands are provided for reference but have not been verified):
   # reporting_agent_env\Scripts\activate

   # Create a requirements.txt file with the following content:
   cat > requirements.txt << EOL
   pytd>=0.9.0
   pandas>=1.0.0
   numpy>=1.19.0
   EOL

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   The scripts require a Treasure Data API key. Set the following environment variables:

   ```bash
   # On macOS/Linux:
   export TD_API_KEY=your_api_key_here
   # On Windows (Note: Not verified):
   # set TD_API_KEY=your_api_key_here

   # Optional: If using a custom API endpoint
   # export TD_API_SERVER=https://api.treasuredata.com
   ```

4. **Add Scripts to Python Path**

   ```bash
   # From the root of the engage-api repository
   # On macOS/Linux:
   export PYTHONPATH=$PYTHONPATH:.
   # On Windows (Note: Not verified):
   # set PYTHONPATH=%PYTHONPATH%;.
   ```

#### Running the Test Setup Script

After setting up the environment, you can use the `setup_test_tables.py` script to create test tables with sample data:

```bash
# From the root of the engage-api repository
python scripts/reporting_agent/setup_test_tables.py --database engage_roi_reporting --create-tables --revenue-samples 500 --days 30 --realistic-revenue
```

This script supports the following parameters:
- `--revenue-samples`: Number of revenue samples to generate (default: 1)
- `--days`: Number of days to distribute data over (default: 30)
- `--realistic-revenue`: Generate data based on existing email events if available

## Test Scripts

A table creation script is provided for setting up a test environment:

```python
# Script for setting up test tables
scripts/reporting_agent/setup_test_tables.py
```

Additional scripts for sample data generation:

```python
# Script for generating revenue sample data
scripts/reporting_agent/generate_revenue_data.py
```

## Important Notes

- This workflow is designed to be run by the PS team
- The workflow should be implemented as a user-defined workflow
- Handle API keys with appropriate security measures

## Troubleshooting

Common issues and solutions:

1. **API access errors**: Check that API keys are correctly configured
2. **Missing tables**: Ensure all required tables have been created
3. **Data not updating**: Check workflow logs to confirm each step executed successfully