# Need to plot graph for Prophet
import matplotlib as mlp
mlp.use('agg')
from matplotlib import pyplot as plt

import boto3
import pandas_td as td
from fbprophet import Prophet
import os
import io

class TimeSeriesPredictor(object):
    def __init__(self):
        self.apikey = os.getenv("TD_API_KEY")
        self.endpoint = os.getenv("TD_API_SERVER")
        self.dbname = 'timeseries'
        self.source_table = os.getenv("source_table")
        self.target_table = os.getenv("target_table")
        self.start = os.getenv('start_date')
        self.end = os.getenv('end_date')
        self.period = int(os.getenv('period')) or 365

    def run(self):
        con = td.connect(apikey=self.apikey, endpoint=self.endpoint)

        engine = td.create_engine(
            'presto:{}'.format(self.dbname),
            con=con
        )

        df = td.read_td(
            """
            select ds, y
            from {}
            where ds between '{}' and '{}' 
            """.format(self.source_table, self.start, self.end),
            engine
        )

        model = Prophet(seasonality_mode='multiplicative', mcmc_samples=300)
        model.fit(df)
        future = model.make_future_dataframe(periods=self.period)
        forecast = model.predict(future)

        fig1 = model.plot(forecast)
        fig2 = model.plot_components(forecast)
        predict_fig_data = io.BytesIO()
        component_fig_data = io.BytesIO()
        fig1.savefig(predict_fig_data, format='png')
        fig2.savefig(component_fig_data, format='png')
        predict_fig_data.seek(0)
        component_fig_data.seek(0)

        # Upload figures to S3
        # boto3 assuming environment variables "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
        # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
        # client = boto3.client('sts')
        # response = client.assume_role(
        #     RoleArn=os.environ['AWS_IAM_ROLE_ARN'],
        #     RoleSessionName='ml-prediction')
        # session = boto3.Session(
        #     aws_access_key_id=response['Credentials']['AccessKeyId'],
        #     aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        #     aws_session_token=response['Credentials']['SessionToken'])
        # s3 = session.resource('s3')
        #
        # predicted_fig_file = "predicted.png"
        # component_fig_file = "component.png"
        #
        # # ACL should be chosen with your purpose
        # s3.Object(os.environ['S3_BUCKET'], predicted_fig_file).put(
        #     ACL='public-read', Body=predict_fig_data, ContentType='image/png'
        # )
        # s3.Object(os.environ['S3_BUCKET'], component_fig_file).put(
        #     ACL='public-read', Body=component_fig_data, ContentType='image/png'
        # )

        # To avoid TypeError: can't serialize Timestamp, convert `pandas._libs.tslibs.timestamps.Timestamp` to `str`
        forecast.ds = forecast.ds.apply(str)

        # Store prediction results
        td.to_td(forecast, "{}.{}".format(self.dbname, self.target_table), con, if_exists='replace')


if __name__ == '__main__':
    TimeSeriesPredictor().run()
