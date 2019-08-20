import sys

import pandas as pd
import pytd

from pedestrian_detector import PedestrianDetector

# TODO: fill the following env vars
TD_DATABASE = ""
TD_TABLE = ""
TD_API_KEY = ""
TD_API_SERVER = "https://api.treasuredata.com"


if __name__ == "__main__":
    client = pytd.Client(
        database=TD_DATABASE, apikey=TD_API_KEY, endpoint=TD_API_SERVER
    )
    detector = PedestrianDetector()

    counts, timestamps = [], []
    try:
        while True:
            cnt, ts = detector.detect()
            print(cnt, ts)
            counts.append(cnt)
            timestamps.append(ts)
            if len(counts) == 10:
                client.load_table_from_dataframe(
                    pd.DataFrame(data={"time": timestamps, "num_pedestrian": counts}),
                    TD_TABLE,
                    writer="insert_into",
                    if_exists="append",
                )
                counts, timestamps = [], []
    except Exception as e:
        if len(counts) != 0:
            client.load_table_from_dataframe(
                pd.DataFrame(data={"time": timestamps, "num_pedestrian": counts}),
                TD_TABLE,
                writer="insert_into",
                if_exists="append",
            )
            sys.exist("Stopped: {}".format(e))
