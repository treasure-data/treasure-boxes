# Workflow: td example (Result Output to MySQL)

This example workflow ingests data using [Treasure Data's Writing Job Results into MySQL Table)](https://docs.treasuredata.com/articles/result-into-mysql) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_mysql

Second, please set destination td account's master apikey by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_mysql --set mysql.host=xyz
    $ td wf secrets --project td_mysql --set mysql.port=3306
    $ td wf secrets --project td_mysql --set mysql.user=abcde
    $ td wf secrets --project td_mysql --set mysql.password=fghijklmn

    # Set Secrets on your local for testing
    $ td wf secrets --local --set mysql.host=xyz
    $ td wf secrets --local --set mysql.port=3306
    $ td wf secrets --local --set mysql.user=abcde
    $ td wf secrets --local --set mysql.password=fghijklmn

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_mysql td_mysql --session now
    
# Supplemental

URL format of Result Output to MySQL is the following.

- mysql://user:password@host:port/database/table?mode=append

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-mysql#four-modes-to-modify-data-appendreplacetruncateupdate)

# Next Step

If you have any questions, please contact support@treasure-data.com.
