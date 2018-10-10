import tarfile
import os
from common import get_export_dir


def run():
    # FIXME: Need to create an image including pandas-td by default
    os.system("pip install pandas-td boto3")

    import boto3
    import tensorflow as tf
    import numpy as np
    import pandas_td as td

    con = td.connect(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])
    presto = td.create_engine('presto:sentiment', con=con)

    test_df = td.read_td("""
        select
            rowid, sentence, sentiment, polarity
        from
            movie_review_test_shuffled
    """, presto)

    examples = []

    for index, row in test_df.iterrows():
        feature = {'sentence': tf.train.Feature(
            bytes_list=tf.train.BytesList(value=[row['sentence'].encode('utf-8')]))}
        example = tf.train.Example(features=tf.train.Features(feature=feature))
        examples.append(example.SerializeToString())

    # Download the TensorFlow model to S3
    # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    s3 = boto3.resource('s3')
    s3.Bucket(os.environ['S3_BUCKET']).download_file('tfmodel.tar.gz', 'tfmodel.tar.gz')

    with tarfile.open('tfmodel.tar.gz') as tar:
        tar.extractall()

    with tf.Session(graph=tf.Graph()) as sess:
        export_dir = get_export_dir()
        predict_fn = tf.contrib.predictor.from_saved_model(export_dir)
        predictions = predict_fn({'inputs': examples})

    test_df['predicted_polarity'] = np.argmax(predictions['scores'], axis=1)
    test_df['score'] = np.max(predictions['scores'], axis=1)

    td.to_td(
        test_df[['rowid', 'predicted_polarity', 'score']], 'sentiment.test_predicted_polarities', con=con,
        if_exists='replace', index=False)


if __name__ == '__main__':
    run()
