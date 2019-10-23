import os
import sys

os.system(f"{sys.executable} -m pip install -U tensorflow==2.0.0 tensorflow_hub==0.7.0")


def run(input_table="movie_review_test_shuffled", database="sentiment"):
    import boto3
    import pytd
    import tensorflow as tf
    import tensorflow_hub as hub
    import numpy as np
    import pandas as pd

    client = pytd.Client(
        database=database,
        apikey=os.environ["TD_API_KEY"],
        endpoint=os.environ["TD_API_SERVER"],
    )
    print("fetch data")
    query_result = client.query(
        f"""
            select
                rowid, sentence
            from
                {input_table}
        """
    )
    df = pd.DataFrame(**query_result)

    print("load model")
    model_file = "keras_model.h5"

    # Download the TensorFlow model from S3
    # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and
    # "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    s3 = boto3.resource("s3")
    s3.Bucket(os.environ["S3_BUCKET"]).download_file(model_file, model_file)

    print("predict")
    model = tf.keras.models.load_model(
        model_file, custom_objects={"KerasLayer": hub.KerasLayer}
    )
    model.summary()

    result = model.predict(df["sentence"].values)

    print("upload prediction results")
    table = "test_predicted_polarities"
    df["predicted_polarity"] = np.where(result > 0.5, 1, 0)
    client.load_table_from_dataframe(
        df[["rowid", "predicted_polarity"]], table, if_exists="overwrite"
    )
    print("Upload finished")


if __name__ == "__main__":
    run()
