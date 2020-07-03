import cuenote
import pandas
import time
import os
import sys

os.system(f"{sys.executable} -m pip install -U pytd==1.2.0 td-client")
import pytd

TD_API_KEY = os.environ.get("td_apikey")
TD_API_SERVER = os.environ.get("td_endpoint")
TD_DATABASE = os.environ.get("td_database")

limit = 1000

jobinfo = {
    "adbook": [],
    "adbookname": [],
    "adbookusers": [],
    "allowerror": [],
    "approve": [],
    "delivid": [],
    "delivtime": [],
    "docomo": [],
    "endhour": [],
    "exclusion": [],
    "mailid": [],
    "mailtype": [],
    "maxconn": [],
    "newconn": [],
    "nonuniq_aggregation": [],
    "nonuniq_aggregation_column": [],
    "nonuniq_aggregation_op": [],
    "recvlimit": [],
    "retryinterval": [],
    "retrylimit": [],
    "sendlimit": [],
    "sendnumber": [],
    "smime": [],
    "starthour": [],
    "status": [],
    "subject": [],
}


def main():
    # Create a TD client instance.
    client = pytd.Client(
        apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE
    )

    # Retrieves the details for each job.
    cnt = limit
    page = 1
    while cnt == limit:
        cnt = 0
        for delivery in cuenote.call_api(
            "getDelivList", {"limit": str(limit), "page": str(page)}
        ).iter("deliv_jobqueue"):
            keys = jobinfo.keys()
            for info_items in cuenote.call_api(
                "getDelivInfo", {"delivid": delivery.attrib["delivid"]}
            ).iter("jobinfo"):
                for key in keys:
                    jobinfo[key] += [cuenote.format_value(key, info_items.attrib[key])]
            cnt += 1
        page += 1
    df_jobinfo = pandas.DataFrame(jobinfo.values(), index=jobinfo.keys()).T

    # Request CN to generate logs for each delivery.
    expids = {"expid": []}
    for i in range(len(jobinfo["delivid"])):
        if jobinfo["delivtime"][i] >= (int(time.time()) - (60 * 60 * 24 * 14)):
            for expid in cuenote.call_api(
                "startExport", {"delivid": jobinfo["delivid"][i], "strcode": "utf8"}
            ).iter("expid"):
                expids["expid"] += [int(expid.text)]
    df_expids = pandas.DataFrame(expids.values(), index=expids.keys()).T

    # Refresh Job Info table.
    client.load_table_from_dataframe(
        df_jobinfo, "jobinfo", writer="bulk_import", if_exists="overwrite"
    )

    # Insert expids into the queue table.
    if expids["expid"]:
        client.load_table_from_dataframe(
            df_expids, "queue", writer="bulk_import", if_exists="overwrite"
        )
