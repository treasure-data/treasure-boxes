import sys
import json
from os import system
from os import environ

system(f"{sys.executable} -m pip install -U --user pytd")

import requests


class DataRobotPredictionError(Exception):
    """Raised if there are issues getting predictions from DataRobot"""


def make_datarobot_deployment_predictions(data, deployment_id):
    """
    Make predictions on data provided using DataRobot deployment_id provided.
    See docs for details:
         https://app.datarobot.com/docs-jp/users-guide/deploy/api/new-prediction-api.html

    Parameters
    ----------
    data : str
        [{"Feature1":numeric_value,"Feature2":"string"}]
    deployment_id : str
        The ID of the deployment to make predictions with.

    Returns
    -------
    Response schema:
        https://app.datarobot.com/docs-jp/users-guide/deploy/api/new-prediction-api.html#response-schema

    Raises
    ------
    DataRobotPredictionError if there are issues getting predictions from DataRobot
    """
    DR_USERNAME = environ["DR_USERNAME"]
    DR_PRED_HOST = environ["DR_PRED_HOST"]
    DR_CLOUD_KEY = environ.get("DR_CLOUD_KEY", None)
    DR_API_KEY = environ["DR_API_KEY"]

    # Set HTTP headers. The charset should match the contents of the file.
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    if DR_CLOUD_KEY is not None:
        headers["datarobot-key"] = DR_CLOUD_KEY

    url = (
        "https://{prediction_host}/predApi/v1.0/deployments/{deployment_id}/"
        "predictions".format(prediction_host=DR_PRED_HOST, deployment_id=deployment_id)
    )
    # Make API request for predictions
    predictions_response = requests.post(
        url, auth=(DR_USERNAME, DR_API_KEY), data=data, headers=headers
    )
    _raise_dataroboterror_for_status(predictions_response)
    # Return a Python dict following the schema in the documentation
    return predictions_response.json()


def _raise_dataroboterror_for_status(response):
    """Raise DataRobotPredictionError if the request fails along with the response returned"""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        err_msg = "{code} Error: {msg}".format(
            code=response.status_code, msg=response.text
        )
        raise DataRobotPredictionError(err_msg)


def td_query(sql, connection):
    cur = connection.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    data = [dict(zip(columns, row)) for row in rows]
    return data


def main(sql, database, table, target, deployment_id):
    # SetUp
    from pytd import Client
    from pytd.dbapi import connect
    import pandas as pd

    tdcli = Client(database=database)
    tdcon = connect(tdcli)

    record = td_query(sql, tdcon)
    try:
        # Predict
        predictions = make_datarobot_deployment_predictions(
            json.dumps(record), deployment_id
        )
    except DataRobotPredictionError as exc:
        print(exc)

    for pred in predictions["data"]:
        record[pred["rowId"]][target] = pred["prediction"]

    # Upload
    df = pd.DataFrame(record)
    tdcli.load_table_from_dataframe(
        df, "{}.{}".format(database, table), writer="insert_into", if_exists="overwrite"
    )
    tdcon.close()
    print("{} records processed".format(len(df.index)))
