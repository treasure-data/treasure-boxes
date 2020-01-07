# Workflow: Scenario (skip zero loading)

## What is the purpose of this scenario?
If the file to be loaded is not found when we use replace mode of Data Connector, an empty table is created as a result of replacing 0 records.
We can resolve the task by using workflow like this example.


# How to Run
First, upload the project.

    # Upload
    $ td wf push skip_zero_load

Second, register the api key as a workflow secret.

    # Set secrets
    $ td wf secrets --project skip_zero_load --set s3.access_key_id
    $ td wf secrets --project skip_zero_load --set s3.secret_access_key

Now, you can refer to these credentials by ${secret:xxx}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start skip_zero_load skip_zero_load_wf --session now


# Next Step

If you have any questions, please contact [support@treasure-data.com](support@treasure-data.com).
