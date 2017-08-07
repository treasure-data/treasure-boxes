# Workflow: td_load Example (Mixpanel)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Mixpanel](https://docs.treasuredata.com/articles/data-connector-mixpanel) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.
This workflow also be able to run incrementally using Mixpanel `Where` parameter in API Request. 

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# Preparation

Some Mixpanel account will have timestamp field, which is the processing time when Mixpanel process the event data. The field name could be `mp_processing_time_ms`, You can check with Mixpanel to see if your Mixpanel account have that field enable or not.

We will use that field as the incremental_field.

```yaml
 mixpanel:
    timezone: "US/Pacific"
    from_date: "${last_session_date}"
    fetch_days: 1
    incremental_column: mp_processing_time_ms
```

You will need to create a [Treasure Data's Saved Presto Query](https://docs.treasuredata.com/articles/presto) that will return the max ingestion time, Example:

```sql
SELECT Max(mp_processing_time_ms) FROM Mixpanel
```
Name that query `latest_fetched_time_query` or change the configuration according to that query

```yaml
+query_latest_fetched_time:
  td_run>: latest_fetched_time_query
  database: ${td.dest_db}
  store_last_results: true
```
# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set mixpanel.api_key=xyz
    $ td wf secrets --project td_load_example --set mixpanel.api_secret=xyz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
