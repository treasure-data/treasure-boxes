import os
import sys
from logging import INFO, StreamHandler, getLogger
import urllib

import boto3
from botocore.exceptions import ClientError

import digdag

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


def generate_presigned_url(bucket, region_name, s3_path, expires_in):
    """Generate Pre-signed URL for the specific S3 Object
    https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html

    :param bucket: Bucket to upload to
    :param region_name: String region to upload bucket in, e.g., 'us-east-1'
    :param s3_path: File name to upload. Default: "example_file.txt"
    :param expires_in: the expiration period in seconds
    """

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
        region_name=region_name,
    )

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": s3_path},
            ExpiresIn=expires_in,
        )
        expiration_unixtime = url.split("?")[1].split("&")[-1].split("=")[1]

        digdag.env.store(
            {
                "presigned_url": url,
                "expiration_unixtime": expiration_unixtime,
                "encoded_secret_key": urllib.parse.quote(
                    os.environ["S3_SECRET_ACCESS_KEY"]
                ),  # Secret Key needs to be URL encoded
            }
        )

    except ClientError as e:
        logger.error(e)
        sys.exit(os.EX_DATAERR)
