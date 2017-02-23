# Workflow: td example (Result Output to Redshift)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into AWS Redshift](https://docs.treasuredata.com/articles/result-into-redshift) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push sample_project

Second, please set aws redshift credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project sample_project --set redshift.password=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set redshift.password=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_redshift --session now

# Supplemental

URL format of Result Output to Redshift is the following.

- redshift://username:password@hostname:port/database/table

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-redshift)

# Next Step

If you have any questions, please contact support@treasure-data.com.
