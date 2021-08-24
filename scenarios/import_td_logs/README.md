# Workflow: Import Treasure Data Logs from Data Landing Area
This example shows how you can use workflow to ingest Treasure Data Logs From Data Landing Areas to your Treasure Data account. 

# How to Run
## Requirement
The workflow requires that Data Landing Areas feature is enabled in your Treasure Data account and thne you've got your User ID to access to it.

## Steps
First, edit configurations. You can find the following settings in the `import_td_logs.dig` file.

|  Parameter |  Description  |
| ---- | ---- |
|  api_endpoint  | The endpoint of the Treasure Data API. See this [document]('https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints'). (e.g. https://api.treasuredata.com) |
|  dla_host  | The hostname of the Data Landing Area (e.g. dla1.treasuredata-co.jp)  |
|  user_id  |  Your user_id received from TD when you enabled Data Landing Areas feature |
|  account_id  |  Your TD account_id  |
|  query_logs_table  | The table name where query logs are stored (e.g. query_logs)  |
|  workflow_logs_table  | The table name where workflow logs are stored (e.g. workflow_logs)  |
|  users_table  | The table name where users data are stored (e.g. users)  |

Next, upload the workflow to Treasure Data.

    # Upload
    $ td wf push import_td_logs

Set secrets with your private key that is the rest of public key you gave to TD when you enabled Data Landing Areas feature.

    $ td wf secrets --project import_td_logs --set sftp.dla_secret_key_file=@~/.ssh/id_rsa_dla
    $ td wf secrets --project import_td_logs --set td.apikey

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start import_td_logs import_td_logs --session now

If you have any questions, contact to support@treasuredata.com.
