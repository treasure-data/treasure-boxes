# Workflow: td_load Example (Shopify)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Shopify](https://docs.treasuredata.com/display/public/INT/Shopify+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set shopify.apikey
    $ td wf secrets --project td_load_example --set shopify.password
    $ td wf secrets --project td_load_example --set shopify.store_name

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

| Keys       | Description |
| ---------- | ----------- |
| apikey     | Shopify provided API Key. |
| password   | Shopify provided password. |
| store_name | Shopify store name for which data needs to be fetched. |
| target     | Shopify object for which data needs to be fetched from store. `customers`, `orders`, `products` and `transactions` are available. |
| from_date  | Parameter which fetch records from the date specified for specified target Shopify object. |


# Next Step

If you have any questions, please contact support@treasure-data.com.
