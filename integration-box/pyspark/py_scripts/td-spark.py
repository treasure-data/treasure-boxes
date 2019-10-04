import os
from typing import Optional

import pyspark.sql.functions as func
from pyspark.sql import SparkSession
from td_pyspark import TDSparkContext, TDSparkContextBuilder


def _prepare_td_spark() -> TDSparkContext:
    """
    Create SparkSession with local mode setting td-spark specific configurations.

    :return: TDSparkContext
    """

    apikey = os.getenv("TD_API_KEY")
    endpoint = os.getenv("TD_API_SERVER")

    site = "us"
    if ".co.jp" in endpoint:
        site = "jp"
    elif "eu01" in endpoint:
        site = "eu01"

    builder = SparkSession.builder.appName("spark_sample")
    td = (
        TDSparkContextBuilder(builder)
        .apikey(apikey)
        .site(site)
        .jars(TDSparkContextBuilder.default_jar_path())
        .build()
    )

    return td


def process_data(
    database_name: str, table_name: str, td_spark: Optional[TDSparkContext] = None
) -> None:
    """
    Load a Treasure Data table and upload it to Treasure Data after PySpark processing.

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """
    if td_spark is None:
        td_spark = _prepare_td_spark()

    # Read sample_datasets from TD table
    access_df = td_spark.table("sample_datasets.www_access").df()

    # Process with PySpark
    processed_df = access_df.filter("method = 'GET'").withColumn(
        "time_str", func.from_unixtime("time")
    )

    # Upload processed Spark DataFrame to TD
    td_spark.create_database_if_not_exists(database_name)
    td_spark.create_or_replace(processed_df, f"{database_name}.{table_name}")


def execute_sql(
    database_name: str, table_name: str, td_spark: Optional[TDSparkContext] = None
) -> None:
    """
    Execute SparkSQL

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """

    if td_spark is None:
        td_spark = _prepare_td_spark()

    # Prepare temporary view before running SparkSQL
    access_df = td_spark.table(f"{database_name}.{table_name}").df()
    access_df.createOrReplaceTempView(table_name)

    # Execute SparkSQL
    spark = td_spark.spark
    summary_df = spark.sql(
        f"""\
    select agent, count(*) cnt
    from {table_name}
    group by 1 order by 2 desc"""
    )
    print(summary_df.toPandas().head(10))


def upload_dataframe(
    database_name: str, table_name: str, td_spark: Optional[TDSparkContext] = None
) -> None:
    """
    Create Pandas DataFrame and upload it to Treasure Data

    :param database_name: Target database name on Treasure Data
    :param table_name: Target table name on Treasure Data
    :param spark: [Optional] SparkSession
    """

    import numpy as np
    import pandas as pd

    if td_spark is None:
        td_spark = _prepare_td_spark()

    spark = td_spark.spark

    df = pd.DataFrame({"c": np.random.binomial(10, 0.5, 10)})
    sdf = spark.createDataFrame(df)
    td_spark.create_database_if_not_exists(database_name)
    td_spark.create_or_replace(sdf, f"{database_name}.{table_name}")


if __name__ == "__main__":
    _td = _prepare_td_spark()
    _database_name = "td_spark_example"
    _table_name = "summarized_access"

    process_data(_database_name, _table_name, _td)
    execute_sql(_database_name, _table_name, _td)
    upload_dataframe(_database_name, _table_name + "_pandas", _td)
