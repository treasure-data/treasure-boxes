Table Schema Change Detection
======

This Treasure Data workflow is intended to prevent new columns being added to data tables due to changing inputs. It 
assumes that new data is first going to a staging table before being appended to a final data table. This workflow will 
mitigate the risk of exposing PII as well as give greater control to admins and project leaders who need to ensure data 
loads contain only specified columns.

This workflow will warn you through email when there is:  

1. A new column name, or  

2. The same column name with different data type.

## Requirements

1. A Treasure Data Account that uses staging tables to update final data tables.

2. A table in your database with the columns 'final_table', 'final_database' and 'staging_table', 'staging_database' 
that maps one to the other (this table name should be set as the value for the 'tablemap_table' variable in the 
workflow - include full database.table name).

|final_table    |final_database    |staging_table   |staging_database   |
|:-------------:|:----------------:|:--------------:|:-----------------:|
|example_final  |example_final_db  |example_stage    |example_stageDB   |
|example_final1 |example_final_db  |example_stage1   |example_otherDB   |


## Set Up

1. Create a new workflow in your [Treasure Data Console](https://console.treasuredata.com/app/workflows/ "Treasure Data").

2. Copy and paste the entire table_schema_change_detection.dig file into the workflow.

3. Add a project file for each query in the 'sql' folder and make sure to set names to reflect the query file names. 
Paste in the queries.

4. Adjust the variables in the _export step of the workflow to configure your database, tablemap_table, 
and email_warnings reciepients._

5. Test it out!
