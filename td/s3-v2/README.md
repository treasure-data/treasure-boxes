# Workflow: td example (Result Output to S3 v2)

This example workflow exports TD job results into AWS S3 using the [AWS S3 v2 connector](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Export+Integration+v2) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

1. [TD Toolbelt](https://docs.treasuredata.com/display/public/PD/Installing+TD+Toolbelt+and+Treasure+Agent#InstallingTDToolbeltandTreasureAgent-InstallingTDToolbelt)
2. You will need to create a new Authentication for AWS S3 v2 in advance. Instructions can be found in the [TD documentation](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Export+Integration+v2#AmazonS3ExportIntegrationv2-UsetheTDConsoletoCreateaConnection). The connection name will be used in this example.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_s3_v2

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_s3_v2 --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_s3_v2 td_s3_v2 --session now

## Local mode

    # Run
    $ td wf run td_s3_v2.dig

# Supplemental

Available parameters for `result_settings` can be found in the [TD documentation](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Export+Integration+v2#AmazonS3ExportIntegrationv2-(Optional)ConfigureExportResultsinWorkflow)

# Next Step

If you have any questions, please contact [support@treasure-data.com](mailto:support@treasure-data.com).
