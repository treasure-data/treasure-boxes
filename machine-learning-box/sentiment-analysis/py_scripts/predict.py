import csv
import os
import sys
import tarfile
import time

from tf_utils.common import get_export_dir


def run(input_table="movie_review_test", database="sentiment"):
    import boto3
    import tensorflow as tf
    import numpy as np
    import tdclient

    td = tdclient.Client(
        apikey=os.environ["TD_API_KEY"], endpoint=os.environ["TD_API_SERVER"]
    )
    job = td.query(
        database,
        f"""
            select
                rowid, sentence
            from
                {input_table}
        """,
        type="presto",
    )
    job.wait()

    examples = []
    row_ids = []
    for row in job.result():
        rowid, sentence = row
        row_ids.append(rowid)

        feature = {
            "sentence": tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[sentence.encode("utf-8")])
            )
        }
        example = tf.train.Example(features=tf.train.Features(feature=feature))
        examples.append(example.SerializeToString())

    # Download the TensorFlow model to S3
    # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    s3 = boto3.resource("s3")
    s3.Bucket(os.environ["S3_BUCKET"]).download_file("tfmodel.tar.gz", "tfmodel.tar.gz")

    with tarfile.open("tfmodel.tar.gz") as tar:
        tar.extractall()

    with tf.Session(graph=tf.Graph()) as sess:
        export_dir = get_export_dir()
        predict_fn = tf.contrib.predictor.from_saved_model(export_dir)
        predictions = predict_fn({"inputs": examples})

    predicted_polarities = np.argmax(predictions["scores"], axis=1)
    scores = np.max(predictions["scores"], axis=1)

    table = "test_predicted_polarities"
    upload_prediction_result(
        td,
        row_ids,
        predicted_polarities,
        scores,
        database,
        table,
        ["rowid", "predicted_polarity", "score"],
    )


def upload_prediction_result(
    client,
    row_ids,
    predicted_values,
    scores,
    database,
    table,
    fieldnames=["rowid", "predicted_value", "score"],
):

    import tempfile
    import tdclient

    sys.stderr.write(f"Uploading prediction results to {database}.{table}\n")
    # Upload prediction result to TD
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", newline="")
    temp_filename = f.name

    writer = csv.DictWriter(f, fieldnames=["time"] + fieldnames)
    writer.writeheader()
    t = int(time.time())
    for rowid, value, score in zip(row_ids, predicted_values, scores):
        writer.writerow(
            {
                "time": t,
                fieldnames[0]: rowid,
                fieldnames[1]: value,
                fieldnames[2]: score,
            }
        )

    sys.stderr.write(f"Create or recreate table {database}.{table}\n")
    try:
        client.table(database, table)
    except tdclient.errors.NotFoundError:
        pass
    else:
        client.delete_table(database, table)
    client.create_log_table(database, table)
    client.import_file(database, table, "csv", temp_filename)

    f.close()

    # Wait for ingestion until the table will be available
    while True:
        job = client.query(
            database, f"select count(predicted_polarity) from {table}", type="presto"
        )
        job.wait()
        if not job.error():
            break
        time.sleep(10)

    sys.stderr.write("Upload finished")


if __name__ == "__main__":
    run("sentiment")
