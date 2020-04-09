import requests
import urllib
import base64
import os
from datetime import datetime

CNFC_ENDPOINT = os.environ.get("cnfc_endpoint")
CNFC_USER = os.environ.get("cnfc_user")
CNFC_PASSWORD = os.environ.get("cnfc_password")


def call_api(command, params):
    destination = "{endpoint}{command}?{parameters}".format(
        endpoint = CNFC_ENDPOINT,
        command = command,
        parameters = urllib.parse.urlencode(params)
    )
    basic_user_and_pasword = base64.b64encode(
        f"{CNFC_USER}:{CNFC_PASSWORD}".encode("utf-8")
    )
    response = requests.get(destination, headers={
            "User-Agent": "Treasure Data Custom Script",
            "Authorization": "Basic " + basic_user_and_pasword.decode("utf-8"),
        })
    return response

def format_value(col, val):
    if col == "delivtime":
        res = int(datetime.strptime(val, "%Y%m%d%H%M%S").timestamp())
    else:
        res = val
    return res
