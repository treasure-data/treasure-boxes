This document focuses on how to execute the SQL functions of the current workflow inside TD. For more details on configuring the Python model and its hyper-parameters, refer to [`td_mta/README.md`](../td_mta/README.md).

## What data will you need for building this model?

Any table in CDP that tracks historical touchpoints of users engaging with the client brand/content, which can point to marketing channels, sources, or campaigns (can be both digital and physical) that the user was exposed to during their journey to conversion. 

In order to model **Multi-Touch Attribution** (MTA), you need to define which touchpoints count as conversion events in the data. See a sample schema of an input table below:

| `time`  | `user_id`  | `channel` | `source`   | `conversion` |
|:-----:|:--------:|:-------:|:--------:|:----------:|
| 14563 | GhY5Q3   | Direct  | organic  |     0      |
| 56412 | Hu7YYh   | Social  | facebook |     0      |
| 16788 | Yu90G3   | Email   | SFMC     |     1      |

This table is often created by using SQL code to parse and join multiple user-activity tables together, which could be a combination of both digital and physical touchpoints, depending on what marketing campaigns the client is actively running, and whether that data is available in the CDP. More concretely, to meet your use cases and business rules, the queries need to properly extract `utm_source`, `utm_medium`, and channel parameters along with defining conversion events.

## How to configure the Python model

The workflow template reads some of the basic configurations from [`config/params.yml`](../config/params.yml) and dynamically passes the parameters to [`td_mta/config.py`](../td_mta/config.py) that Python scripts eventually load for running machine learning operations.

See more details below:

```python
db: str = 'DATABASE NAME'  # name of database where model will read and write data to.
table: str = 'INPUT TABLE'  # enter name of the final touchpoints union_table with ab_rnd attribute created by the SQL Query `queries/union_ab_rand.sql`
metrics_table: str = 'MODEL METRICS'  # this will be the name of the table that the model will write to TD with LSTM performance metrics such as RMSE and LogLoss. 
shapley_table: str = 'SHAPLEY VALUES'  # this will be the name of the table with the final shapley values, broken down by each day of the customer journey. Note***Aggregate final shapley values across the full journey are output in a separate table that has the same name as shapley_table but with a "_channel" prefix at the end. 
if_exists: str = 'overwrite'  # this can overwrite metrics and shapley values table after each new run. If you prefer to preserve old values and just append new values, then change the parameter to 'append'.
user_column: str = 'canonical_id'  # this points to the column that contains unique user IDs, most commonly 'canonical_id' since this is typically the output of our ID unification algorithm.
time_column: str = 'time'  # name of the column that contains timestamp for each touchpoint.
action_column: str = 'channels'  # this tells LSTM model to use that column as the categorical features when predicting probabilities of conversion. In other words - this is the column that you are trying to get the final shapely values for. Other columns that can be used here are 'source', 'channel_source', 'campaign', depending on what the marketing team wants to measure.
conversion_column: str = 'conversion'  # name of the column that marks conversion events
user_rnd_column: str = 'ab_rnd'  # name of rand digit attribute for random shuffling
users_per_tfrecord: int = 20000  # this is how many unique users will be sabed in each individual TensorFlow record. Rule of thumb is to try get about 2-3% of users per record, so if you have a table with 1M users, then you can make this number 40,000, which will draw from the dataset 25 times with random shuffling to create separate TensorFlow records.
lookback_window_days: int = 3  # this is the lookback window you want to set before the model starts to define how many days from conversion events do you want to track back to define what marketing touchpoints were part of the user journey. 
positive_tfrecords_dir: str = os.path.join(data_dir, 'positive_tfrecords')  # no need to change this, it just tells the model to store TF records in the current project directory.
negative_tfrecords_dir: str = os.path.join(data_dir, 'negative_tfrecords')  # no need to change this, it just tells the model to store TF records in the current project directory.
downsample_epoch_fraction:  int =  0.5  # each epoch uses a randomly subsampled fraction of all the training data, but it's a different fraction every epoch. This will reduce the training time, but will not reduce the Shapley value calculation time.

model_dir: str = os.path.join(data_dir, 'model')  # no need to change this

# Model hyper-parameters
dropout_rate: float = 0.5  # regularization metric for LSTM models aimed at reducing overfitting and improving model performance. Historically, dropout rate values between 0.4 and 0.6 have proven to be the preferred for a variety of LSTM models and hidden layers. 
model_width: int = 128  # means we're using 128th dimensional vectors for the linear transformations of Neural Network layers. 128x128 matrices are used. 

# Training hyper-parameters
train_epochs: int = 3  # how many epochs you want the LSTM to run. Note that for very large datasets a single epoch can take more than 5hrs, so it is advisable to keep that number small at first and increase as you see fit. Typically, you want to watch how val_loss and val_rmse change with each epoch and stop at the epoch after which val_loss stops decreasing.
train_batch_size: int = 1000  # how many samples go in each training batch. The larger this number, the faster each epoch will run, but this might have a slight negative effect on performance.  It's recommended testing different variations and finding good balance between run speed and model performance. 
validation_batch_size: int = 10000  # same rules apply as train_batch size, except you always want your validation batch size 10x or so larger than train_batch, since training has been done at this point and we're only using the validation dataset at the end to estimate val metrics.
validation_fraction: float = 0.10  # decides what fraction of the total data you will hold-out for validation and how many records will go into the model training. We recommend 10% as the default metric, but other fractions can be tested if needed.
shuffle_buffer_size: int = 10000  # not very important since we are already doing random shuffling in the beginning during TF record random sampling. 
```

You technically don't need to change any of the code in any of the other project files, as the code has been tested and optimized multiple times by a full team of Data Scientists. However, if your own team wants to inspect the code and try to tweak different things, then contact your Customer Success Representative and we will be happy to provide more detailed technical documentation.

