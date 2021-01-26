# Workflow: td example (Result Output to nend)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into nend](https://docs.treasuredata.com/display/public/INT/nend+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/aecb26e71143d76d012ae2fa560b42f6.png)

![](https://t.gyazo.com/teams/treasure-data/b4ed6e7904ea456d095c723417d10caa.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_nend

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_nend --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_nend td_nend --session now

## Local mode

    # Run
    $ td wf run td_nend.dig

# Supplemental

Available parameters for `result_settings` are here.

- target_type: (string(idfa|idfamd5|gaid|nenduu), required)
- target_name: (string, required)
- retry_initial_wait_sec: (integer, default 5)
- retry_limit: (integer, default 4)
- mode: (string(append|replace), default replace)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/nend+Export+Integration)

# Next Step

If you have any questions, please contact support@treasure-data.com.
