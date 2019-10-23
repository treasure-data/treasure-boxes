# td-spark example

**To enable td-spark to connect to Treasure Data, please contact support@treasuredata.com**

This is PySpark example with td-spark.

How to run:

```bash
$ td wf push td-spark
$ td wf secrets --project td-spark --set td.apikey --set td.apiserver
# Input TD API KEY (1/XXXXXXX) and ENDPOINT (e.g. https://api.treasuredata.com)
$ td wf start td-spark pyspark --session now
```

## Further Readings

- [td-spark Official doc](https://support.treasuredata.com/hc/en-us/articles/360001487167-Apache-Spark-Driver-td-spark-FAQs)
