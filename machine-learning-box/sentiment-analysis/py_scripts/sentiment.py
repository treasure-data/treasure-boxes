import os
import sys
import tarfile

from tf_utils.common import EXPORT_DIR_BASE


def get_predictions(estimator, input_fn):
    return [x["class_ids"][0] for x in estimator.predict(input_fn=input_fn)]


def _upload_model(embedded_text_feature_column, estimator):
    import boto3
    import tensorflow as tf

    feature_spec = tf.feature_column.make_parse_example_spec(
        [embedded_text_feature_column]
    )
    serving_input_receiver_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(
        feature_spec
    )
    estimator.export_saved_model(EXPORT_DIR_BASE, serving_input_receiver_fn)

    with tarfile.open("tfmodel.tar.gz", "w:gz") as tar:
        tar.add(EXPORT_DIR_BASE, arcname=os.path.basename(EXPORT_DIR_BASE))

    # Upload the TensorFlow model to S3
    # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    s3 = boto3.resource("s3")
    # ACL should be chosen with your purpose
    s3.Bucket(os.environ["S3_BUCKET"]).upload_file("tfmodel.tar.gz", "tfmodel.tar.gz")


def run(
    with_aws=True,
    database="sentiment",
    train_table="movie_review_train",
    test_table="movie_review_test",
):
    # Original code is published at official document of TensorFlow under Apache License Version 2.0
    # https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub

    os.system(f"{sys.executable} -m pip install tensorflow_hub")

    import tensorflow as tf
    import tensorflow_hub as hub
    import pytd.pandas_td as td

    con = td.connect(
        apikey=os.environ["TD_API_KEY"], endpoint=os.environ["TD_API_SERVER"]
    )
    presto = td.create_engine(f"presto:{database}", con=con)

    train_df = td.read_td(
        f"""
        select
            rowid, sentence, sentiment, polarity
        from
            {train_table}_shuffled
    """,
        presto,
    )

    test_df = td.read_td(
        f"""
        select
            rowid, sentence, sentiment, polarity
        from
            {test_table}_shuffled
    """,
        presto,
    )

    # Shuffle has been done by HiveQL in the shuffle task
    # train_df = train_df.sample(frac=1).reset_index(drop=True)

    with tf.Session(graph=tf.Graph()) as sess:
        train_input_fn = tf.estimator.inputs.pandas_input_fn(
            train_df, train_df["polarity"], num_epochs=None, shuffle=True
        )

        embedded_text_feature_column = hub.text_embedding_column(
            key="sentence", module_spec="https://tfhub.dev/google/nnlm-en-dim128/1"
        )

        estimator = tf.estimator.DNNClassifier(
            hidden_units=[500, 100],
            feature_columns=[embedded_text_feature_column],
            n_classes=2,
            optimizer=tf.train.AdamOptimizer(learning_rate=0.003),
        )

        estimator.train(input_fn=train_input_fn, steps=1000)

        # Export TF model to S3
        if with_aws:
            _upload_model(embedded_text_feature_column, estimator)

        predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
            train_df, train_df["polarity"], shuffle=False
        )

        predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
            test_df, test_df["polarity"], shuffle=False
        )

        train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
        test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)
        print("Training set accuracy: {accuracy}".format(**train_eval_result))
        print("Test set accuracy: {accuracy}".format(**test_eval_result))

        results = get_predictions(estimator, predict_test_input_fn)

    # Store prediction results to Treasure Data

    test_df["predicted_polarity"] = results

    td.to_td(
        test_df[["rowid", "predicted_polarity"]],
        f"{database}.test_predicted_polarities",
        con=con,
        if_exists="replace",
        index=False,
    )


if __name__ == "__main__":
    run()
