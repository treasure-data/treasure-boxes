# Time series analysis with Prophet

***This is an experimental workflow. It doesn't work on production environment yet***

This example introduces time series for sales data prediction using [Facebook Prophet](https://facebook.github.io/prophet).
Details are described in [the official document](https://facebook.github.io/prophet/docs/non-daily_data.html#monthly-data). 

This workflow will:

1. Fetch past sales data from Treasure Data
2. Build a model with Prophet
3. Predict future sales and write back to Treasure Data
4. Upload predicted figures to S3

## Workflow

```bash
$ ./data.sh # prepare example data
$ td workflow push prophet
# export TD_API_KEY=1/xxxxx
# export TD_API_SERVER=https://api.treasuredata.com
# export AWS_ACCESS_KEY_ID=AAAAAAAAAA
# export AWS_SECRET_ACCESS_KEY=XXXXXXXXX
$ td workflow secrets \
  --project prophet \
  --set apikey=$TD_API_KEY \
  --set endpoint=$TD_API_SERVER \
  --set s3_bucket=$S3_BUCKET \
  --set aws_access_key_id=$AWS_ACCESS_KEY_ID \
  --set aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
$ td workflow start prophet predict_sales --session now
```
 
* [predict_sales.dig](predict_sales.dig)
