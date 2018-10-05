# Time series analysis with Prophet

***This is an experimental workflow. It doesn't work on production environment yet***

This example introduces time series prediction using [Facebook Prophet](https://facebook.github.io/prophet).

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
