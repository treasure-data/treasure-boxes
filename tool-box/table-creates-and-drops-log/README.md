Anomalous Table Creates and Deletes Log
======

## Overview

This workflow uses three inputs to determine anomalies within an account's audit log of table creates and deleats.
These anomalous actions will be recorded in a new table to empower users to investigate the create and delete actions.
Currently this workflow only works within a single account. If you own multiple accounts please either set up this
workflow for each account you want monitored or work with your Treasure Data team to discuss the possibility of expanding
this workflow's scope.

A unique list of tables that are impacted by anomalous changes will also be created which will reslut in fewer items than
the create/delete action log. This view may have significantly fewer records and a better starting point for investigation.
This table impact log will also be included in an email notification so that you can quickly review the list of tables
recording anomalous creates/deletes directly from your email.

### How it works
The tree inputs used to determine an anomalous action are:
1. lookback_range_days
    * This is the lookback range that the latest create/delete must have occured within. It is recomended to set this
number to the frequency which this workflow is scheduled to run. (i.e. if the workflow runs weekly set the
lookback_range_days to 7)
2. anomaly_range_days
    * This is the number of days that the workflow will look back for anomalies. If there are less than anomaly_threashold
creates/deletes within this timeframe then the actions will be flagged as anomalies.
3. anomaly_threshold
    * This input sets the maximum number of changes that can occur within the anomaly_range_days timeframe to be considered
an anomaly. The reason for this is that there may be tables that update every day, week or month and you will want to
filter out any regularly scheduled deletes/creates. Work with your team to understand what the minimum number of
creates/deletes per table_name would be within your anomaly_range_days timeframe. Remember that you can always change
this later on if you find you are capturing regularly scheduled actions.

You will also be able to specify a mailing_list of emails to recieve anomaly notifications, exclude_databases and
exclude_tables lists of databases and/or tables you would like excluded from the analysis.

### Using Google Sheets

By using Google Sheets with this workflow you will be able to instantly dig into analysis of anomalous creates/deletes
within a spreadsheet rather needing to export or query this data in an additional workflow. If you do not wish to use
this option please make sure to place a '#' before each line in the workflow related to Google Sheets. This includes
variables: 'google_sheet_id' and 'google_sheet_connection_name' as well as the step '+create_google_sheet_of_anomalous_jobs'.


## Setup

1. Create a new workflow within the account you would like to have analyzed.
    * Copy and paste the anomalous_table_creates_and_deletes_log.dig into the workflow.
2. Specify the options available:
    * **database:** Set the name of an existing database where you would like your log files to be maintained. If there is not
already a database you would like to use, please [create one](https://docs.treasuredata.com/display/public/PD/Database+and+Table+Management)
and enter the name here.
    * **lookback_range_days:** Should be an intiger representing a number of days, see Overview for more details.
    * **anomaly_range_days:** Should be an intiger representing a number of days, see Overview for more details.
    * **anomaly_threashold:** Should be an intiger representing a number of days, see Overview for more details.
    * **google_sheet_id:** Create a blank Google Sheet shared to the appropriate audience to store the log of anomalous create/
delete actions. There is an
[ID in the URL](https://developers.google.com/sheets/api/guides/concepts)
, copy that ID and paste it into the google_sheet_id: in the workflow. If you do not want to use Google Sheets just enter
'#' in front of this variable and in all lines within the '+create_google_sheet_of_anomalous_jobs' step of the workflow.
    * **google_sheet_connection_name:** Enter the name of your
[Google Sheets connection](https://docs.treasuredata.com/display/public/INT/Google+Sheets+Export+Integration)
within your Treasure Data account.
    * **mailing_list:** Enter all emails you would like to recieve notifications of anomalous actions seperated by commas.
    * **exclude_databases:** If you do not wish to exclude databases please enter: []. Otherwise use regex to identify the
    list the databases you would like to exclude, each on a new line preceeded by a '-'.
    * **exclude_tables:** If you do not wish to exclude tables please enter: []. Otherwise use regex to identify the
    list the tables you would like to exclude, each on a new line preceeded by a '-'. Please consider the full
    database_name.table_name of tables in this section.
3. If you are opting out of using Google Sheets for an output, please make sure to place a '#' before each line in the
workflow related to Google Sheets. This includes variables: 'google_sheet_id' and 'google_sheet_connection_name' as well as
the step '+create_google_sheet_of_anomalous_jobs'.
4. You are now ready to run the workflow and ensure setup is correct.
5. Schedule the workflow to ensure you stay up to date with new creates/deletes accross your account.

## Using the output

What are these IDs?
