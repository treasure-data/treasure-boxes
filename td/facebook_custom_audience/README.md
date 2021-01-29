# Workflow: td example (Result Output to Facebook Custom Audience)

This example workflow outputs data to a Facebook custom audience using [Writing Job Results into Facebook Custom Audience](https://docs.treasuredata.com/display/public/INT/Facebook+Custom+Audience+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in Treasure Data, please create connection by following the instructions on this page [Writing Job Results into Facebook Custom Audience](https://docs.treasuredata.com/display/public/INT/Facebook+Custom+Audience+Export+Integration)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_facebook_custom_audience

If you want to mask any settings, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_facebook_custom_audience --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_facebook_custom_audience export_facebook_custom_audience --session now

## Local mode

    # Run
    $ td wf run facebook_custom_audience.dig

# Supplemental

Available parameters for `result_settings` are here.

- ad_account_id: your Facebook Ad Account ID, without act_ prefix (string, required)
- api_version: Facebook Graph API version (string, default: "v2.11")
- output_name: name of output Custom Audience (string, required)
- description: description of output Custom Audience (string, optional)
- pre_hashed : Whether or not the data has already been hashed. If not, the plugin will automatically hash the data (boolean, default: false)
- customer_file_source : Specify the source of the user information collected into this file (string, default: null, values: USER_PROVIDED_ONLY, PARTNER_PROVIDED_ONLY, BOTH_USER_AND_PARTNER_PROVIDED)
- retryInitialWaitMsec: time to wait between retries (int, required, default: 60000).
- retryLimit: Number of times to retry on failure (int, optional, default: 5)


For more details, please see [Treasure Data documentation (GUI)](https://docs.treasuredata.com/display/public/PD/Using+Workflow+from+TD+Console)
or [Treasure Data documentation(CLI)](https://docs.treasuredata.com/display/public/PD/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI)

# Next Step
If you have any questions, please contact support@treasuredata.com.
