# Sentiment classification with TensorFlow

***This is an experimental workflow. It doesn't work on production environment yet***

This example introduces sentiment analysis for movie reviews using TensorFlow and TensorFlow Hub.
Original example is written in [the official document](https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub).

This workflow will:
1. Fetch review data from Treasure Data
2. Build a model with TensorFlow
3. Store the model on S3
4. Predict polarities for unknown review data and write back to Treasure Data

Currently, prediction with fetching model from S3 is not evaluated yet.

## Workflow
 ```bash
$ ./data.sh # prepare example data
$ td workflow push sentiment
# export TD_API_KEY=1/xxxxx
# export TD_API_SERVER=https://api.treasuredata.com
# export AWS_ACCESS_KEY_ID=AAAAAAAAAA
# export AWS_SECRET_ACCESS_KEY=XXXXXXXXX
$ td workflow secrets \
  --project sentiment \
  --set apikey=$TD_API_KEY \
  --set endpoint=$TD_API_SERVER \
  --set s3_bucket=$S3_BUCKET \
  --set aws_access_key_id=$AWS_ACCESS_KEY_ID \
  --set aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
$ td workflow start sentiment sentiment-analysis --session now
```

* [sentiment-analysis.dig](sentiment-analysis.dig)
