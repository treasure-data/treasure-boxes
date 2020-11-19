# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow.
You can export result to Your PostgreSQL without running the same query.

## Note

Using `td_result_export` operator is much easier and simpler for calling API by yourself.  
If you want to know how to use `td_result_export`, please check the [Doc](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1084693/Reference+for+Treasure+Data+Operators#td_result_export%3E%3A)  

The sample is [here](https://github.com/treasure-data/treasure-boxes/blob/master/scenarios/result_export/export_result_prallel.dig)

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
https://tddocs.atlassian.net/wiki/spaces/PD/overview


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
https://tddocs.atlassian.net/wiki/spaces/PD/pages/223379597/Setting+Workflow+Secrets+from+the+Command+Line

Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_postgresql export_result_postgresql --session now
```

## Next Step
If you have any questions, please contact to support@treasuredata.com.
