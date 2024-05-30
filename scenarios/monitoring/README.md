# Note
Monitoring workflows are collection how to use REST API.
These workflows are ready to use after pushing these workflow to TD and registering one secret(td.apikey).
However, some of them do not work depending on each TD environment.
For example, if your TD environment would not have Policy-Based Permission feature, initial_ingest_policy and incremental_ingest_policy workflows of basic_monitoring don't work.

# FAQ
## 504 Server Error: Gateway Time-out error
This error is a temporary network error.
Therefore, try to run workflows again later.
If this error occurs frequently, reduce the value of *count* parameter in each task.

## 403 Client Error: Forbidden for url: https://xxxxxx
This error is that owner of td.apikey don't have enough psermission.
Monitoring Workflow ingest all TD objects.
Therefore, owner of td.apikey must be admin and have all permission for TD functions.
