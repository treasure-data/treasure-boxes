# Workflow: Scenario (Account Reporting)

This scenario shows how you can ingest account data from Treasure Data API's for account reporting.

# How to Run

1. Update the values in `config.yml`:
- The API base urls for your region can be found here: https://api-docs.treasuredata.com/en/overview/aboutendpoints/#treasure-data-api-baseurls
- `target.database` - Sets the database the data will be ingested to. This database must exist prior to running the workflow.
- `target.tables` - Sets the table names for each report.

2. Upload the workflow with TD CLI.
```
    $ td wf push account_reporting
```
3. Set the Treasure Data API Key as a workflow secret using the `td wf secrets` command.
```
    # Set Treasure Data API Key workflow secret
    $ td wf secrets --project account_reporting --set td.apikey=<treasuredata_master_api_key>
```
Finally, you can trigger the session manually.
```
    # Run
    $ td wf start account_reporting account_reporting --session now
```
If you have any questions, contact to support@treasuredata.com.
