# Workflow: Scenario (Import from Iterable API into Treasure Data)

This scenario shows how you can ingest data not supported by the Iterable connector using TD Workflow Custom Scripts with Iterable API. This example will ingest Iterable Campaigns that are in a Ready state into Treasure Data.

# How to Run

1. Update the destination database and table values in the `import_iterable_to_td.dig` file (`<database_name>` and `<table_name>`).

2. Upload the workflow with TD CLI.

    $ td wf push import_iterable_to_td

3. Set the Iterable API Key and Treasure Data API Key as workflow secrets using the `td wf secrets` command.

    # Set Iterable API Key workflow secret
    $ td wf secrets --project import_iterable_to_td --set iterable.apikey=<iterable_api_key>

    # Set Treasure Data API Key workflow secret
    $ td wf secrets --project import_iterable_to_td --set td.apikey=<treasuredata_master_api_key>

Finally, you can trigger the session manually.

    # Run
    $ td wf start import_iterable_to_td import_iterable_to_td --session now

If you have any questions, contact to support@treasuredata.com.
