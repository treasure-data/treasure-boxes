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

There are two workflows:

1. which uploads a trained model to Amazon S3 and prediction results to TD
2. which uploads prediction results to TD.

### An example workflow with Amazon S3

```bash
$ ./data.sh # prepare example data
$ td workflow push sentiment
$ td workflow secrets \
  --project sentiment \
  --set apikey \
  --set endpoint \
  --set s3_bucket \
  --set aws_access_key_id \
  --set aws_secret_access_key
# Set secrets from STDIN like: apikey=1/xxxxx, endpoint=https://api.treasuredata.com, s3_bucket=$S3_BUCKET,
#              aws_access_key_id=AAAAAAAAAA, aws_secret_access_key=XXXXXXXXX
$ td workflow start sentiment sentiment-analysis --session now
```

* [sentiment-analysis.dig](sentiment-analysis.dig)

### An example workflow without Amazon S3

```bash
$ ./data.sh # prepare example data
$ td workflow push sentiment
$ td workflow secrets \
  --project sentiment \
  --set apikey \
  --set endpoint
# Set secrets from STDIN like: apikey=1/xxxxx, endpoint=https://api.treasuredata.com
$ td workflow start sentiment sentiment-analysis-simple --session now
```

* [sentiment-analysis-simple.dig](sentiment-analysis-simple.dig)
