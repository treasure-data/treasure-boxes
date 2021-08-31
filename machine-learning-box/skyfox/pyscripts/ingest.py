import os
import sys

os.system(f"{sys.executable} -m pip install --upgrade pytd==1.4.0")
apikey = os.environ["TD_API_KEY"]
endpoint = os.environ["TD_API_SERVER"]
path = './pyscripts/data'

def classification_dataset(database):
    import pandas as pd
    import pytd
    client = pytd.Client(apikey=apikey, endpoint=endpoint)

    # train
    df = pd.read_csv(f'{path}/classification_train.csv')
    client.load_table_from_dataframe(df, f'{database}.classification_train', if_exists='overwrite')
    
    # pred
    df = pd.read_csv(f'{path}/classification_pred.csv')
    client.load_table_from_dataframe(df, f'{database}.classification_pred', if_exists='overwrite')

def regression_dataset(database):
    import pandas as pd
    import pytd
    client = pytd.Client(apikey=apikey, endpoint=endpoint)

    # train
    df = pd.read_csv(f'{path}/regression_train.csv')
    client.load_table_from_dataframe(df, f'{database}.regression_train', if_exists='overwrite')
    
    # pred
    df = pd.read_csv(f'{path}/regression_pred.csv')
    client.load_table_from_dataframe(df, f'{database}.regression_pred', if_exists='overwrite')

def timeseries1_dataset(database):
    import pandas as pd
    import pytd
    client = pytd.Client(apikey=apikey, endpoint=endpoint)

    # train
    df = pd.read_csv(f'{path}/timeseries1_train.csv')
    client.load_table_from_dataframe(df, f'{database}.timeseries1_train', if_exists='overwrite')
    
    # pred
    df = pd.read_csv(f'{path}/timeseries1_pred.csv')
    client.load_table_from_dataframe(df, f'{database}.timeseries1_pred', if_exists='overwrite')

def timeseries2_dataset(database):
    import pandas as pd
    import pytd
    client = pytd.Client(apikey=apikey, endpoint=endpoint)

    # train
    df = pd.read_csv(f'{path}/timeseries2_train.csv')
    client.load_table_from_dataframe(df, f'{database}.timeseries2_train', if_exists='overwrite')
    
    # pred
    df = pd.read_csv(f'{path}/timeseries2_pred.csv')
    client.load_table_from_dataframe(df, f'{database}.timeseries2_pred', if_exists='overwrite')

def main(database):
    classification_dataset(database)
    regression_dataset(database)
    timeseries1_dataset(database)
    timeseries2_dataset(database)

if __name__ == '__main__':
    database = 'skyfox'
    classification_dataset(database)
    regression_dataset(database)
    timeseries1_dataset(database)
    timeseries2_dataset(database)
