# Workflow: Scenario (Load file name as a column from GCS)

## Scenario

The purpose of this scenario is to capture loaded file name as data from Google Cloud Storage(GCS) on Google Cloud Platform(GCP).


*Steps*
1. Obtain file names and file contents from multiple files in a specific bucket of GCS.
2. Register the file name and the contents of the file in the table.

In this scenario, the custom scripts are used. Please refer to the Treasure data documentation for custom script.

 - [Custom Scripts](https://docs.treasuredata.com/display/public/PD/Custom+Scripts)

This scenario is just an example of how to get the file name and file contents using custom script. You don't necessarily have to match the file format to achieve this, but you can use this code as a reference to create your own.

# How to Run for Server/Client Mode
Here's how to run this sample to try it out.

Preparation, you have to do the follows.
- Create a GCP service account with read/write permissions for GCS and obtain a credential file.
- Save a credential file named "credential.json" in the local folder.(This file do not need to upload, Don't leak this file.)
- Since GCS bucket name is unique, change the bucket name from "td_test_bucket" to an appropriate one.
- create a GCS bucket and create folder "files" and "with_filename".
- Upload the files in the files folder of this sample to the files folder of the GCS you created.
- Change "database_name" in gcs_filename_add.dig to an appropriate name.
- Files in the Local folder should be removed before running.


First, please upload the workflow.

    # Upload
    $ td wf push gcs_filename_add

And Set the GCP service account credential to the workflow secret as follows.

    td wf secrets --project gcs_filename_add --set gcp.json_key=@credential.json


You can trigger the session manually to watch it execute.

    # Run
    $ td wf start gcs_filename_add gcs_filename_add --session now

After executed, the "data.tmp" will be created in the "with_filename" folder on GCS and created td table "master_with_filename" in TD.


# Next Step

If you have any questions, please contact to support@treasuredata.com.
