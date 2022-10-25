# Workflow: td example (Result Output to Google AdWords Remarketing Lists)

This example workflow outputs data to a google adwords remarketing lists using [Writing Job Results into Google AdWords Remarketing Lists](https://docs.treasuredata.com/display/public/INT/Google+Ads+Remarketing+Lists+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in Treasure Data, please create connection by following the instructions on this page [Writing Job Results into Google Adwords Remarketing Lists](https://docs.treasuredata.com/display/public/INT/Google+Ads+Remarketing+Lists+Export+Integration)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push googleads_remarketing_lists

If you want to mask any settings, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project googleads_remarketing_lists --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start googleads_remarketing_lists googleads_remarketing_lists --session now

## Local mode

    # Run
    $ td wf run googleads_remarketing_lists.dig

# Supplemental

Available parameters for `result_settings` are here.

- client_customer_id : Your AdWords Customer ID, the format is: xxx-yyy-zzzz (string, required)
- name : Name for the user list. (string, required)
- description : Description of the user list. (string, optional)
- app_id : Your mobile application ID. Required when you export Mobile Advertising ID (string, optional)
- mode : output mode. Supported values: append or replace (string, optional, default: append)
- membership_lifespan : Number of days users' contact info stays on the user list (int, optional, default: 10000)
- batch_size : Number of records to upload in each batch (int, optional, default: 100000)
- maximum_retries : Number of retries before system gives up. (int, optional, default: 5)
- initial_retry_interval_millis : Initial retry time wait in milliseconds. (int, optional, default: 500)
- maximum_retry_interval_millis : Max retry wait in milliseconds. (int, optional, default: 300000)


For more details, please see [Treasure workflow documentation (GUI)](https://docs.treasuredata.com/display/public/PD/Using+Workflow+from+TD+Console)
or [Treasure workflow documentation (CLI)](https://docs.treasuredata.com/display/public/PD/Using+TD+Workflow+from+the+Command+Line)

# Next Step
If you have any questions, please contact support@treasuredata.com.
