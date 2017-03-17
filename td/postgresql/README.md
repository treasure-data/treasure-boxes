# Workflow: td example (Result Output to PostgreSQL)

This example workflow ingests data using [Treasure Data's Writing Job Results into PostgreSQL Table)](https://docs.treasuredata.com/articles/result-into-postgresql) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_postgresql

Second, please set destination td account's master apikey by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set postgresql.host=xyz
    $ td wf secrets --project td_load_example --set postgresql.port=5432
    $ td wf secrets --project td_load_example --set postgresql.user=abcde
    $ td wf secrets --project td_load_example --set postgresql.password=fghijklmn

    # Set Secrets on your local for testing
    $ td wf secrets --local --set postgresql.host=xyz
    $ td wf secrets --local --set postgresql.port=5432
    $ td wf secrets --local --set postgresql.user=abcde
    $ td wf secrets --local --set postgresql.password=fghijklmn

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_postgresql td_postgresql --session now
    
# Supplemental

URL format of Result Output to PostgreSQL is the following.

- postgresql://username:password@hostname:port/database/table

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-postgresql#result-output-url-format)

# Next Step

If you have any questions, please contact support@treasure-data.com.
