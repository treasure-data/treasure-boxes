import io
import os


class TimeSeriesPredictor(object):
    def __init__(self):
        self.apikey = os.getenv("TD_API_KEY")
        self.endpoint = os.getenv("TD_API_SERVER")

    def _upload_graph(self, model, forecast):
        import boto3
        import matplotlib as mlp

        # Need to plot graph for Prophet
        mlp.use("agg")
        from matplotlib import pyplot as plt

        fig1 = model.plot(forecast)
        fig2 = model.plot_components(forecast)
        predict_fig_data = io.BytesIO()
        component_fig_data = io.BytesIO()
        fig1.savefig(predict_fig_data, format="png")
        fig2.savefig(component_fig_data, format="png")
        predict_fig_data.seek(0)
        component_fig_data.seek(0)

        # Upload figures to S3
        # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
        # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
        s3 = boto3.resource("s3")

        predicted_fig_file = "predicted.png"
        component_fig_file = "component.png"

        # ACL should be chosen with your purpose
        s3.Object(os.environ["S3_BUCKET"], predicted_fig_file).put(
            ACL="public-read", Body=predict_fig_data, ContentType="image/png"
        )
        s3.Object(os.environ["S3_BUCKET"], component_fig_file).put(
            ACL="public-read", Body=component_fig_data, ContentType="image/png"
        )

    def run(
        self,
        database="timeseries",
        source_table="retail_sales",
        target_table="predicted_sales",
        start_date="1993-01-01",
        end_date="2016-05-31",
        period=365,
        with_aws=True,
    ):
        import pytd.pandas_td as td
        from fbprophet import Prophet

        period = int(period)

        con = td.connect(apikey=self.apikey, endpoint=self.endpoint)

        engine = td.create_engine(f"presto:{database}", con=con)

        # Note: Prophet requires `ds` column as date string and `y` column as target value
        df = td.read_td(
            f"""
            select ds, y
            from {source_table}
            where ds between '{start_date}' and '{end_date}'
            """,
            engine,
        )

        model = Prophet(seasonality_mode="multiplicative", mcmc_samples=300)
        model.fit(df)
        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)

        if with_aws:
            self._upload_graph(model, forecast)

        # To avoid TypeError: can't serialize Timestamp, convert `pandas._libs.tslibs.timestamps.Timestamp` to `str`
        forecast.ds = forecast.ds.apply(str)

        # Store prediction results
        td.to_td(
            forecast, "{}.{}".format(database, target_table), con, if_exists="replace"
        )


if __name__ == "__main__":
    TimeSeriesPredictor().run()
