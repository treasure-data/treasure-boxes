# Workflow: td example (Result Output to Another TD Account)

This example workflow ingests data using [Treasure Data's Writing Job Results into TD Table)](https://docs.treasuredata.com/articles/result-into-td) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/1683a6fdfe390f7942c677e18ba1cca8.png)

![](https://t.gyazo.com/teams/treasure-data/9d7e21e7b4442abbb9e009eebcd19681.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push another_td_account

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project another_td_account --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.


You can trigger the session manually.

    # Run
    $ td wf start another_td_account another_td_account --session now
    
# Supplemental

Available parameters for `result_settings` are here.

- user_database_name: (string, required)
- user_table_name: (string, required)
- mode: (string(append|replace), default append)
- time: (string, optional)

## Endpoints are below.

- AWS US: api.treasuredata.com
- IDCF  : api.ybi.idcfcloud.net
- AWS TOKYO: api.treasuredata.co.jp

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-td#two-ways-to-modify-data-appendreplace)

# Next Step

If you have any questions, please contact support@treasure-data.com.
