# Workflow: td example (Result Output to Twitter Tailored Audience)

This example workflow outputs data to a twitter tailorerd audience using [Writing Job Results into your Twitter Tailored Audience](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1081589/Twitter+Tailored+Audience+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in Treasure Data, please create connection by following the instructions on this page [Writing Job Results into your Twitter Tailored Audience](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1081589/Twitter+Tailored+Audience+Export+Integration)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push twitter_tailored_audience

If you want to mask any settings, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project twitter_tailored_audience --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start twitter_tailored_audience twitter_tailored_audience --session now

## Local mode

    # Run
    $ td wf run twitter_tailored_audience.dig

# Supplemental

Available parameters for `result_settings` are here.

- ad_account_id: This is your Twitter Ad Account ID (string, required)
- audience_name: Name of Tailored Audience list to create. (string, required)
- audience_type: Name of output Custom Audience. it is one of email, id, device id or handle (string, required)
- pre_hashed :  Indicates whether the data has already been normalized and hashed. If not, TD automatically normalizes and hashes the records. (boolean, default: false)
- retrylimit: Number of times to retry on failure (int, optional, default: 6)
- retry_initial_wait_msec: Interval to retry if a recoverable error happens (int, optional, default: 10000)
- max_retry_wait_msec: Maximum time in milliseconds between retrying attempts. (int, optional, default: 320000)


For more details, please see [Treasure Data documentation (GUI)](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1084846/Using+Workflow+from+TD+Console)
or [Treasure Data documentation(CLI)](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1083651/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI)

# Next Step
If you have any questions, please contact support@treasuredata.com.
