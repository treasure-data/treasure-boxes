# Amazon Kinesis Import Integration 

This example processes data from a sample similar to Kinesis Firehose data stream and imports into Treasure Data platform.

## Things to know:

1. Lambda handler function is the main method that processes steam events. When that function is invoked, Lambda invokes the handler method. By default, it has the name `lambda_function.lambda_handler`
2. An event object, which is taken as an argument for lambda_handler is a JSON-formatted document.
3. Kinesis Firehose events are base64 encoded and need to be decoded. We also assume the payload comes in JSON form.
4. Below is the sample from firehose stream event in JSON form. And the lambda_function script is set to handle this input type.

```json
{
  "invocationId": "invocationIdExample",
  "deliveryStreamArn": "arn:aws:kinesis:EXAMPLE",
  "region": "us-west-2",
  "records": [
    {
      "recordId": "49546986683135544286507457936321625675700192471156785154",
      "approximateArrivalTimestamp": 1495072949453,
      "data": "eyJmb28iOiAiYmFyIn0="
    }
  ]
}
```
4. If your streaming input event is of different form, the `lambda_handler` function has to be changed accordingly to parse the data. 

## Run

- Copy and paste script in `lambda_function.py` into your handler function.
- Specify target database name, target table name and TD API Key using the `TD_DATABASE`, `TD_TABLE`, `TD_API_KEY` 
environment variables.
- Specify the correct endpoint for the region you are using using the `TD_ENDPOINT` environment variable:
  * Europe: https://eu01.records.in.treasuredata.com
  * US: https://us01.records.in.treasuredata.com
  * Korea: https://ap02.records.in.treasuredata.com
  * Japan: https://ap01.records.in.treasuredata.com