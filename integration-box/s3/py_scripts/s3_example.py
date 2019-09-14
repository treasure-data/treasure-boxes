import os
import sys
from logging import DEBUG, StreamHandler, getLogger

import boto3
from botocore.exceptions import ClientError

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def upload_data(bucket, region_name, file_name="example_file.txt"):
    """Upload a file to an S3 bucket

    :param bucket: Bucket to upload to
    :param region_name: String region to upload bucket in, e.g., 'us-east-1'
    :param file_name: File name to upload. Default: "example_file.txt"
    """

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
        region_name=region_name,
    )

    with open(file_name, "w") as f:
        f.write("This is example text\n")
        f.write("to upload to S3.")

    object_name = file_name
    logger.debug(
        (
            "Start uploading...\n"
            f"  file name: {file_name}\n"
            f"  bucket name: {bucket}\n"
            f"  object name: {object_name}"
        )
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(e)
        sys.exit(os.EX_DATAERR)

    logger.debug("Upload finished")


def download_data(bucket, region_name, object_name="example_file.txt"):
    """Download a file to an S3 bucket

    :param bucket: Bucket to download to
    :param region_name: String region to download bucket in, e.g., 'us-east-1'
    :param object_name: File name to download. Default: "example_file.txt"
    """

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
        region_name=region_name,
    )

    file_name = object_name

    logger.debug("Start downloading")
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logger.error(e)
        sys.exit(os.EX_DATAERR)

    logger.debug("Download finished")

    with open(file_name, "r") as f:
        contents = f.read()

    print(contents)


if __name__ == "__main__":
    upload_data("aki-dev", "us-east-1")
    download_data("aki-dev", "us-east-1")
