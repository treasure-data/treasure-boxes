# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow.
You can export result to Your FTP serber without running the same query.

## Note

Using `td_result_export` operator is much easier and simpler for calling API by yourself.
If you want to know how to use `td_result_export`, please check the [Doc](https://docs.treasuredata.com/display/public/PD/Reference+for+Treasure+Data+Operators#ReferenceforTreasureDataOperators-td_result_export%3E:)

The sample is [here](https://github.com/treasure-data/treasure-boxes/blob/master/scenarios/result_export/export_result_prallel.dig)


## Scenario

1. Run Query
2. Export Result to FTP Server

## Prerequisite

Create a connection on console

![](https://t.gyazo.com/teams/treasure-data/ce6d63afb6917ee99d7a5fdace2b7ccd.png)

![](https://t.gyazo.com/teams/treasure-data/55071234c2d489b7bb1bdbb342a067e0.png)

Connection name is used in Workflow file

## How to Run for Server/Client Mode
First, please upload the workflow after making changes to the connection and filepath variable defined in `_export` section.

```
# Upload
$ td wf push export_result_ftp
```

Second, please set your td account credentials by ```td wf secrets``` command.
```
# Set Secrets
$ td wf secret --project export_result_ftp --set td.apikey
```

For detail, please refer to the below page.
https://docs.treasuredata.com/display/public/PD/Product+Documentation+Home


Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_ftp export_result_ftp --session now
```

## Next Step
Further reading: https://docs.treasuredata.com/display/public/PD/About+Using+Workflows+to+Export+Data+with+TD+Toolbelt#AboutUsingWorkflowstoExportDatawithTDToolbelt-FTPResultOutputusingresult_settingsExample
If you have any questions, please contact to support@treasuredata.com.
