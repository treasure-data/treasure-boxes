# Workflow: Marketo Daily Load

Data Connector for Marketo uses Marketo Bulk Export API, but the API has several limitations; filter conditions doesn't work as expected and delay arriving of activity/lead logs.

This example workflow take care of such limitations

# How to Run

## For Filter by CreatedAt

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push marketo_daily_load

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project marketo_daily_load --set marketo.account_id=xxxxxx
    $ td wf secrets --project marketo_daily_load --set marketo.client_id=yyyyy
    $ td wf secrets --project marketo_daily_load --set marketo.client_secret=zzzzz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load_activity.yml](config/daily_load_activity.yml)
- [config/daily_load_lead.yml](config/daily_load_lead.yml)

If you use Treasure Workflow UI, overwrite above parameters into ${secret:marketo.xxxx} in yml files directly.

Now, you can trigger the session manually.

    # Run
    $ td wf start marketo_daily_load daily_load_createdat --session 'YOUR_DATE(ex. 2018-01-01)'

Before you trigger, confirm whether there is a target database and tables.

## For Filter by CreatedAt in Lead

Lead by Data Connector for Marketo supports a filter with updateAt column (mk_updatedat), but updatedAt don't support incremental ingestion.
By using the following workflows, you can ingest data Lead filtered by using updatedat.

    # Run
    $ td wf start marketo_daily_load initialize_updatedat --session 'YOUR_DATE(ex. 2018-01-01)'
    $ td wf start marketo_daily_load daily_load_lead_updatedat --session 'YOUR_DATE(ex. 2018-01-01)'

NOTE: Not all Marketo Account have the feature to filter by updatedAt. In this case, you would see this error; "Marketo API Error, code: 1035, message: Unsupported filter type for target subscription: updatedAt".

# Next Step

If you have any questions, please contact support@treasure-data.com.
