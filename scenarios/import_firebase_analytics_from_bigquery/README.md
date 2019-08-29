# Workflow: Scenario: Import Firebase analytics incrementally

## Why should you run queries sequentially?
So far, TreasureData does not support Firebase analytics.
When you want to import Firebase analytics data into TD, you have to import data from BigQuery.
As a Firebase analytics design, Firebase creates a new table everyday, and it makes impossible to import data incrementally.
So, this sample shows how to import Firebase analytics data incrementally.

## Scenario

Import Firebase analytics data from BigQuery to TreasureData.  
Firebase analytics data contains nested data, so you should unnests json data to row data during importing data.
In this sample, you can check how to unset firebase analytics data.

For more details, please refer to below links.  
[Working with Arrays in Standard SQL](https://cloud.google.com/bigquery/docs/reference/standard-sql/arrays#Querying%20Nested%20Arrays)

# How to Run

First, you need to replace "database", "table" in the dig file with Your TD database and table name.
Also, you must replace "project_id", "dataset" with your GCP's project ID and dateset in td-load.yml file.

    # Upload
    $ td wf push import_firebase_analytics_from_bigquery

Second, please upload the workflow.

    # Upload
    $ td wf push import_firebase_analytics_from_bigquery

Third, please set datasource credentials by td wf secrets command.

    # Set Secrets
    $ td wf secrets --project import_firebase_analytics_from_bigquery --set td.apikey
    $ td wf secrets --project import_firebase_analytics_from_bigquery --set gcp.jsonkey=@<Your json key file>

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start import_firebase_analytics_from_bigquery import_firebase_analytics_from_bigquery --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
