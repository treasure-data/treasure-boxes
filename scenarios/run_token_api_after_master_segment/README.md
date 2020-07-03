# Workflow: Run Token workflow after master segment workflow

## What is the purpose of this scenario?

There is a scenario which you want to kick certain workflow after the master segments finishes.
This workflow checks if there is running master segment workflow or not. After finishing the master segment workflow, it will start Profile API refresh workflow.
 

## Regarding api_host
"api_host" in get_wf_running_status.dig is up to your account's site.  
You have to change it if your account's site is located in EU or Tokyo.

Please refer to the doc for more details.  
[https://support.treasuredata.com/hc/en-us/articles/360001474288-Sites-and-Endpoints](https://support.treasuredata.com/hc/en-us/articles/360001474288-Sites-and-Endpoints)

# How to Run
First, upload the project.

    # Upload
    $ td wf push get_wf_running_status

Second, register the api key as a workflow secret.

    # Set secrets
    $ td wf secrets --project get_wf_running_status --set td.apikey

Now, you can refer to api key as ${secret:td.apikey}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start get_wf_running_status get_wf_running_status --session now

# Next Step

If you have any questions, please contact [support@treasure-data.com](support@treasure-data.com).