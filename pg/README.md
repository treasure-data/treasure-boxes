# Workflow: pg

This example executes queries to PostgreSQL server using [pg operator](http://docs.digdag.io/operators/pg.html).

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push pg_example

Second, please set password for postgre server using `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project pg_example --set pg.password=xyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set pg.password=xyzxyz    

Now, you can trigger the session manually.

    # Run
    $ td wf start pg_example pg_example --session now

You can check the workflow status from [Workflow console](https://workflows.treasuredata.com/).

# Next Step

If you have any questions, please contact support@treasure-data.com.
