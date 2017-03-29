# Workflow: td example (Result Output to Salesforce)

This example workflow exports TD job results into Salesforce [Treasure Data's Writing Job Results into Salesforce](https://docs.treasuredata.com/articles/result-into-salesforce) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

Salesforce.com organization and username, password, and security token for API integration
https://docs.treasuredata.com/articles/result-into-salesforce#prerequisites

# Running workflow

### Local Testing
    # Set Secrets on your local for testing
    $ td wf secrets --local --set sfdc.password=******
    $ td wf secrets --local --set sfdc.securitytoken=********
    #Run it locally
    $ td wf run td_sfdc

### Server Testing
    #Push to server
    $ td wf push result_sfdc
    # Set Secrets
    $ td wf secrets --project result_sfdc --set sfdc.password=******
    $ td wf secrets --project result_sfdc --set sfdc.securitytoken=********
    
You can trigger the session manually.

    # Run
    $ td wf start result_sfdc td_sfdc --session now

# Supplemental

Example URL formats of Result Output to Salesforce with different modes:

- sfdc://user%40treasure-data.com:PASSWORDSECURITYTOKEN@login.salesforce.com/Contact              #(default: mode=append)
- sfdc://user%40treasure-data.com:PASSWORDSECURITYTOKEN@login.salesforce.com/Contact?mode=truncate  #truncate mode
- sfdc://user%40treasure-data.com:PASSWORDSECURITYTOKEN@login.salesforce.com/Contact?mode=update&unique=CustomerId__c&upsert=false' #update mode


For more details on Result output to Salesforce, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-salesforce)

# Next Step

If you have any questions, please contact support@treasure-data.com.