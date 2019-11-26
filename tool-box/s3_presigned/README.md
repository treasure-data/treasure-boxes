# Share your Query Result using S3

This is a simple example to share the query result with others using Amazon S3 Pre signed URL functionality.

- https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html

## Prerequisites

- Download td cli
- Create an Amazon S3 bucket
- Basic Knowledge of Treasure Workflow's syntax

## How to run this example

You can copy or clone this directory.

After copying the directory, you should variables in `s3.dig` file.

- `bucket`: Destionation S3 Bucket
- `region`: AWS Region name the S3 bucket exists
- `s3_path`: Destination file path
- `expires_in`: The URL lifetime in seconds

Then, push the workflow with `td wf push` command.

```sh
$ td wf push s3_presigned
2019-11-21 14:05:46 +0900: Digdag v0.9.31
Creating .digdag/tmp/archive-8059838056523852496.tar.gz...
  Archiving py_scripts/s3_example.py
  Archiving config/daily_load.yml
  Archiving queries/count.sql
  Archiving README.md
  Archiving mail_body.txt
  Archiving s3.dig
Workflows:
  s3.dig
Uploaded:
  id: 50786
  name: s3_presigned
  revision: b7c407db-7510-4b26-bcbc-db7f0f177d77
  archive type: s3
  project created at: 2018-11-16T01:07:53Z
  revision updated at: 2019-11-21T05:05:51Z

Use `td workflow workflows` to show all workflows.
```

Before running this workflow, we need to set secrets with `td wf secrets` command. Enter AWS access key id and secret access key for the bucket. Input credentials after showing `aws.s3.access_key_id:` and `aws.s3.secret_access_key`.

```sh
$ td wf secrets --project s3_presigned --set s3.access_key_id  --set s3.secret_access_key
2019-09-14 10:11:05 +0900: Digdag v0.9.39
s3.access_key_id:
s3.secret_access_key:
Secret 's3.access_key_id' set
Secret 's3.secret_access_key' set
```

Then, let's start running the example workflow.

```sh
$ td wf start s3_presigned s3 --session now
2019-09-14 10:15:23 +0900: Digdag v0.9.39
Started a session attempt:
  session id: 12623047
  attempt id: 55668803
  uuid: 094b3ba3-7b79-4abb-a529-89e5b67ba711
  project: s3_presigned
  workflow: s3
  session time: 2019-09-14 01:15:24 +0000
  retry attempt name:
  params: {}
  created at: 2019-09-14 10:15:27 +0900

* Use `td workflow session 12623047` to show session status.
* Use `td workflow task 55668803` and `td workflow log 55668803` to show task status and logs.
```

Once this workflow finishes successfully, email like below will be delivered to the specified addresses:

```
You can download the report from:

https://samplebucket.s3.amazonaws.com/output/output.csv?AWSAccessKeyId=AKIAXXXXXXXXXXXXXX&Signature=d5nSbqSd8ZMhi3Pay1RhOv7UOtE%3D&Expires=1574313335

this link expires in 2019-11-21 05:15:35+00:00
```
