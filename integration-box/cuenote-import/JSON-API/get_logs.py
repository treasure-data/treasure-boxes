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

days_refresh_logs = 14


def main():
    # Create a TD client instance.
    client = pytd.Client(
        apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE
    )

    # Download log files from Cuenote, then upload CSVs to TD
    delivery_ids = client.query(
        "select delivery_id from jobinfo where TD_INTERVAL(TD_TIME_PARSE(delivery_time), '-{days_refresh_logs}d')".format(days_refresh_logs=days_refresh_logs))
    for delivery_id in delivery_ids["data"]:

        # Delivery Log
        result = cuenote.call_api(
            "delivery/{delivery_id}/log".format(delivery_id=delivery_id[0]), {"with_delivlog": "true"})
        df = pandas.read_csv(io.BytesIO(result.content),
                                header=0, encoding="UTF-8")
        df["delivery_id"] = delivery_id[0]
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
            "device",
            "content",
            "additional_information",
            "delivery_id"
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
                df, "log_deliv_stg", writer="bulk_import", if_exists="append"
            )

        # Click Log
        result = cuenote.call_api("delivery/{delivery_id}/log/click".format(
            delivery_id=delivery_id[0]), {"with_delivlog": "true"})
        df = pandas.read_csv(io.BytesIO(result.content),
                                header=0, encoding="UTF-8")
        df["delivery_id"] = delivery_id[0]
        df.columns = [
            "clicked_at",
            "clicked_url",
            "email_address",
            "type",
            "click_count",
            "device",
            "content",
            "additional_information",
            "delivery_id"
        ]
        df["clicked_at"] = pandas.to_datetime(df["clicked_at"])
        if len(df) > 0:
            client.load_table_from_dataframe(
                df, "log_clickcount_stg", writer="bulk_import", if_exists="append"
            )
