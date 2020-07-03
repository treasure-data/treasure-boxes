import cuenote
import pandas
import io
import os
import sys

os.system(f"{sys.executable} -m pip install -U pytd==1.2.0 td-client")
import pytd

TD_API_KEY = os.environ.get("td_apikey")
TD_API_SERVER = os.environ.get("td_endpoint")
TD_DATABASE = os.environ.get("td_database")


def main():
    # Create a TD client instance.
    client = pytd.Client(
        apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE
    )

    # Download log files from Cuenote, then upload CSVs to TD
    expids = client.query("SELECT expid FROM queue")
    for expid in expids["data"]:
        for export in cuenote.call_api(
            "getExportStatus", {"expid": str(expid[0])}
        ).iter("export"):
            for item in export:
                csv = cuenote.download_log(item.attrib["url"])
                df = pandas.read_csv(io.StringIO(csv), header=0, encoding="UTF-8")
                df["delivid"] = item.attrib["delivid"]

                if item.tag == "log_clickcount":
                    df.columns = [
                        "clicked_at",
                        "clicked_url",
                        "email_address",
                        "click_count",
                        "member_id",
                        "delivid",
                    ]
                    df["clicked_at"] = pandas.to_datetime(df["clicked_at"])

                elif item.tag == "log_deliv":
                    df.columns = [
                        "email_address_id",
                        "email_address",
                        "status_updated_at",
                        "status_loc",
                        "status",
                        "mx_host_name",
                        "connection_ip_port",
                        "smtp_status_updated_at",
                        "smtp_status_loc",
                        "smtp_status",
                        "smtp_response",
                        "bounce_received_at",
                        "bounce_type",
                        "bounce_summary",
                        "bounce_content",
                        "bounce_address",
                        "bounce_log_id",
                        "unreachable_at",
                        "all_retries",
                        "first_retry",
                        "last_retry",
                        "retry_count",
                        "last_retry_status_loc",
                        "last_retry_status",
                        "last_retry_response",
                        "member_id",
                        "delivid",
                    ]
                    df["status_updated_at"] = pandas.to_datetime(
                        df["status_updated_at"]
                    )
                    df["smtp_status_updated_at"] = pandas.to_datetime(
                        df["smtp_status_updated_at"]
                    )
                    df["bounce_received_at"] = pandas.to_datetime(
                        df["bounce_received_at"]
                    )
                    df["unreachable_at"] = pandas.to_datetime(df["unreachable_at"])

                if len(df) > 0:
                    client.load_table_from_dataframe(
                        df, item.tag + "_stg", writer="bulk_import", if_exists="append"
                    )
            client.query("DELETE FROM queue WHERE expid = {0}".format(expid[0]))
