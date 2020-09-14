# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow.
You can export result to Your FTP serber without running the same query.

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
https://tddocs.atlassian.net/wiki/spaces/PD/overview


Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_ftp export_result_ftp --session now
```

## Next Step
Further reading: https://tddocs.atlassian.net/wiki/spaces/PD/pages/1081684/About+Using+Workflows+to+Export+Data+with+TD+Toolbelt#FTP-Result-Output-using-result_settings-Example
If you have any questions, please contact to support@treasuredata.com.
