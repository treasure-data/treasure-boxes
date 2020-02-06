import xml.etree.ElementTree as xEt
import urllib.request
import urllib.parse
import base64
import os
from datetime import datetime

CNFC_ENDPOINT = os.environ.get("cnfc_endpoint")
CNFC_USER = os.environ.get("cnfc_user")
CNFC_PASSWORD = os.environ.get("cnfc_password")


def call_api(command, params):
    xml = xEt.Element("forcast")
    xml.set("version", "fc6.0.6")
    execute = xEt.SubElement(xml, "execute")
    execute.set("id", "1")
    execute.set("command", command)
    parameter = xEt.SubElement(execute, "parameter")

    if command == "startExport":
        export = xEt.SubElement(parameter, "export")
        log_deliv = xEt.SubElement(export, "log_deliv")
        log_deliv.set("delivid", params["delivid"])
        log_deliv.set("strcode", params["strcode"])
        log_deliv.set("with_usercolumn", "1")
        log_deliv.set("with_insert", "1")
        log_clickcount = xEt.SubElement(export, "log_clickcount")
        log_clickcount.set("delivid", params["delivid"])
        log_clickcount.set("strcode", params["strcode"])
        log_clickcount.set("with_usercolumn", "1")
        log_clickcount.set("with_insert", "1")
    else:
        for key in params:
            parameter.set(key, params[key])

    req_body = "CCC=%E6%84%9B&xml=" + urllib.parse.quote(xEt.tostring(xml))
    basic_user_and_pasword = base64.b64encode(
        f"{CNFC_USER}:{CNFC_PASSWORD}".encode("utf-8")
    )
    request = urllib.request.Request(
        CNFC_ENDPOINT,
        req_body.encode(),
        {
            "User-Agent": "Treasure Data Custom Script",
            "Content_Type": "form-data",
            "Authorization": "Basic " + basic_user_and_pasword.decode("utf-8"),
        },
    )

    with urllib.request.urlopen(request) as res:
        data = res.read()
        root = xEt.fromstring(data)
        return root[0]


def download_log(url):
    basic_user_and_pasword = base64.b64encode(
        f"{CNFC_USER}:{CNFC_PASSWORD}".encode("utf-8")
    )
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Treasure Data Custom Script",
            "Authorization": "Basic " + basic_user_and_pasword.decode("utf-8"),
        },
    )

    with urllib.request.urlopen(request) as res:
        data = res.read().decode("utf-8")
        return data


def format_value(col, val):
    if col == "delivtime":
        res = int(datetime.strptime(val, "%Y%m%d%H%M%S").timestamp())
    else:
        res = val
    return res
