# Workflow: export_result to TD
This example shows how use result_export API in Treasure Data workflow. 
You can export result to Another Treasure Data Account without running the same query.

## Scenario

1. Run Query
2. Export result to another TD account.

## How to Run for Server/Client Mode
First, please upload the workflow.
```
# Upload
$ td wf push export_result_td
```

Second, please set your td account credentials by ```td wf secrets``` command.
```
# Set Secrets
$ td wf secret --project export_result_td --set td.apikey
$ td wf secret --project export_result_td --set http.authorization
```

Note: http.authorization is used as header in your API request. 
You must http.authorization like this : ```TD1 <Your APIKey>```

For detail, please refer to the below page.
https://support.treasuredata.com/hc/en-us/articles/


Third, please set your other services' credentials by ```td wf secrets``` command.
```
# Set Secrets again
$ td wf secret --project export_result_td --set tdApikey // User's apikey
$ td wf secret --project export_result_td --set tdEndpoint // This is option. Default is api.treasuredata.com
$ td wf secret --project export_result_td --set tdDatabase // Database name
$ td wf secret --project export_result_td --set tdTable // Tabale
```

For detail, please refer to below page.
https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management#L5

Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_td export_result_td --session now
```

## Next Step
If you have any questions, please contact to support@treasuredata.com.
