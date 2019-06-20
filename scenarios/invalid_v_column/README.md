# Workflow: Scenario (invalid v column)

## What is the purpose of this scenario?
We cannot invalid including v column when we execute `SELECT *` in Hive query by any option of workflow operators.  
However, there is requirement to invalid it in workflow in the case that we recreate the table.  
This example show how to do it by using `http>:` operator to call Treasure Data API.

# How to Run
Firstly, you can upload the project.

    # Upload
    $ td wf push invalid_v_column

Secondaly, please register api key as secrets.

    # Set secrets
    $ td wf secrets --project invalid_v_column --set td.apikey

Now, you can refer to api key as ${secret:td.apikey}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start invalid_v_column wf_invalid_v_column --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
