# Amazon Kinesis Import Integration 

This example processes data from a sample similar to Kinesis data stream and imports into Treasure Data platform

# Things to know:
1. Lambda handler function is the main method that processes steam events. When that function is involed, Lambda invokes the handler method. By deafult, it has the name `lambda_function.lambda_handler`
2. An event object, which is taken as an argument for lambda_handler is a JSON-formatted document that contains data to be processed
3. `python_import_test.py` is the test script we used to process the sample data below. The data, which is the event object varies depends on the input stream and so the format of the JSON data. So the script has to be changed accordingly.

```
{
            "Records": [
                {"Sans":
                    {
                        "Timestamp": "2019-01-02T12:45:07.000Z",
                        "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r=="
                    }
                }
            ]
}
```

# Run
- Copy and Paste script in lambda_function.py into your handler function
- Specify target database name, target table name and TD API Key, at td_database, td_table, td_master_key