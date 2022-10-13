# Workflow: td_load Example (Amazon S3)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Amazon S3 v2](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The v2 integration has enhanced security features and requested features including a new authentication method, SSE-KMS support, and quote policy.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

## Content

This directory has 2 types of workflows. These are different from authentication method.

One uses a secret key, which is the authentication method until now.
The other uses [AssumeRole (AWS documentation)](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html).

S3 v2 intoroduced a newly authentication method with AssumeRole. If you want use the method, you need to use v2 integration instead of v1.
