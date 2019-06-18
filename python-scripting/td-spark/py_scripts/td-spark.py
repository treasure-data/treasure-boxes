import os
from typing import Optional

from pyspark.sql import SparkSession
import pyspark.sql.functions as func

TD_SPARK_BASE_URL = "https://s3.amazonaws.com/td-spark/"
TD_SPARK_JAR_NAME = "td-spark-assembly_2.11-1.2.0.jar"


def _download_td_spark(destination: str) -> None:
    from urllib.error import HTTPError
    from urllib.request import urlopen

    download_url = TD_SPARK_BASE_URL + TD_SPARK_JAR_NAME

    try:
        response = urlopen(download_url)
    except HTTPError:
        raise RuntimeError("failed to access to the download URL: " + download_url)

    try:
        with open(destination, "w+b") as f:
            f.write(response.read())
    except Exception:
        os.remove(destination)
        raise

    response.close()


def _prepare_td_spark() -> SparkSession:
    """
    Create SparkSession with local mode setting td-spark specific configurations.

    :return: SparkSession
    """

    td_spark_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), TD_SPARK_JAR_NAME)
    _download_td_spark(td_spark_path)

    apikey = os.getenv("TD_API_KEY")
    endpoint = os.getenv("TD_API_SERVER")

    site = "us"
    if ".co.jp" in endpoint:
        site = "jp"
    elif "eu01" in endpoint:
        site = "eu01"

    os.environ[
        "PYSPARK_SUBMIT_ARGS"
    ] = f"""\
    --jars {td_spark_path}
    --conf spark.td.apikey={apikey}
    --conf spark.td.site={site}
    --conf spark.serializer=org.apache.spark.serializer.KryoSerializer
    --conf spark.sql.execution.arrow.enabled=true
    pyspark-shell
    """

    spark = SparkSession.builder.master("local").appName("spark_sample").getOrCreate()

    return spark


def process_data(database_name: str, table_name: str, spark: Optional[SparkSession] = None) -> None:
    """
    Load a Treasure Data table and upload it to Treasure Data after PySpark processing.

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """
    if spark is None:
        spark = _prepare_td_spark()

    # Read sample_datasets from TD table
    access_df = spark.read.format("com.treasuredata.spark").load("sample_datasets.www_access")

    # Process with PySpark
    processed_df = access_df.filter("method = 'GET'").withColumn("time_str", func.from_unixtime("time"))

    # Upload processed Spark DataFrame to TD
    processed_df.write.mode("overwrite").format("com.treasuredata.spark").option(
        "table", f"{database_name}.{table_name}"
    ).save()


def execute_sql(database_name: str, table_name: str, spark: Optional[SparkSession] = None) -> None:
    """
    Execute SparkSQL

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """

    if spark is None:
        spark = _prepare_td_spark()

    # Prepare temporary view before running SparkSQL
    access_df = spark.read.format("com.treasuredata.spark").load(f"{database_name}.{table_name}")
    access_df.createOrReplaceTempView(table_name)

    # Execute SparkSQL
    summary_df = spark.sql(
        f"""\
    select agent, count(*) cnt
    from {table_name}
    group by 1 order by 2 desc"""
    )
    print(summary_df.toPandas().head(10))


def upload_dataframe(database_name: str, table_name: str, spark: Optional[SparkSession] = None) -> None:
    """
    Create Pandas DataFrame and upload it to Treasure Data

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """

    import numpy as np
    import pandas as pd

    if spark is None:
        spark = _prepare_td_spark()

    df = pd.DataFrame({"c": np.random.binomial(10, 0.5, 10)})
    sdf = spark.createDataFrame(df)
    sdf.write.mode("overwrite").format("com.treasuredata.spark").option("table", f"{database_name}.{table_name}").save()


if __name__ == "__main__":
    _spark = _prepare_td_spark()
    _database_name = "td_spark_example"
    _table_name = "summarized_access"

    process_data(_database_name, _table_name, _spark)
    execute_sql(_database_name, _table_name, _spark)
    upload_dataframe(_database_name, _table_name + "_pandas", _spark)
