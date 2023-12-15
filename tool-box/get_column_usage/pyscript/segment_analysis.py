import os, sys
import json
from functools import cached_property

packages = [
    'pandas==1.5.2',
    'pytd==1.5.1',
    'tqdm==4.64.1'
]

def installed_packages():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])
    return installed_packages_list

# Install required packages
for package in packages:
    if package not in installed_packages():
        os.system(f"{sys.executable} -m pip install -U {package}")


# Load environment variables
TD_API_KEY = os.environ['TD_API_KEY']
TD_ENDPOINT = os.environ['TD_ENDPOINT']
SESSION_TIME = int(os.environ['SESSION_TIME'])

from collections import Counter
from .audience_studio import ParentSegment


def count_columns_in_segment_rules(parent_segment_id: int) -> dict:
    '''
        Count the number of segments for each columns used in rule
    '''

    parent_segment = ParentSegment(parent_segment_id)
    root_folder = parent_segment.get_root_folder()
    segments = root_folder.list_batch_segments()

    columns = []
    for segment in segments:
        columns_ = segment.extract_columns_in_rule()
        columns += columns_
    return dict(Counter(columns))


def count_columns_in_activations(parent_segment_id: int) -> dict:
    '''
        Count the number of activations for each columns
    '''

    parent_segment = ParentSegment(parent_segment_id)
    activations = parent_segment.get_activations()

    columns = []
    activations_with_all_columns = 0
    for activation in activations:
        if activation.columns:
            columns += activation.columns
        if activation.all_columns:
            activations_with_all_columns += 1

    counter = Counter(columns)
    counter['__allColumns__'] = activations_with_all_columns
    
    return dict(counter)


def list_used_columns_in_segments(parent_segment_id: int) -> list:
    '''
        list used columns for each segments
    '''

    parent_segment = ParentSegment(parent_segment_id)
    root_folder = parent_segment.get_root_folder()
    segments = root_folder.list_batch_segments()

    ret = []
    for segment in segments:
        ret += list(map(lambda x: [segment.id, segment.name, x], segment.extract_columns_in_rule()))
    return ret


def list_used_columns_in_activations(parent_segment_id: int) -> dict:
    '''
        list used columns for each activations
    '''

    parent_segment = ParentSegment(parent_segment_id)
    activations = parent_segment.get_activations()

    ret = []
    for activation in activations:
        segment = activation.segment

        if activation.columns:
            columns = list(set(activation.columns))
            ret += list(map(lambda x: [segment.id, segment.name, activation.id, activation.name, x], columns))
        if activation.all_columns:
            ret.append([segment.id, segment.name, activation.id, activation.name, 'all_column'])
    
    return ret


def main(
        parent_segment_id_list: list,
        database: str
        ):
    import pandas as pd
    import pytd
    from tqdm import tqdm

    client = pytd.Client(apikey=TD_API_KEY, endpoint=TD_ENDPOINT, database=database)
    client.create_database_if_not_exists(database)


    def create_columns_used_in_segments_df(parent_segment_id: int) -> pd.DataFrame:
        counts = count_columns_in_segment_rules(parent_segment_id)
        df = pd.DataFrame.from_dict(counts, orient='index', columns=['count'])
        df['parent_segment_id'] = parent_segment_id
        return df

    def create_count_columns_in_activations_df(parent_segment_id: int) -> pd.DataFrame:
        counts = count_columns_in_activations(parent_segment_id)
        df = pd.DataFrame.from_dict(counts, orient='index', columns=['count'])
        df['parent_segment_id'] = parent_segment_id
        return df

    def create_columns_used_list_in_segments_df(parent_segment_id: int) -> pd.DataFrame:
        columns_list = list_used_columns_in_segments(parent_segment_id)
        df = pd.DataFrame(columns_list, columns=['segment_id', 'segment_name', 'column_name'])
        df['parent_segment_id'] = parent_segment_id
        return df

    def create_columns_used_list_in_activations_df(parent_segment_id: int) -> pd.DataFrame:
        columns_list = list_used_columns_in_activations(parent_segment_id)
        df = pd.DataFrame(columns_list, columns=['segment_id', 'segment_name', 'activation_id', 'activations_name', 'column_name'])
        df['parent_segment_id'] = parent_segment_id
        return df

    def before_insert(
        client: pytd.Client, 
        database: str, 
        table: str
    ) -> None:
        # Create table if not exists
        create_table_query = f'''
            create table if not exists {database}.{table} as select 1 as time with no data
        '''
        client.query(create_table_query)

        # Delete existing records
        delete_query = f'''
            delete from {database}.{table} where time = {SESSION_TIME}
        '''
        client.query(delete_query)

        return

    def append_to_td_table(
        client: pytd.Client, 
        df: pd.DataFrame, 
        database: str, 
        table: str
    ) -> None:
        '''
            Append dataframe into a specified table.
            If records with SESSION_UNIX time exist, delete them beforehand.
        '''
        before_insert(client, database, table)

        df['time'] = SESSION_TIME
        df.index.name = 'columns'
        client.load_table_from_dataframe(
            df.reset_index(), 
            f'{database}.{table}', 
            if_exists='append'
        )

    # Append result of `count_columns_in_segment_rules`
    df_list = [create_columns_used_in_segments_df(id_) 
                for id_ in tqdm(parent_segment_id_list)]
    df = pd.concat(df_list)
    append_to_td_table(client, df, database, 'counts_columns_used_in_segments')

    # Append result of `count_columns_in_activations`
    df_list = [create_count_columns_in_activations_df(id_) 
                for id_ in tqdm(parent_segment_id_list)]
    df = pd.concat(df_list)
    append_to_td_table(client, df, database, 'counts_columns_used_in_activations')

    # Append result of `list_columns_used_in_segments`
    table = 'list_columns_used_in_segments'
    df_list = [create_columns_used_list_in_segments_df(id_) 
                for id_ in tqdm(parent_segment_id_list)]
    df = pd.concat(df_list)
    before_insert(client, database, table)
    df['time'] = SESSION_TIME
    client.load_table_from_dataframe(df, f'{database}.{table}', if_exists='append')    

    # Append result of `list_columns_used_in_activations`
    table = 'list_columns_used_in_activations'
    df_list = [create_columns_used_list_in_activations_df(id_) 
                for id_ in tqdm(parent_segment_id_list)]
    df = pd.concat(df_list)
    before_insert(client, database, table)
    df['time'] = SESSION_TIME
    client.load_table_from_dataframe(df, f'{database}.{table}', if_exists='append')    

    return