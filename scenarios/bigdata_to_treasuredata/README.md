# Workflow: Scenario (Import into Treasure Data from Bigquery)

This example workflow ingests data from Bigquery to Treasure Data in accordance with the following steps:

1. Output only necessary data of a table into another in Bigquery
2. Output the table in Bigquery into a CSV file on Google Cloud Storage
3. Output the CSV file on Google Cloud Storage into Treasure Data

In this scenario, some workflow operators are used. You will need to set secrets to use them. Please refer to each documentation for usage.

- `bq>: operator`: [bq>: Running Google BigQuery queries](https://docs.digdag.io/operators/bq.html)
- `bq_extract>: operator`: [bq_extract>: Exporting Data from Google BigQuery](https://docs.digdag.io/operators/bq_extract.html)
- `td_load>: operator`: [td_load>: Treasure Data bulk loading](https://docs.digdag.io/operators/td_load.html)

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push bq_to_td

Next, please set database credentials by `td wf secrets` command.

    # Set Secrets for `bq>:` and `bq_extract>:` operators
    $ td wf secrets --project bq_to_td --set gcp.credential=@credential.json
    
    # Set Secrets for `td_load>:` operator [See example](https://github.com/treasure-data/workflow-examples/tree/master/td_load/gcs)
    $ td wf secrets --project bq_to_td --set gcp.jsonkey=@converted.json
    $ td wf secrets --project bq_to_td --set td.apikey=YOURAPIKEY

Now you can reference these credentials by `${secret:}` syntax in yml file of `td_load` operator.

Finally, you can trigger the session manually.

    # Run
    $ td wf start bq_to_td main.dig --session now

# Next Step

If you have any questions, please contact to support@treasuredata.com.
