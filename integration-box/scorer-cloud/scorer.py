import os
import tarfile
import tempfile

import pandas as pd

import boto3

column_names = [
    "datetime",
    "frame_index",
    "uid",
    "type",
    "confidence",
    "x",
    "y",
    "w",
    "h",
    "attributes",
]


def tsv_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".tsv":
            yield tarinfo


def load_sense_video(database, table, bucket, device_id, date):
    import pytd

    client = pytd.Client(database=database)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
    )
    response = s3.list_objects(
        Bucket=bucket,
        Prefix="AnalyzedData/Rule/future_standard.sensevideo.1.0/{}/{}/texts".format(
            device_id, date
        ),
    )

    if "Contents" not in response:
        print("found no results")
        return

    for c in response["Contents"]:
        key = c["Key"]

        f = tempfile.NamedTemporaryFile(suffix=".tgz")
        s3.download_fileobj(bucket, key, f)

        print("downloaded file: {} -> {}".format(key, f.name))
        try:
            tar = tarfile.open(name=f.name, mode="r:gz")
        except:
            print("-> skipped due to read failure")
            f.close()
            continue
        tsvs = list(tsv_files(tar))
        if len(tsvs) == 0:
            tar.close()
            f.close()
            continue
        tsv = tsvs[0]

        tar.extract(member=tsv)

        print("reading TSV: {}".format(tsv.name))
        df = pd.read_csv(tsv.name, sep="\t", header=None, names=column_names)
        client.load_table_from_dataframe(df, table, writer="spark", if_exists="append")

        os.remove(os.path.abspath(tsv.name))
        tar.close()
        f.close()


if __name__ == "__main__":
    load_sense_video(
        "takuti",
        "sense_video",
        "takuti-scorer-test",
        "LT_92ca49b9-8671-4913-ba77-a3f4453ade4d",
        "2019-08-15",
    )
