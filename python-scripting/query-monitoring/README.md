# Query Monitoring
This workflow retrieves the detail of jobs in status `queued` and `running` every 5 minutes. Then, store the result into TD. It helps you to understand workloads and query performance.

# Installation

## Create a destination table
```
$ td db:create your_database
$ td table:create your_database monitoring
```

## Specify a table in .dig
- td_database
- td_table


## Push the code and set an API key
```
$ td wf push query-monitoring
$ td wf secrets --project query-monitoring --set td.apikey
```

