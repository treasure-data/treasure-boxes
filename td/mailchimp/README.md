# Workflow: td Example (Result Output to Mailchimp)

[Our blog post](https://blog.treasuredata.com/blog/2016/08/31/increase-customer-engagement-with-mailchimp/) describes an importance of customer engagement with Mailchimp and Treasure Data

This example workflow gives you an overview and directions on how to build personalized email lists on Mailchimp using [Treasure Data's Result Output to Mailchimp](https://docs.treasuredata.com/articles/result-into-mailchimp) with [td](http://docs.digdag.io/operators/td.html) operator.

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/cb39d5ab2576b9e1a184cda6e737dbf4.png)

![](https://t.gyazo.com/teams/treasure-data/cbbc2f734d6f2e2db06abce3237a140a.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push mailchimp_export

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project mailchimp_export --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start mailchimp_export mailchimp_export --session now

## Local mode

    # Run
    $ td wf run mailchimp_export.dig

# Supplemental

Available parameters for `result_settings` are here.

- list_id: (string, required)
- update_existing: control whether to update members that are already subscribed to the list or to return an error (boolean, default: false)
- email_column: (string, default: 'email')
- fname_column: (string, default: 'fname')
- lname_column: (string, default: 'lname')
- merge_fields: Array for additional merge fields/ TAG in MailChimp dashboard (array, optional, default: nil)
- grouping_columns: Array for group names in MailChimp dashboard(array, default: nil)
- replace_interests: (boolean(true|false), default true)
- double_optin: (boolean(true|false), default false)
- retry_limit: (int, default 6)
- retry_initial_wait_msec: (int, default 1000)
- max_retry_wait_msec: (int, default 32000)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-mailchimp)

# Next Step

If you have any questions, please contact support@treasuredata.com.
