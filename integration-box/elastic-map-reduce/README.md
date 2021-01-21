# Workflow: Simple Python Script, Using EMR

This example workflow allows the user to run a simple python script using Treasure Workflow using the emr operator. 

# Preparation

This example workflow uses [TD-Pandas](https://docs.treasuredata.com/articles/jupyter-pandas) for creating a pandas dataframe from a td-query, and pushing a dataframe back to Treasure Data as a new table.

This example workflow also uses the [EMR-operator](https://docs.digdag.io/operators/emr.html), that creates a new minimal ephemeral cluster with just one node.

This example workflow also uses the [Sample Datasets](https://console.treasuredata.com/app/databases/27777) database in Treasure Data.

# How to Run

For local mode, register your AWS credentials at first

    # Set Secrets for local mode
    $ td wf secrets --local --set aws.emr.access_key_id
    $ td wf secrets --local --set aws.emr.secret_access_key

For server mode, upload the project to Treasure Data, and then register your AWS credentials into the uploaded project.

    # Upload
    $ td wf push td_emr_example
    # Set secrets
    $ td wf secrets --project td_emr_example --set aws.emr.access_key_id
    $ td wf secrets --project td_emr_example --set aws.emr.secret_access_key

Create a sample database for this workflow to push it's job to
	
	# Sample Database. NOTE: this database may already exist if you've run past tutorials.
	$ td db:create workflow_temp

Then, please modify TD_APIKEY in the load.py

Now, you can trigger the session manually.
    
    # Run on Local
    $ td wf run pandas_emr.dig --session now
    # Run on Server
    $ td wf start td_emr_example pandas_emr --session now

# Results

This example workflow will pull the table Nasdaq into a pandas dataframe, average by day, and push the results back to a table nasdaq_daily_average in the database workflow_temp.

# Limitations

- `region` is not supported. Thus EMR boots on us-east-1.
- to_td is Streaming Import, if EMR cluster is down, the data might be lost. And, the import is not so fast.
- For large dataset, upload it to S3, and use DataConnector for S3 would be better. (Ex. Loading 10 million rows might take 3 hours.)
    
# Next Step

If you have any questions, please contact support@treasuredata.com.
