# Workflow: Simple Python Script, Using EMR

This example workflow allows the user to run a simple python script using Treasure Workflow using the emr operator. 

# Preparation

This example workflow uses [TD-Pandas](https://docs.treasuredata.com/articles/jupyter-pandas) for creating a pandas dataframe from a td-query, and pushing a dataframe back to Treasure Data as a new table.

This example workflow also uses the [EMR-operator](http://docs.digdag.io/operators/emr.html), that creates a new minimal ephemeral cluster with just one node.

This example workflow also uses the [Sample Datasets](https://console.treasuredata.com/app/databases/27777) database in Treasure Data.

# How to Run

First, upload the project to Treasure Data.

    # Upload
    $ td wf push td_emr_example

Create a sample database for this workflow to push it's job to
	
	# Sample Database. NOTE: this database may already exist if you've run past tutorials.
	$ td db:create workflow_temp

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_emr_example simple_emr --session now

# Results

This example workflow will pull the table Nasdaq into a pandas dataframe, average by day, and push the results back to a table nasdaq_daily_average in the database workflow_temp.
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
