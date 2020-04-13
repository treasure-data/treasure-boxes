import cuenote
import json
import pandas
import time
import os
import sys
from datetime import datetime

os.system(f"{sys.executable} -m pip install -U pytd==1.2.0 td-client")
import pytd

TD_API_KEY = os.environ.get("td_apikey")
TD_API_SERVER = os.environ.get("td_endpoint")
TD_DATABASE = os.environ.get("td_database")

jobinfo = {
    "delivery_id": [],
    "adbook_id": [],
    "adbook_name": [],
    "mail_id": [],
    "mail_name": [],
    "refinement": [],
    "fc_status": [],
    "mta_status": [],
    "delivery_time": [],
    "assemble_time": [],
    "first_delivery_end_time": [],
    "delivery_end_time": [],
    "error_count_threshold": [],
    "time_period_starthour": [],
    "time_period_endhour": [],
    "delivery_deadline_hour": [],
    "delivery_velocity": [],
    "is_approval_use": [],
    "exclusion_adbook_id": [],
    "is_nonuniq_aggregation_use": [],
    "nonuniq_aggregation_column": [],
    "nonuniq_aggregation_op": "max",
    "pause_success_percent": [],
    "abtesting_measure_time_hour": [],
    "abtesting_measure_time_min": [],
    "abtesting_measure": [],
    "stat_count": [],
    "stat_success": [],
    "stat_failure": [],
    "stat_deferral": []
}


def main():
    # Create a TD client instance.
    client = pytd.Client(
        apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE
    )

    # Retrieves the details for each job.
    cursor = 0
    keys = jobinfo.keys()
    while cursor is not None:
        result = cuenote.call_api("delivery", {"limit": "50", "cursor": str(cursor)})
        jobs = result.json()
        for job in jobs["list"]:
            for key in keys:
                if key in job:
                    jobinfo[key] += [cuenote.format_value(key, job[key])]
                else:
                    jobinfo[key] += ""
        cursor = jobs["next_cursor"]
    df_jobinfo = pandas.DataFrame(jobinfo.values(), index=jobinfo.keys()).T

    # Refresh Job Info table.
    client.load_table_from_dataframe(
        df_jobinfo, "jobinfo", writer="bulk_import", if_exists="overwrite"
    )
