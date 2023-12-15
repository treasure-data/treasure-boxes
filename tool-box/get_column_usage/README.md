# Get Column Usage Tool
This is a workflow for checking the frequency and location of use of each column set in ParentSegment by outputting them to a table.

# How To Use

 1. Retrieve the files and upload them to Treasure Data.
It is recommended to upload the files using [TD Toolbelt](https://docs.treasuredata.com/display/public/PD/Installing+TD+Toolbelt+and+Treasure+Agent).
 2. Execute the workflow after changing the contents of the uploaded dig file accordingly.

# Configuration

Change the contents of the dig file to match your Treasure Data environment.

| Parameter/Task | Option | Description | Required | 
| -------- | ----------- | ----------- | ----------- |
| timezone |  |   Set your local timezone. ||
| schedule |  |  Set if you want the workflow to run on schedule. ||
| _export | docker:<br>image | Docker image used within the workflow. ||
|  | td:<br>database | Database where output tables are to be stored. | Yes
| +exec<br>　py>: | database |  No need to change as it has already been set up above. ||
|  | parent_segment_id_list | ID of the target parent segment.<br>Multiple IDs can be set up as shown below.<br><img src="https://drive.google.com/uc?export=view&id=1iGJCGCounNTpHqdateALFRUk6hZD54Qm" width="50%">| Yes |
| | _env:<br>TD_API_KEY | When you are not authorized to create tables for the database specified above, you  need to register the appropriate user's Master API key as `td.apikey` in [secrets](https://docs.treasuredata.com/display/public/PD/Setting+Workflow+Secrets+from+TD+Console).||
| | _env:<br>TD_ENDPOINT | When your Treasure Data region is not US, you need to change to an API endpoint in the [appropriate region](https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints).||
| | _env:<br>SESSION_TIME | Execution time of the workflow.<br>This value is stored in `time` column of the output tables.||


# Output Tables
When this workflow is completed, data is output to the following four tables . 
If a table does not exist, a new table will be created, and if it exists, data will be appended to it.

## counts_columns_used_in_activations
The table stores the number of activations that use each column for output mapping.

| Column | Description | 
| -------- | ----------- |
| column | Column name used for output mapping. <br>When "Export All Columns" is checked in the setting of activation, the value `__allColumns__` is stored.| 
| count | Number of activations that use the column for output mapping. |
| parent_segment_id | ID of the target parent segment. |
| time | Execution time of the workflow.|

## counts_columns_used_in_segments
The table stores the number of segments that use each column for extraction criteria.

| Column | Description | 
| -------- | ----------- |
| column | Column name used for extraction criteria. <br>Values are stored in the form `(DATABASE).(COLUMN)`| 
| count | Number of segments that use the column for extraction criteria. |
| parent_segment_id | ID of the target parent segment. |
| time | Execution time of the workflow. |

## list_columns_used_in_activations
The table stores the list of activations that use each column for output mapping.

| Column | Description | 
| -------- | ----------- |
| segment_id | ID of the segment for which the activation is intended. |
| segment_name | Name of the segment. |
| activation_id | ID of the activation that use the column for output mapping. |
| activation_name | Name of the activation. |
| column_name | Name od the column used for output mapping.| 
| parent_segment_id | ID of the target parent segment. |
| time | Execution time of the workflow. |

## list_columns_used_in_segments
The table stores the list of segments that use each column for extraction criteria.

| Column | Description | 
| -------- | ----------- |
| segment_id | ID of the segment that use the column for extraction criteria. |
| segment_name | Name of the segment. |
| column_name | Name of column used for extraction criteria. <br>Values are stored in the form `(DATABASE).(COLUMN)`| 
| parent_segment_id | ID of the target parent segment. |
| time | Execution time of the workflow. |


