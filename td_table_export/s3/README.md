# Workflow: td_table_export example (Result Output to S3)

This example workflow exports TD job results into AWS S3 with [td_table_export](http://docs.digdag.io/operators/td_table_export.html) operator.

# Prerequisites

[TD Toolbelt](https://docs.treasuredata.com/display/public/PD/Installing+TD+Toolbelt+and+Treasure+Agent#InstallingTDToolbeltandTreasureAgent-InstallingTDToolbelt)

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_table_export_s3

Create workflow secrets for your AWS access key. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

You will need to create two secrets: `aws.s3.access_key_id` and `aws.s3.secret_access_key`. To get your access key, please see the [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).

    # Set Secrets
    $ td wf secrets --project td_table_export_s3 --set aws.s3.access_key_id --set aws.s3.secret_access_key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set aws.s3.access_key_id --set aws.s3.secret_access_key

You can trigger the session manually.

    # Run
    $ td wf start td_table_export_s3 export --session now

## Local mode

    # Run
    $ td wf run export.dig

# Next Step

If you have any questions, please contact [support@treasure-data.com](mailto:support@treasure-data.com).
