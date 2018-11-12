# Workflow: td example (Result Output to Salesforce)

This example workflow exports TD job results into Salesforce [Treasure Data's Writing Job Results into Salesforce](https://docs.treasuredata.com/articles/result-into-salesforce) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

Salesforce.com organization and username, password, and security token for API integration
https://docs.treasuredata.com/articles/result-into-salesforce#prerequisites

![](https://t.gyazo.com/teams/treasure-data/0153ad6cb81d8a2ca71d3c55fe6c21e1.png)

![](https://t.gyazo.com/teams/treasure-data/66f7e0bd60707e80a80649ba92a22639.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_sfdc

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sfdc --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_sfdc td_sfdc --session now

## Local mode

    # Run
    $ td wf run td_sfdc.dig

# Supplemental

Available parameters for `result_settings` are here.

- object: (string, required)
- mode: (string(append|truncate|update), default append)
- upsert: (boolean, available for update mode, default true)
- unique: (string, available for update mode)
- hard_delete: (boolean, available for truncate mode, default false)
- concurrency_mode: (string(parallel|serial), default parallel)
- retry: (integer, default 2)
- split_records: (integer, default 10000)

For more details on Result output to Salesforce, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-salesforce)

# Next Step

If you have any questions, please contact support@treasure-data.com.
