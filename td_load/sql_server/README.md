# Workflow: td_load example (Microsoft SQL Server)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Microsoft SQL Server](https://docs.treasuredata.com/articles/data-connector-microsoft-sql-server) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

# Register Data Connector Job

Data Connector for Microsoft SQL Server supports incremental mode using incremental_columns. If you want to use it, you have to register Connector Job without schedule.


First, please prepare the load.yml refer to [Treasure Data's Data Connector for Microsoft SQL Server](https://docs.treasuredata.com/articles/data-connector-microsoft-sql-server).

Please note the following conditions in regard to connection setting:
- If you are using Azure, omit the instance name and provide the port # only.
- If you are not using Azure and want to use your own instance: please make sure that you can connect to the database using only the instance name, without the port. If the instance name does not work, you have to set the correct port instead of instance.

- Sample of [load.yml](load.yml)

Second, please register it without schedule. ([Create the schedule](https://docs.treasuredata.com/articles/data-connector-microsoft-sql-server#create-the-schedule))

    # Sample Command
    td connector:create connector_job_name "" dest_db dest_table load.yml

# How to Run workflow

You don't need to set database credentials as `secrets` because the Connector Job defined it.

So, you can upload the workflow and trigger the session manually.
You must NOT push "load.yml" because it has credential infomation. It's already registered on Data Connector job.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now

# Confirm "Config Diff"

You can check the `last_record` of imported records.

    # Sample Command & Result
    td connector:show connector_job_name
    
    ---
    Name     : connector_job_name
    Cron     :
    Timezone : UTC
    Delay    : 0
    Database : dest_db
    Table    : dest_table
    Config
    ---
    in:
      host: host_name
      .....
    
    Config Diff
    ---
    in:
      last_record:
      - 7
      - 1461826241

# Next Step

If you have any questions, please contact support@treasure-data.com.
