# Workflow: td example (Result Output to Facebook Custom Audience)

This example workflow outputs data to a Facebook custom audience using [Writing Job Results into Facebook Custom Audience](https://support.treasuredata.com/hc/en-us/articles/360001288928-Writing-Job-Results-into-Facebook-Custom-Audience) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in Treasure Data, please create connection by following the instructions on this page [Writing Job Results into Facebook Custom Audience](https://support.treasuredata.com/hc/en-us/articles/360001288928-Writing-Job-Results-into-Facebook-Custom-Audience) 

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_facebook_custom_audience

If you want to mask any settings, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

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

- ad_account_id: your Facebook Ad Account ID, without `act_` prefix _(string, required)_
- api_version: Facebook Graph API version _(string, default: "v2.11")_
- app_secret: if set, `appseret_proof` parameter will be used to access API _(string, optional)_
- access_token: Access Token. We recommend to use never-expired token (see [here](https://github.com/treasure-data/embulk-input-facebook_ads_reporting#never-expired-access-token) for more details) _(string, required)_
- output_name: name of output Custom Audience _(string, required)_
- description: description of output Custom Audience _(string, optional)_
- pre_hashed : Whether or not the data has already been hashed. If not, the plugin will automatically hash the data _(boolean, default: false)_
- customer_file_source : Specify the source of the user information collected into this file _(string, default: null, values: USER_PROVIDED_ONLY, PARTNER_PROVIDED_ONLY, BOTH_USER_AND_PARTNER_PROVIDED)_


For more details, please see [Treasure Data documentation (GUI)](https://support.treasuredata.com/hc/en-us/articles/360001262227-Treasure-Workflow-Quick-Start-Tutorial-for-the-GUI)
or [Treasure Data documentation(CLI)](https://support.treasuredata.com/hc/en-us/articles/360001262207-Treasure-Workflow-Quick-Start-Tutorial-for-the-CLI)

# Next Step
If you have any questions, please contact support@treasuredata.com.
