# Workflow: td example (Result Output to Microsoft Power BI)

This example workflow ingests data using [Treasure Data's Microsoft Power BI Export Integration](https://docs.treasuredata.com/display/INT/Microsoft+Power+BI+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites
In order to register your credential in TreasureData, please create Authentication setting on TD Console.
For URL of TD Console, please refer to [Endpoints](https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints#SitesandEndpoints-Endpoints).

You can know how to create the Authentication from [documentation](https://docs.treasuredata.com/display/INT/Microsoft+Power+BI+Export+Integration) .


The name of the Authentication is used in the dig file.

# How to Run
First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push <project_name>


You can trigger the session manually.

    # Run
    $ td wf start <project_name> <workflow_name> --session now


# Supplemental
Available parameters for `result_settings` are here.

- workspace_id: Shared workspace or group id(string, default null)
- table: Name of the table which needs to create in Power BI dashboard or existing table name (string, required)
- replace_existing_data: truncate the table before pushing data(boolean(true|false), default false)
- retry_initial_wait_msec: Parameter which provides initial wait for each retry logic in milliseconds to call Power BI API for specified database and table to push data to Power BI (int, default 1000)
- retry_limit: Parameter which provides number of times to retry calling Power BI API for specified database and table to push data to Power BI (int, default 7)
- max_retry_wait_msec: Parameter which provides maximum wait for each retry in milliseconds to call Power BI API for specified database and table to push data to Power BI (int, default 30000)
- default_retention_policy: 'None' and 'basicFIFO'(string, default None)
- batch_size: Parameter which provides limit max rows per request(int, default 10000, min 100, max 10000)
- service_plan_rows_limit: Parameter whihc provides limit max rows per hour per dataset with service plans(int, default 1000000, min 100, max 1000000)

# Next Step
If you have any questions, please contact support@treasure-data.com.
