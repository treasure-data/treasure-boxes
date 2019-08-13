# Email String Validation

----
## Overview

This box provides a sample SQL query that can be used to assess whether or not a given email addresses is likely to be a valid email address. This is accomplished using regex and other Presto string functions.

----
## Implementation
1. Download this folder locally
2. Use [TD Toolbelt](https://support.treasuredata.com/hc/en-us/articles/360001262207-Treasure-Workflow-Quick-Start-using-TD-Toolbelt-in-a-CLI) to upload this folder as a Treasure Workflow project in your Treasure Data account
3. Define the variables listed below to specify what data to process in order to enrich the necessary customer profiles

----
## Reference

In order to run properly, this workflow requires that the user define the following variables:

**database** - the name of the database that contains the email field that should be validated

**table** - the name of the table that contains the email field that should be validated

**column** - the name of the column that contains the email address data that should be validated


### Note
* Please note that this query does not test the mail server to validate if a mailbox actually exists at this address, but rather parses the email address string to see if the email address is properly formed.

----
## Questions

Please feel free to reach out to support@treasure-data.com with any questions you have about using this code to enrich your customer profiles


