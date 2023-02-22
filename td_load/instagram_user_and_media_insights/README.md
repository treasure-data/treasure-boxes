# Workflow: Instagram User and Media Insights

This is example workflow ingests insights, using [Treasure Data's Data Connector for Instagram User and Media Insights](https://docs.treasuredata.com/display/public/INT/Instagram+User+and+Media+Insights+Import+Integration) with [`td_load`](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

## Prerequisites

### daily_load.dig

#### How to Run

First, upload the workflow. `ig_insights` is the project name.

```sh
# Upload
$ td wf push ig_insights
```

Second, set datasource credentials by `td wf secrests` command:

```
# Set Sercrets
$ td wf secrests --project ig_insights --set instagram.access_token
```

Now you can reference this credential by `${secret:}` syntax within yaml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

You can trigger the session manually like:

  ```
  # Run
  $ td wf start ig_insights daily_load --session now
  ```

### daily_load_with_ existing_authentication.dig

#### How to Run

First, you need to create a authetication via TD console. see details -> https://docs.treasuredata.com/display/public/INT/Instagram+User+and+Media+Insights+Import+Integration#InstagramUserandMediaInsightsImportIntegration-UsetheTDConsoletoCreateYourConnection

Then, you can obtain the td autheitcation id from the access URL, as follows

![](screenshot1.png)

Finally, you can write td_authentication_id to daily_load_with_existing_authentication.yaml.

- [config/daily_load_with_existing_authentication.yml](config/daily_load_with_existing_authentication.yml)

And you can run the workflow like the following.

    # Run
    $ td wf start td_load_example daily_load_with_existing_authentication --session now


## Supplemental

### Basic Configuration

Available parameters for Instagram User and Media Insights are here:

| Parameters           | Type    | Description                                                                    |
| -------------------- | ------- | ------------------------------------------------------------------------------ |
| `access_token`       | String  | **Required.** Facebook OAuth access token.                                         |
| `facebook_page_name` | String  | **Required.** Name of Facebook page that are linked to Instagram Business account. |
| `data_type`          | String  | **Required**. Data type to import, available values are `user`, `media`, `media_list`, `comments` and `tags`. |
| `incremental`        | Bool    | Incremental import data. Default: `true`                                       |
| `since`              | String  | Import data since this date. Format: yyyy-MM-dd (inclusive), Default: `null`.  |
| `until`              | String  | Import data until this date. Format: yyyy-MM-dd (exclusive), Default: `null`.  |
| `preset_metric`      | String  | User can select a set of predefined metrics. Default: `null`.                  |
| `metrics`            | List    | List of individual metrics to import. Default: `null`.                         |

### Advance Configuration

Following parameters allows you to control API calls and API versions for Instagram User and Media Insights:


| Parameters                        | Type    | Default | Description                              |
| --------------------------------- | ------- | ------- | ---------------------------------------- |
| `maximum_retries`                 | Integer | 3       | Maximum retry times for each API calls.  |
| `initial_retry_interval_millis`   | Integer | 20000   | Initial wait for first retry.            |
| `maximum_retries_interval_millis` | Integer | 120000  | Maximum amount of of total retry time.   |
| `connec_timeout_in_millis`        | Integer | 30000   | Connection timeout when doing API calls. |
| `idle_timeout_in_millis`          | Integer | 60000   | Time a connection can stay idle in pool. |
| `response_timeout_millis`         | Integer | 30000   | Time to wait for reponse.                |
| `throttle_rate_per_second`        | Integer | 5       | Request rate when received throttle header from Facebook Graph API. |
| `throttle_threshold`              | Integer | 90      | Facebook Graph API header contain percent of requests made on the total limit, this will trigger throttle to kick in. |
| `throttle_wait_in_millis`         | Integer | 3600000 | When Facebook Graph API throttle application. We need to wait before resume API requests. |
| `api_version`                     | String  | v6.0    | Facebook Graph API version.              |

## Next Step

If you have any questions, please contact support@treasure-data.com.