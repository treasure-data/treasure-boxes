import json
import os
import sys

os.system(f"{sys.executable} -m pip install -r requirements.txt")

from td_mta.config import Config
from td_mta.parse_and_save_tfrecords import parse_and_save_tfrecords
from td_mta.td_connector import TDConnector
from td_mta.train_model_from_tfrecords import train_model_from_tfrecords
from td_mta.shapley import calculate_shapley


def run(db, table, user_column, time_column, action_column, conversion_column, lookback_window_days):
    config = Config(
                 db=db,
                 table=table,
                 metrics_table='metrics',
                 shapley_table='shapley',
                 user_column=user_column,
                 time_column=time_column,
                 action_column=action_column,
                 conversion_column=conversion_column,
                 lookback_window_days=int(lookback_window_days))

    print(f'==Config:')
    print(json.dumps(config.__dict__, indent=4))
    with open('config.json', 'w') as f:
        f.write(json.dumps(config.__dict__, indent=4))

    count_positive, count_negative = parse_and_save_tfrecords(config)

    metric_df = train_model_from_tfrecords(config=config, count_positive=count_positive, count_negative=count_negative)

    print("==Saving training metrics to TD")
    TDConnector.write(metric_df, db=config.db, table=config.metrics_table, if_exists=config.if_exists)

    print("==Calculating Shapley values")
    shapley_df, channel_shapley_df = calculate_shapley(config)

    print("==Saving Shapley values to TD")
    TDConnector.write(shapley_df, db=config.db, table=config.shapley_table, if_exists=config.if_exists)
    TDConnector.write(channel_shapley_df, db=config.db, table=config.shapley_table + '_channel',
                      if_exists=config.if_exists)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Customer Journey MTA',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config', '-c', metavar='', help='json file with configuration')
    args = parser.parse_args()

    if args.config is not None:
        with open(args.config) as f:
            config = json.load(f)
        print(f"==Read config from {args.config}: {config}")
        config = Config(**config)

    run()
