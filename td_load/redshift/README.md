# Workflow: td_load Example (Amazon Redshift)

This example workflow ingests data in daily basis, using [Amazon Redshift Import Integration
](https://docs.treasuredata.com/display/public/INT/Amazon+Redshift+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required/Optional Keys
## Authentication
| Keys     | Required | Description |
| -------- | ----------- | ----------- |
| host | Y | database host name. (string) |
| port | Y | database port number. (integer, default: 5439)|
| user | Y | database login user name. (stirng)|
| ssl | N | enables SSL. Data will be encrypted but CA or certification will not be verified (boolean, default: false) |
| connect_timeout | N | timeout for establishment of a database connection. (integer (seconds), default: 300) |
| socket_timeout | N | timeout for socket read operations. 0 means no timeout. (integer (seconds), default: 1800) |
| fetch_rows | N | number of rows to fetch one time (used for java.sql.Statement#setFetchSize) (integer, default: 10000) |
| options | N | extra JDBC properties. (has, default: []) |

Or, you can specify authentication info using td_authentication_id option.([Reusing the existing Authentication](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2#AmazonS3ImportIntegrationv2-reuseAuthenticationReusingtheexistingAuthentication))

## Load Settings
| Keys | Required | Description |
| -------- | ----------- | ----------- |
| database | Y | destination database name (string) |
| schema | Y | destination schema name (string, default: "public") |
| query | N | If you write SQL directly, SQL to run (string) |
| table | N | If query is not set, destination table name (string) | 
| select | N | If query is not set, expression of select (e.g. id, created_at) (string, default: "*")|
| where | N | If query is not set, WHERE condition to filter the rows (string, default: no-condition) |
| order_by | N | If query is not set, expression of ORDER BY to sort rows (e.g. created_at DESC, id ASC) (string, default: not sorted) |
| default_timezone | N | If the sql type of a column is date/time/datetime and the Source type is string, column values are formatted int this default_timezone. You can overwrite timezone for each columns using column_options option. (string, default: UTC) |
| after_select | N | if set, this SQL will be executed after the SELECT query in the same transaction. (string)|
| column_options | N | advanced: key-value pairs where key is a column name and value is options for the column. (array, see the following details)| 

Each element of column_options have the following options.

| key | Required | Descritpion |
| -------- | ----------- | ----------- |
| value_type | Y | the Source get values from database as this value_type. Typically, the value_type determines getXXX method of java.sql.PreparedStatement. (string, default: depends on the sql type of the column. Available values options are: long, double, float, decimal, boolean, string, json, date, time, timestamp) |
| type | Y | Column values are converted to this Source type. Available values options are: boolean, long, double, string, json, timestamp. By default, the td_load operator type is determined according to the sql type of the column (or value_type if specified). |
| timestamp_format | N | If the sql type of the column (value_type) is date/time/datetime and the Source type (type) is string, column values are formatted by this timestamp_format. And if the Source type (type) is timestamp, this timestamp_format may be used in the output plugin. For example, stdout plugin use the timestamp_format, but csv formatter plugin doesn't use. (string, default : %Y-%m-%d for date, %H:%M:%S for time, %Y-%m-%d %H:%M:%S for timestamp) |
| timezone | N | If the sql type of the column is date/time/datetime and the Source type is string, column values are formatted in this timezone. (string, value of default_timezone option is used by default) |

# Next Step

If you have any questions, please contact support@treasure-data.com.
