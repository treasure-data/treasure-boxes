# DataRobot2TreasureData
This digdag workflow creates a table on Treasure Data generated from DataRobot's prediction result using DataRobot Python client.

## Prerequisite
- Supposes that you already have built a ML model and set Treasure Data as a data source on DataRobot.
- Following parameters are necessary.  

| Variable | Description | Example |
| -------- | ----------- | --------|
| td.apikey | Master API Key for Treasure Data. [link] | `1234/abcdefghijklmnopqrstuvwxyz1234567890`|
| td.username | Email address to log in Treaure Data's console | `hogehoge@treasure-data.com` |
| td.password | Password to log in Treasure Data's console | `xxxxxx` |
| dr.apikey | DataRobot's API Key. \*  | `ABcdEFGhIJk12MNoPqrS3uvW_xyz123`|
| dr.project_id | Project ID for DataRobot. \* | `5d3e76e931c473290afae6fd` | 
| dr.model_id | Model ID for DataRobot. \* | `5d3e7b875844414bffba1579` | 
| dr.datasource_id | Data source ID for DataRobot | `5d3e76d06cd83a00139c6a72` |

\* You can get these parameters from the DataRobot's screen below.  
> Select Model > Predict > Deploy Model API
<img src="./images/datarobot.png" width="400px">

## Push the code and set variables
```
td wf push --project datarobot_integration
td wf secret --project datarobot_integration --set dr.apikey
td wf secret --project datarobot_integration --set td.apikey
td wf secret --project datarobot_integration --set td.username
td wf secret --project datarobot_integration --set td.password
```
