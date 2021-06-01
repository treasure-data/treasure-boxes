# Workflow: Scenario (Load file name as a column from S3)

## Scenario

The purpose of this scenario is to capture loaded file name as data from S3 on AWS.


*Steps*
1. Obtain file names and file contents from multiple files in a specific bucket of S3.
   <br>the sample
   <br>file name: files_aaa_20210401
   <br>contents:
   ```
   aaa
   ```
   The file name is given a date, like a daily file. The file content is simply a single item. You will prepare several similar files.

2. Register the file name and the contents of the file in the table.

In this scenario, the custom scripts are used. Please refer to the Treasure data documentation for custom script.

 - [Custom Scripts](https://docs.treasuredata.com/display/public/PD/Custom+Scripts)

This scenario is just an example of how to get the file name and file contents using custom script. You don't necessarily have to match the file format to achieve this, but you can use this code as a reference to create your own.

# How to Run for Server/Client Mode
Here's how to run this sample to try it out.

Preparation, you have to do the follows.
- Since S3 bucket name is unique, change the bucket name from "td-test-bucket" to an appropriate one.
- create a S3 bucket and create folders "files" and "with_filename".
- Upload the files in the files folder of this sample to the files folder of the S3 you created.
- Change "database_name" in s3_filename_add.dig to an appropriate name.
- Files in the Local folder should be removed before running.


First, please upload the workflow.

    # Upload
    $ td wf push s3_filename_add

And Set the S3 Access key ID and Secret access key to the workflow secret as follows.

    # Set Secrets
    $ td wf secrets --project s3_filename_add --set s3.access_key_id
    $ td wf secrets --project s3_filename_add --set s3.secret_access_key


You can trigger the session manually to watch it execute.

    # Run
    $ td wf start s3_filename_add s3_filename_add --session now

After executed, the "data.tmp" will be created in the "with_filename" folder on S3 and created td table "master_with_filename" in TD.


# Next Step

If you have any questions, please contact to support@treasuredata.com.
