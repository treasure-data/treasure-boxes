# Workflow: td example (Result Output to Microsoft SQL Server)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into SQL Server tables](https://docs.treasuredata.com/articles/result-into-microsoft-sql-server) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by td wf push command.

    # Upload
    $ td wf push sample_project

Second, please set Microsoft Azure credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project sample_project --set sqlserver.password=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set sqlserver.password=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_microsoft_sql_server --session now
    
# Supplemental

JSON format of Result Output to Microsoft SQL Server is the following.

- {"type":"sqlserver","host":"host","username":"username","password":"password","database":"database","table":"table","batch_size":16777216,"mode":"insert"}

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-microsoft-sql-server)

# Next Step

If you have any questions, please contact support@treasure-data.com.
