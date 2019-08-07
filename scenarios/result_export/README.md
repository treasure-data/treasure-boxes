# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow. 
You can export result to Your S3 & Tableau without running the same query.

###  Note: **This is experimental usage.**

## Scenario

1. Run Query
2. Export Result to S3 & Tableau

## How to Run for Server/Client Mode
First, please upload the workflow.
```
# Upload
$ td wf push export_result_paralell
```

Second, please set your td account credentials by ```td wf secrets``` command.
```
# Set Secrets
$ td wf secret --project export_result_parallel --set td.apikey
$ td wf secret --project export_result_parallel --set http.authorization
```

Note: http.authorization is used as header in your API request. 
You must http.authorization like this : ```TD1 <Your APIKey>```

For detail, please refer to the below page.
https://support.treasuredata.com/hc/en-us/articles/


Third, please set your other services' credentials by ```td wf secrets``` command.
```
# Set Secrets again
$ td wf secret --project export_result_parallel --set aws.s3.access_key_id
```

If you don't want to execute command repeatedly, you can set secret from a file.
```
$ td wf secret --project export_result_parallel --set @credential.yml
```

For detail, please refer to below page.
https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management#L5

Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_parallel export_result_parallel --session now
```

## If you want to export results to more services

Please refer to each ```export_result_<Service Name>``` directories.

## Next Step
If you have any questions, please contact to support@treasuredata.com.
