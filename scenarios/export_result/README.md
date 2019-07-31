# Workflow: export_result
This example shows how use result_export API in Treasure Data workflow. This API is useful in below case.
- When you want to export query result to mulitipile services like S3, RedShift, and Tablueau **without executing the query again**.

## Scenario
The purpose of this secenario is to export query result to **mulitipile** destinations. So for, you can specify only one export setting on Web UI. In this scenario, you would use http:> operator instead of 

## How to Run for Server/Client Mode
First, please upload the workflow.
```
# Upload
$ td wf push export_result
```

Second, please set your td account credentials by ```td wf secrets``` command.
```
# Set Secrets
$ td wf secret --project export_result_exmaple --set td.apikey
$ td wf secret --project export_result_example --set http.authorization
```

Note: http.authorization is used as header in your API request. 
Value which would be set in http.authorization must seem like this: ```TD1 Your APIKey```

For detail, please refer to the below page.
https://support.treasuredata.com/hc/en-us/articles/


Third, please set your other services' credentials by ```td wf secrets``` command.
```
# Set Secrets again
$ td wf secret --project export_result_example --set aws.s3.access_key_id
```

If you don't want to execute command repeatedly, you can set secret from a file.
```
$ td wf secret --project export_result_example --set @credential.yml
```

For detail, please refer to below page.
https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management#L5

Finally, you can trigger the session manually.

```
# Run
$ td wf start export_result_example --session now
```

## Next Step
If you have any questions, please contact to support@treasuredata.com.
