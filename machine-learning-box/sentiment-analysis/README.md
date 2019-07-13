# Sentiment classification with TensorFlow

This example introduces sentiment analysis for movie reviews using [TensorFlow](https://www.tensorflow.org/) and [TensorFlow Hub](https://www.tensorflow.org/hub), or [Chainer](https://chainer.org/).
Original example is written in [the official document](https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub).

This workflow will:

1. Fetch review data from Treasure Data
2. Build a model with TensorFlow
3. Store the model on S3
4. Predict polarities for unknown review data and write back to Treasure Data

Currently, prediction with fetching model from S3 is not evaluated yet.

Note: Before pytd v1.0, pytd depends on td-spark. If your account isn't enabled td-spark, please contact support@treasure-data.com.

## Workflow

There are three workflows:

1. which uploads a trained model to Amazon S3 and prediction results to TD with TensorFlow
2. which uploads prediction results to TD with TensorFlow.
3. which uploads prediction results to TD with pretrained model by using Chainer.

### An example workflow with TensorFlow using Amazon S3

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

### An example workflow with TensorFlow without using Amazon S3

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

### An example workflow with Chainer for prediction

```bash
$ ./data.sh # prepare example data
$ td workflow push sentiment
$ td workflow secrets \
  --project sentiment \
  --set apikey \
  --set endpoint
# Set secrets from STDIN like: apikey=1/xxxxx, endpoint=https://api.treasuredata.com
$ td workflow start sentiment sentiment-analysis-chainer --session now
```

* [sentiment-analysis-chainer.dig](sentiment-analysis-chainer.dig)

Note: Original Chainer example was written in [the chainer repository](https://github.com/chainer/chainer/tree/v6.1.0/examples/text_classification) and we trained the model with CNN + MLP with imdb.binary data. The labels were modified with the original Chainer example as positive=1 and negative=0, which are consistent with TensorFlow example's preprocessing.
