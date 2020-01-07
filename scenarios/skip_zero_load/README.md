# Workflow: Scenario (skip zero loading)

## What is the purpose of this scenario?
If the file to be loaded is not found when we use replace mode of Data Connector, an empty table is created as a result of replacing 0 records.
We can resolve the task by using workflow like this example.

# Overview of this Example
1. drop/create temporary table(this is a empty table)
2. load from S3 into temporary table
3. check the number of loaded records
    1. when the number of loaded records is 0, output message into log
    2. when the number of loaded records is greater than 0, rename temporary table with producation table

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
