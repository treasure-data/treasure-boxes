# S3 upload/download example for Python

This is a simple example integration to upload/download a data from Python Custom Scripting with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

Ensure to create S3 bucket your own, and your S3 bucket has appropriate policy to upload/download from Python Custom Scripting. See also https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html

To set credentials securely, we recommend to use secrets for Treasure Workflow. See also https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management

## Prerequisites

- Download td cli
- Create an Amazon S3 bucket
- Basic Knowledge of Treasure Workflow's syntax

## How to run this example

You can copy or clone this directory.

After copying the directory, you should modify `bucket` and `region` in the [s3.dig](s3.dig) file.

Then, push the workflow with `td wf` command.

```sh
$ td wf push s3
2019-09-14 10:10:40 +0900: Digdag v0.9.39
Creating /Users/ariga/src/workflow-examples/integration-box/s3/.digdag/tmp/archive-3664291240571650731.tar.gz...
  Archiving py_scripts/s3_example.py
  Archiving example_file.txt
  Archiving s3.dig
Workflows:
  s3.dig
Uploaded:
  id: 144643
  name: s3
  revision: 194b860e-0b19-46c2-927a-f337523cc91a
  archive type: s3
  project created at: 2019-09-14T01:10:45Z
  revision updated at: 2019-09-14T01:10:45Z

Use `td workflow workflows` to show all workflows.
```

Before running this workflow, we need to set secrets with `td wf secrets` command. Enter AWS access key id and secret access key for the bucket. Input credentials after showing `aws.s3.access_key_id:` and `aws.s3.secret_access_key`.

```sh
$ td wf secrets --project s3 --set s3.access_key_id  --set s3.secret_access_key
2019-09-14 10:11:05 +0900: Digdag v0.9.39
s3.access_key_id:
s3.secret_access_key:
Secret 's3.access_key_id' set
Secret 's3.secret_access_key' set
```

Then, let's start running the example workflow.

```sh
$  td wf start s3 s3 --session now
2019-09-14 10:15:23 +0900: Digdag v0.9.39
Started a session attempt:
  session id: 12623047
  attempt id: 55668803
  uuid: 094b3ba3-7b79-4abb-a529-89e5b67ba711
  project: s3
  workflow: s3
  session time: 2019-09-14 01:15:24 +0000
  retry attempt name:
  params: {}
  created at: 2019-09-14 10:15:27 +0900

* Use `td workflow session 12623047` to show session status.
* Use `td workflow task 55668803` and `td workflow log 55668803` to show task status and logs.
```

You can see your workflow result in the console. Alternatively, you can see them via `td wf log/task/session` commands as shown in the execution log of `td wf start`.

```sh
td workflow log 55668803
2019-09-14 10:47:13 +0900: Digdag v0.9.39
2019-09-14 01:15:30.378 +0000 [INFO] (0166@[1:s3]+s3+upload) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.upload_data
...snip...
2019-09-14 01:17:13.678 +0000 [INFO] (0279@[1:s3]+s3+upload) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.upload_data
.digdag/tmp/digdag-py-142517842-474732747026709309/runner.py:4: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
Start uploading...
  file name: example_file.txt
  bucket name: aki-dev
  object name: example_file.txt
Upload finished
tar: .digdag/tmp: file changed as we read it
2019-09-14 01:17:22.022 +0000 [INFO] (0177@[1:s3]+s3+upload) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.upload_data
...snip...
2019-09-14 01:19:14.685 +0000 [INFO] (0137@[1:s3]+s3+download) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.download_data
.digdag/tmp/digdag-py-142517843-1217800761999370093/runner.py:4: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
Start downloading
Download finished
This is example text
to upload to S3.
tar: .digdag/tmp: file changed as we read it
2019-09-14 01:19:22.603 +0000 [INFO] (0287@[1:s3]+s3+download) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.download_data
2019-09-14 01:19:28.421 +0000 [INFO] (0192@[1:s3]+s3+download) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.download_data
2019-09-14 01:19:35.455 +0000 [INFO] (0216@[1:s3]+s3+download) io.digdag.core.agent.OperatorManager: py>: py_scripts.s3_example.download_data
```
