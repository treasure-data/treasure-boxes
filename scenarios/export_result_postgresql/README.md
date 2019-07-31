# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow. 
You can export result to Your PostgreSQL without running the same query.

## Scenario

1. Run Query
2. Export Result to PostgreSQL

## How to Run for Server/Client Mode
First, please upload the workflow.
```
# Upload
$ td wf push export_result_postgresql
```

Second, please set your td account credentials by ```td wf secrets``` command.
```
# Set Secrets
$ td wf secret --project export_result_postgresql --set td.apikey
$ td wf secret --project export_result_postgresql --set http.authorization
```

Note: http.authorization is used as header in your API request. 
You must http.authorization like this : ```TD1 <Your APIKey>```

For detail, please refer to the below page.
https://support.treasuredata.com/hc/en-us/articles/


Third, please set your other services' credentials by ```td wf secrets``` command.
```
# Set Secrets again
$ td wf secret --project export_result_postgresql --set postgreUser // PostgreSQL Username
$ td wf secret --project export_result_postgresql --set postgrePass // User's password
$ td wf secret --project export_result_postgresql --set postgreHost // PostgreSQL Host Name
$ td wf secret --project export_result_postgresql --set postgrePort // This is option
$ td wf secret --project export_result_postgresql --set postgreDatabase // PostgreSQL Database
$ td wf secret --project export_result_postgresql --set postgreTable // PostgreSQL Table
```

For detail, please refer to below page.
https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management#L5

Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_postgresql export_result_postgresql --session now
```

## Next Step
If you have any questions, please contact to support@treasuredata.com.
