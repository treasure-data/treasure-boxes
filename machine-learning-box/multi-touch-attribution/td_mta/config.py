import os
from dataclasses import dataclass

from td_mta.data import data_dir
from td_mta.td_connector import TDConnector


@dataclass
class Config:
    db: str = 'DATABASE NAME'
    table: str = 'INPUT UNION_TABLE NAME from SQL QUERIES WITH AB_RND'
    metrics_table: str = 'MODEL METRICS TABLE NAME'
    shapley_table: str = 'SHAPLEY VALUES TABLE NAME'
    if_exists: str = 'overwrite'
    user_column: str = 'canonical_id'
    time_column: str = 'time'
    action_column: str = 'channels'
    conversion_column: str = 'conversion'
    user_rnd_column: str = 'ab_rnd'
    users_per_tfrecord: int = 10000
    lookback_window_days: int = 3
    positive_tfrecords_dir: str = os.path.join(data_dir, 'positive_tfrecords')
    negative_tfrecords_dir: str = os.path.join(data_dir, 'negative_tfrecords')
    model_dir: str = os.path.join(data_dir, 'model')

    # Model hyper-parameters
    dropout_rate: float = 0.5
    model_width: int = 128

    # Training hyper-parameters
    train_epochs: int = 3
    train_batch_size: int = 100
    validation_batch_size: int = 1000
    validation_fraction: float = 0.1
    shuffle_buffer_size: int = 10000
    downsample_epoch_fraction: float = 0.5

    def __post_init__(self):
        self.action_vocab = TDConnector.distinct(self.db, self.table, self.action_column)
        print(f'Action vocab: {self.action_vocab}')
