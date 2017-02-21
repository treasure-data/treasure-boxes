# Workflow: td example (Result Output to s3)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into AWS S3](https://docs.treasuredata.com/articles/result-into-s3) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please set s3 credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project sample_project --set s3.access_key_id=xyzxyzxyzxyz
    $ td wf secrets --project sample_project --set s3.secret_access_key=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set s3.access_key_id=xyzxyzxyzxyz
    $ td wf secrets --local --set s3.secret_access_key=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push sample_project
    
    # Run
    $ td wf start sample_project sample --session now
    
# Supplemental

URL format of Result Output to s3 is the following.

- s3://access_key_id:secret_access_key@/bucket_name/path/to/file.csv?option=value

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-s3)

# Next Step

If you have any questions, please contact support@treasure-data.com.
