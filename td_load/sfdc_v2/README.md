# Workflow: td_load Example (SFDC)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Salesforce](https://docs.treasuredata.com/display/public/INT/Salesforce+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.


# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required/Optional Keys

| Keys     | Description |
| -------- | ----------- |
| username | User name for force.com REST API. |
| password | Password for Force.com REST API. |
| client_id | Client ID for your application. |
| client_secret | Client secret for your application. |
| login_url | Your Login URL for Salesforce. |
| td_authentication_id | see [Reusing the existing Authentication](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2#AmazonS3ImportIntegrationv2-reuseAuthenticationReusingtheexistingAuthentication) |
| target | Target objact name. |
| soql | your custom SObject Query Language. |
| where | your filter condition on SObject. |
| columns | target SObject attributes. |
| retry_initial_wait_sec | Wait seconds for exponential backoff initial value. |
| retry_limit | Try to retry this times. |
| include_deleted_records | Include deleted records or not. If true, it enbles including deleted records in ingested records. |
| use_rest | Always use REST API regardless reasons to ingest data |

# Next Step

If you have any questions, please contact support@treasure-data.com.
