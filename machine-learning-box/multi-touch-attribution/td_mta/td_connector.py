import pandas as pd
import pytd


class TDConnector:

    @staticmethod
    def read(db: str, table: str) -> pd.DataFrame:
        client = pytd.Client(database=db)
        results = client.query(f'select * from {table}')
        columns = results['columns']
        data = results['data']
        return pd.DataFrame(data=data, columns=columns)

    @staticmethod
    def write_group_map(client: pytd.Client, db: str, table: str, group_by: str, write_to: str):
        query = f'''select rand(18) as ab_rnd, {group_by}
from  (select distinct {group_by} from {table}) as T1
cluster by rand(43)'''

        results = client.query(query, engine='hive')
        columns = results['columns']
        data = results['data']
        df = pd.DataFrame(data=data, columns=columns)
        write_table = pytd.table.Table(client, db, write_to)
        writer = pytd.writer.BulkImportWriter()
        writer.write_dataframe(df, write_table, if_exists='overwrite')

        return len(df)

    @staticmethod
    def batch_query(table: str, start: float, end: float, user_rnd_column: str):
        return f'''SELECT * from {table}
WHERE {user_rnd_column} >= {start} AND {user_rnd_column} < {end}'''

    @staticmethod
    def paginate(db: str, table: str, group_by: str, user_rnd_column: str, count_per_page: int):
        client = pytd.Client(database=db)

        total_count = client.query(f'select COUNT(DISTINCT({group_by})) from {table}')['data'][0][0]
        batches = list(range(0, count_per_page * total_count // count_per_page, count_per_page)) + [total_count]
        batches = [b / total_count for b in batches]
        print(f'==Total users: {total_count}. Splitting into {len(batches)} batches')

        for start, end in zip(batches[:-1], batches[1:]):
            query = TDConnector.batch_query(table=table, start=start, end=end,
                                            user_rnd_column=user_rnd_column)
            print(f'==Fetching {query}')
            results = client.query(query)
            columns = results['columns']
            data = results['data']
            yield pd.DataFrame(data=data, columns=columns)

    @staticmethod
    def write(df: pd.DataFrame, db: str, table: str, if_exists: str = 'error'):
        client = pytd.Client(database=db)
        table = pytd.table.Table(client, db, table)
        writer = pytd.writer.BulkImportWriter()
        writer.write_dataframe(df, table, if_exists=if_exists)

    @staticmethod
    def distinct(db: str, table: str, column: str):
        client = pytd.Client(database=db)
        return [row[0] for row in client.query(f'select DISTINCT({column}) from {table}')['data']]
