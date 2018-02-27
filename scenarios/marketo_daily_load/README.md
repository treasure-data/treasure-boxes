# Workflow: Marketo Daily Load

Data Connector for Marketo uses Marketo Bulk Export API, but the API has several limitations; filter conditions doesn't work as expected and delay arriving of activity/lead logs.

This example workflow take care of such limitations

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push marketo_daily_load

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project marketo_daily_load --set marketo.account_id=xxxxxx
    $ td wf secrets --project marketo_daily_load --set marketo.client_id=yyyyy
    $ td wf secrets --project marketo_daily_load --set marketo.client_secret=zzzzz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load_activity_log.yml](config/daily_load_activity_log.yml)
- [config/daily_load_lead.yml](config/daily_load_lead.yml)

If you use Treasure Workflow UI, overwrite above parameters into ${secret:marketo.xxxx} in yml files directly.

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

Before you trigger, confirm whether there is a target database and tables.
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
