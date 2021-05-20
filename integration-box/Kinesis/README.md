# Amazon Kinesis Import Integration 

This example processes data from a sample similar to Kinesis data stream and imports into Treasure Data platform

# Things to know:
1. Lambda handler function is the main method that processes steam events. When that function is involed, Lambda invokes the handler method. By deafult, it has the name `lambda_function.lambda_handler`
2. An event object, which is taken as an argument for lambda_handler is a JSON-formatted document that contains data to be processed
3. Below is the sample from firehose stream event in JSON form. And the lambda_function script is set to handle this input type.

```
{
  "invocationId": "invocationIdExample",
  "deliveryStreamArn": "arn:aws:kinesis:EXAMPLE",
  "region": "us-west-2",
  "records": [
    {
      "recordId": "49546986683135544286507457936321625675700192471156785154",
      "approximateArrivalTimestamp": 1495072949453,
      "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4="
    }
  ]
}
```
4. If your streaming input event is of different form, the lambda_handler function has to be changed accordingly to parse the data part of the JSON input.

# Run
- Copy and Paste script in lambda_function.py into your handler function
- Specify target database name, target table name and TD API Key, at td_database, td_table, td_master_key