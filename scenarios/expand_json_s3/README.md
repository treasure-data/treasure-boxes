# Workflow: expand_json example

This example workflow ingests data from datasource with [JSON Lines](http://jsonlines.org/) format using [expand_json filter](https://github.com/civitaspo/embulk-filter-expand_json).

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# File format

Input file needs to be format in JSON Lines. This example assumes the following file as input.

```
{"id": 1, "name":"John Smith", "valid_user":true, "email":{"primary": "foo1@example.com", "secondary": "bar1@example.com"}}
{"id": 2, "name":"Joe Bloggs", "valid_user":false, "email":{"primary": "foo2@example.com", "secondary": "bar2@example.com"}}
```

**Note that each JSON object should be placed in one line.**

# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set s3.region
    $ td wf secrets --project td_load_example --set s3.access_key_id
    $ td wf secrets --project td_load_example --set s3.secret_access_key

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/load.yml](config/load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
