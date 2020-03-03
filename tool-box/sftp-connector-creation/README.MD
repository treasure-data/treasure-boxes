# SFTP Connector Creation using Python in Treasure Data


## Introduction
The main objective of this custom python script to reduce/save the time and effort while creating the sftp connector manually using UI.

  * What this code does?
    1. It needs the seed file, which will contain the sftp detail (credentials and Path) and TD detail (apikey and db details).
    2. DB details in above seed file will be picked dynamically as per file. Table name will be same as file name over sftp with prefix as parent folder.
    3. Once sftp connection is established, then python scripts iterates over each file path specified (including subfolders if any).
    4. Script guess each file using seed file (from step1), If Guess fails then It stores the error and continue to guess next file if available. If the guess is successful then it updates all non strings columns (of guessed file) to string data type and store the updated info in new (guessed) file.
    5. Then It create the table in which sftp connector will load the data.
    6. Then It executes the connector create command, If command fails then It stores the error and continue to create next  connector. If the command is successful then it loads the initial data to table (created in step 5).
    7. The script also have the Flag to enable/disable the initial load. Script repeats steps 3 to 6 for each file.
    8. At last, Script list all of all errors for each file in JSON format if any otherwise script will print message like 'Connectors created successfully'.
    9. All Connector Name(s) will be shown in the UI as sftp_YYYYMMDD_HHMMSS. But when one list connectors in CLI then one will be seeing the correct readable names which was specified while creating the connectors (step6).

    Note: All the dynamically created seed files (will have prefix as seed_), guessed files (will have prefix as load_ and load1_) will be using the name of data files. load1_ files are the files which have all fields as STRING.

## Prerequisites
  - Need to install the python packages using below command:
    - pip install -r requirements.txt
  - Create the seed file seed_standard.yml
  - Enter all the SFTP credentials in config_sftp.py

## How to run this
You can run the python file create_sftp_connector.py directly in CLI or in IDE like PyCharm after performing Prerequisites.
- Command to run the code from CLI
  - python create_sftp_connector.py

## Sample Output Logs
Please see the sample logs in log_sample.txt
