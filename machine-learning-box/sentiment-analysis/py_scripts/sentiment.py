import os
import sys


def _upload_model(model, model_file="keras_model.h5"):
    import boto3

    model.save(model_file)

    # Upload the TensorFlow model to S3
    # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    s3 = boto3.resource("s3")
    # ACL should be chosen with your purpose
    s3.Bucket(os.environ["S3_BUCKET"]).upload_file(model_file, model_file)


def run(
    with_aws=True,
    database="sentiment",
    train_table="movie_review_train",
    test_table="movie_review_test",
):
    # Original code is published at official document of TensorFlow under Apache License Version 2.0
    # https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub

    os.system(
        f"{sys.executable} -m pip install -U tensorflow==2.0.0 tensorflow_hub==0.7.0"
    )

    import pytd
    import tensorflow as tf
    import tensorflow_hub as hub
    import numpy as np
    import pandas as pd

    print("fetch data")
    client = pytd.Client(
        database=database,
        apikey=os.environ["TD_API_KEY"],
        endpoint=os.environ["TD_API_SERVER"],
    )

    print("fetch training data")
    train_df = pd.DataFrame(
        **client.query(
            f"""
        select
            rowid, sentence, sentiment, polarity
        from
            {train_table}_shuffled
    """
        )
    )

    print("fetch test data")
    test_df = pd.DataFrame(
        **client.query(
            f"""
        select
            rowid, sentence, sentiment, polarity
        from
            {test_table}_shuffled
    """
        )
    )

    # Shuffle has been done by HiveQL in the shuffle task
    # train_df = train_df.sample(frac=1).reset_index(drop=True)

    print("dowload pretrained model")
    hub_layer = hub.KerasLayer(
        "https://tfhub.dev/google/nnlm-en-dim128/2", input_shape=[], dtype=tf.string
    )
    print("start training")
    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(500, activation="relu"))
    model.add(tf.keras.layers.Dense(100, activation="relu"))
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.summary()

    x_val = train_df["sentence"].iloc[:10000].values
    partial_x_train = train_df["sentence"].iloc[10000:].values

    y_val = train_df["polarity"].iloc[:10000].values
    partial_y_train = train_df["polarity"].iloc[10000:].values
    history = model.fit(
        partial_x_train,
        partial_y_train,
        epochs=40,
        batch_size=512,
        validation_data=(x_val, y_val),
    )

    results = model.evaluate(test_df["sentence"].values, test_df["polarity"].values)
    print(results)

    if with_aws:
        _upload_model(model)

    pred = model.predict(test_df["sentence"].values)
    test_df["predicted_polarity"] = np.where(pred > 0.5, 1, 0)

    client.load_table_from_dataframe(
        test_df[["rowid", "predicted_polarity"]],
        "test_predicted_polarities",
        if_exists="overwrite",
    )


if __name__ == "__main__":
    run()
