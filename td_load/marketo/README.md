# Workflow: td_load Example (Marketo)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Marketo](https://docs.treasuredata.com/display/public/INT/Marketo+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set marketo.account_id
    $ td wf secrets --project td_load_example --set marketo.client_id
    $ td wf secrets --project td_load_example --set marketo.client_secret

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load_activity_log.yml](config/daily_load_activity_log.yml)
- [config/daily_load_lead.yml](config/daily_load_lead.yml)
- [config/daily_load_program_members.yml](config/daily_load_program_members.yml)

If you use Treasure Workflow UI, overwrite above parameters into ${secret:marketo.xxxx} in yml files directly.

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

Before you trigger, confirm whether there is a target database and tables.
    
# Required Keys

| Keys          | Description |
| ------------- | ----------- |
| account_id    | Marketo Munchkin ID. |
| client_id     | Marketo client ID. |
| client_secret | Marketo client sectet. |
| target        | Marketo import source. |

Required values exists depending on `target` value:

| target | Required keys |
| ------ | -------- |
| lead     | from_date |
| activity | from_date |
| campaign | |
| all_lead_with_list_id | |
| all_lead_with_program_id | |
| program | tag_type, tag_value, earliest_updated_at, latest_updated_at, filter_values |
| custom_object | custom_object_api_name, custom_object_filter_type, custom_object_filter_from_value, custom_object_filter_values |
| program_members | |

Note that `custom_object_filter_from_value` and `custom_object_filter_values` affect `custom_object_filter_as_text` option that specifies input filter values as text (comma separated).
The former option recognizes `custom_object_filter_as_text` as `false`, but the later regards the option as `true`.

# Next Step

If you have any questions, please contact support@treasure-data.com.