## How to set up the Python Custom Scripting execution

The final task of the sample workflow below instantiates a temporal Python execution environment in TD. 

```yaml
+execute_python_code:
  docker:
    image: "digdag/digdag-python:3.7"
  py>: td_mta.docker_main.run
  # ...
```

The important syntax here is that the notation `td_mta.docker_main.run` after the `py>` operator tells workflow to look at the `td_mta` project folder, find the `docker_main.py` file and execute the `run()` function inside that file. This is where the full Python code for the Deep Learning LSTM Shapely Values model is executed.

It is also important to copy your Master API Key from your TD account and create a `secret` in the workflow called `td.apikey`, where you can paste the API Key to keep it safe. That secret is then interpreted as an environmental variable `TD_API_KEY`, which is needed by the Python code to read and write data to TD.

## What to do if Workflow returns ERROR because of reaching its max limit capacity?

Depending on a tier your contract determines, the `py>` tasks have a memory limit of 8 or 30GB and 1 or 4 virtual CPUs (not GPUs), which might result in an error if we attempt to run the model on a very large volume of data. 

In our experiment, the model ran successfully with the larger tier on 20M rows of data and 2 epochs, which took about 10-12 hours. However, when attempting on 30M rows of data and 5 epochs, the model took over 24 hours to run, which caused TD to automatically kill the Workflow; TD Workflow has a 24-hour limit per single process, so any model configuration that takes 24+ hours of runtime would need to be run outside of TD. 

Hence, note that on large volumes of data and running model with higher matrix dimensionality (e.g., longer lookback periods, more distinct channels in `channel_col`), it will take about 5-6 hours per training epoch and another 2-4 housrs for TensorFlow record creation and random shuffling + Shapely Value calculations, so expect model to take 24+ hours to complete. In those cases, we advise running only the SQL portion of the workflow first, and download the Python code and run locally or inside an EC2 instance. More instructions on how to do that can be found in [`td_mta/README.md`](../td_mta/README.md). 

## How to execute Python code locally, independent from workflow functions?

As mentioned earlier, if you hit memory limit error in TD, you might want to run the model on your local machine or possibly in an EC2 instance with multiple GPUs available. Most of the approach for running the code locally is fairly similar, but broken in two parts:

1.  Run SQL code in TD workflow 
    - You need to comment out the `py>` part of the workflow and then run the workflow to only execute the initial SQL data transformation steps and output the final table of touchpoints and conversions.
2.  Download the workflow locally via [TD Toolbelt CLI](https://toolbelt.treasuredata.com/)
    - Or, just extract the `td_mta` folder from the original project file. That folder contains a `README.md` file that explains the steps you need to take to install the `requirements.txt` file and configure the `config.py` file.
3.  Follow the steps shared earlier in the doc on how to configure the `config.py` file with the proper database, table names and hyper-parameters before you execute the `main.py`. 
4.  In CLI, navigate to the `td_mta` project folder directory and first make sure you set your `TD_API_KEY`:
    ```
    $ export TD_API_KEY='PASTE MASTER API KEY HERE'
    ```
5.  Requires Python 3.7 or higher. Install requirements:
    ```
    $ pip install -r requirements.txt
    ```
6.  Lastly, execute the command below in CLI, to run the `main.py` file inside the `td_mta` folder:
    ```
    $ python3 -m td_mta.main
    ```
    This will trigger the `main.py` file in the `td_mta` folder and you will be able to see the logs that the Python code is programmed to print in the CLI.

The model might take anywhere from 2 - 24+ hours depending on the volume of data that is being fed and the number of training epochs in the `config.py` file (default = 3).

## How to interpret the model output and use its insights to help marketing teams understand the effectiveness of different advertising channels and plan marketing budgets more efficiently?

Typically, it is normal to see Shapley Values decreasing with time. However, some channels may retain decent shapely ratios even when further away from conversion, which will indicate that they are more influential than other channels and better at initiating user interest and possible journeys to conversion. That is, such channels can justify higher marketing budgets and more aggressive spend, especially during direct response-focused campaigns with high Return On Investment (ROI) / Cost Per Acquisition (CPA) goals. 

> **NOTE**
> 
> In a perfect world, you would not expect to see negative Shapley values, but in reality, we often do. Why? The reason is some marketing channels have a proclivity to bring in a lot of unqualified traffic. For example, it is common for display ad click-throughs to be accidental, which means that if I see a visitor to my site from a display ad click-through, we can usually predict that visitor will not convert. The Shapley values pick up on that fact and sometimes exhibit negative values in our matrix as a result.
> 
> Other channels might only have slightly positive values one or two days close to conversion and then get close to 0 or negative Shapley Values after that, which means that they don't seem to have a long-lasting effect on user behavior and are mostly effective as a final push when the user is further down the customer journey funnel and closer to the final purchase decision. Such channels would not be justified constant heavy spending of marketing budget and might be more effective at a campaign set up of less daily impressions on unknown or new users, but higher impression frequency when the user has shown a higher intent to purchase such as actively browsed the product page or maybe added something to cart more recently.

Another effective use of the Shapley Attribution ratios is when they are combined with specific campaign data such as impression counts and CPM per channel. For instance, knowing the total number of conversions that occur during the time interval of the data that the MTA model was trained on, we can multiply the shapely ratio for each channel times total conversion count to estimate how many conversion events get attributed to each channel. From there we can add data for our marketing budget spend per channel during that same time period the MTA model was trained on. Knowing total spend and number of conversions, we can now calculate CPA for each channel and start understanding where we can shift budgets to optimize ad spend and improve marketing KPIs such as ROMS.