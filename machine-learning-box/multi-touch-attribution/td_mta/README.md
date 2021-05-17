# td-mta

Multi Touch Attribution for Treasure Data

## Getting Started

Requires Python 3.7 or higher. Install requirements:
```shell script
$ pip install -r requirements.txt
```

Running on mock data saved under `mta` db in `mock_data` table:

```shell script
$ python -m td_mta.main
```

The above script is split into 3 separate functions: 
- `save_tfrecords()`: Reads data from TD and saves tfrecords files to a local directory.
- `train_model()`: Trains the MTA model using the tfrecords files and saves it to a local directory.
- `calculate_shapely()`: Loads the MTA model and calculates the shapley values for positive examples.

These functions can be run independently in separate containers as long as they run the same version of configuration and code, and have access to the files saved from previous step. The default mock data in this demo is very small and random so the results and model do not make sense.


## Configuration
All the configurable parameters in `config.py` via a dataclass. The parameters and their default values are:
```python
@dataclass
class Config:
    db: str = 'mta'
    table: str = 'mock_data'
    metrics_table: str = 'metrics'
    shapely_table: str = 'shapley'
    if_exists: str = 'overwrite'
    user_table: str = 'user_rnd'
    user_column: str = 'user_id'
    time_column: str = 'time'
    action_column: str = 'source'
    conversion_column: str = 'conversion'
    user_rnd_column: str = 'ab_rnd'
    users_per_tfrecord: int = 10000
    lookback_window_days: int = 5
    positive_tfrecords_dir: str = os.path.join(data_dir, 'positive_tfrecords')
    negative_tfrecords_dir: str = os.path.join(data_dir, 'negative_tfrecords')
    model_dir: str = os.path.join(data_dir, 'model')
    # Training hyper-parameters
    steps_per_epoch: int = 100
    train_epochs: int = 5
    train_batch_size: int = 1000
    validation_batch_size: int = 1000
    validation_fraction: float = 0.5
    shuffle_buffer_size: int = 100000
    # Network hyper-parameters
    dropout_rate: float = 0.5
    model_width: int = 64
```

To change a parameter you can  initialize the configuration in the `main.py` accordingly. For example to update the lookback window, database, tables names from environment variables change the configuration initialization: `configuration = Config()` in `main.py` to:

```python
    configuration = Config(db=os.environ['DB'],
                           table=os.environ['DATA_TABLE'],
                           lookback_window_days=int(os.environ['LOOKBACK_WINDOW']),
                           positive_tfrecords_dir='/save_dir/positive_tfrecords',
                           negative_tfrecords_dir='/save_dir/negative_tfrecords')
```

## User table
The script assumes the presence of a table that stores mapping of user ids to a random hex. This mapping is used to generate batch queries if the number of users is greater than `users_per_tfrecord` configuration parameter (default is 10000). The name of this table can be specified via `user_table` configuration parameter (default is `usr_rnd`). The sql query to generate this table is:

```
select rand(18) as ab_rnd, {user_id_column}
from  (select distinct {user_id_column} from {table}) as T1
cluster by rand(43)'''
``` 

## Batch queries
The number of users queried in a single batch is controlled by the `users_per_tfrecord` configuration parameter (default is 10000). This number should be tuned according to the available memory. If it is too large, it can cause out of memory error. If it is too low, it would slow down the script. 