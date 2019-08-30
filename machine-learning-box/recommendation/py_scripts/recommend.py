import os

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from td_pyspark import TDSparkContext, TDSparkContextBuilder


def _prepare_td_spark() -> TDSparkContext:
    """
    Create SparkSession with local mode setting td-spark specific configurations.
    :return: TDSparkContext
    """

    apikey = os.environ["TD_API_KEY"]
    endpoint = os.environ["TD_API_SERVER"]

    site = "us"
    if ".co.jp" in endpoint:
        site = "jp"
    elif "eu01" in endpoint:
        site = "eu01"

    builder = SparkSession.builder.appName("spark_als")
    td = (
        TDSparkContextBuilder(builder)
        .apikey(apikey)
        .site(site)
        .jars(TDSparkContextBuilder.default_jar_path())
        .build()
    )

    return td


def spark_als(
    database: str, source_table: str, target_table: str, item_size: int
) -> None:

    item_size = int(item_size)

    td = _prepare_td_spark()

    ratings = (
        td.table(f"{database}.{source_table}")
        .df()
        .select(["userid", "itemid", "rating"])
    )

    X_train, X_test = ratings.randomSplit([0.8, 0.2])
    als = ALS(
        maxIter=5,
        regParam=0.01,
        seed=43,
        userCol="userid",
        itemCol="itemid",
        ratingCol="rating",
        coldStartStrategy="drop",
    )
    model = als.fit(X_train)

    predictions = model.transform(X_test)
    evaluator = RegressionEvaluator(
        metricName="rmse", labelCol="rating", predictionCol="prediction"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"RMSE: {str(rmse)}")

    user_recs = model.recommendForAllUsers(item_size)
    user_recs.show()
    user_recs_without_ratings = user_recs.select(
        col("userid"), col("recommendations.itemid").alias("recommended_items")
    )
    td.create_or_replace(user_recs_without_ratings, f"{database}.{target_table}")
    print(f"Finish uploading recommended data to {database}.{target_table}")


if __name__ == "__main__":
    spark_als("movielens", "ratings", "recommendation_als")
