# Integration for DataRobot
This example creates a table on Treasure Data from DataRobot's prediction result.

## Push the code and set variables
```
td wf push --project datarobot_integration
td wf secret --project datarobot_integration --set datarobot.apikey
td wf secret --project datarobot_integration --set td.apikey
td wf secret --project datarobot_integration --set td.username
td wf secret --project datarobot_integration --set td.password
```

You must set proper values for arguments below.
- database (Destination database for Treasure Data)
- table (Destination table for Treasure Data)
- project_id (from DataRobot)
- model_id (from DataRobot)
- datasource_id (from DataRobot)
