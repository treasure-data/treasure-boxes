# Time series analysis with Prophet

This example introduces time series for sales data prediction using [Facebook Prophet](https://facebook.github.io/prophet).
Details are described in [the official document](https://facebook.github.io/prophet/docs/non-daily_data.html#monthly-data).

This workflow will:

1. Fetch past sales data from Treasure Data
2. Build a model with Prophet
3. Predict future sales and write back to Treasure Data
4. Upload predicted figures to S3

## Workflow

There are two workflow examples:

1. which uploads prediction results to TD as well as uploads predicted graphs to Amazon S3 and sends a notification to Slack
2. which uploads prediction results. This doesn't require S3 and Slack

Note: Before pytd v1.0, pytd depends on td-spark. If your account isn't enabled td-spark, please contact support@treasure-data.com.

### An example working with Amazon S3 and Slack

```bash
$ ./data.sh # prepare example data
$ td workflow push prophet
$ td workflow secrets \
 --project prophet \
  --set apikey \
  --set endpoint \
  --set s3_bucket \
  --set aws_access_key_id \
  --set aws_secret_access_key
# Set secrets from STDIN like: apikey=1/xxxxx, endpoint=https://api.treasuredata.com, s3_bucket=$S3_BUCKET,
#              aws_access_key_id=AAAAAAAAAA, aws_secret_access_key=XXXXXXXXX
$ td workflow start prophet predict_sales --session now
```

* [predict_sales.dig](predict_sales.dig)

### An example working without AWS

```bash
$ ./data.sh # prepare example data
$ td workflow push prophet
$ td workflow secrets \
 --project prophet \
  --set apikey \
  --set endpoint \
# Set secrets from STDIN like: apikey=1/xxxxx, endpoint=https://api.treasuredata.com
$ td workflow start prophet predict_sales_simple --session now
```

* [predict_sales_simple.dig](predict_sales_simple.dig)
