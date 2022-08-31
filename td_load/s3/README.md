# Workflow: td_load Example (Amazon S3)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Amazon S3](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

[Amazon S3 v2 connector](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2) is also available.
The v2 integration has enhanced security features and requested features including a new authentication method, SSE-KMS support, and quote policy.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set s3.endpoint
    $ td wf secrets --project td_load_example --set s3.access_key_id
    $ td wf secrets --project td_load_example --set s3.secret_access_key

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

Both v1 and v2 connectors have the same required keys.

| Keys     | Description |
| -------- | ----------- |
| bucket   | S3 bucket name. |
| path_prefix | Prefix of target keys. |
| access_key_id | AWS access key ID. |
| secret_access_key | AWS secret access key. |

# Next Step

If you have any questions, please contact support@treasure-data.com.
