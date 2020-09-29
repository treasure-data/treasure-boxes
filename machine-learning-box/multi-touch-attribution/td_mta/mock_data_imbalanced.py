import random
import string
import pytd
import pandas as pd
from typing import List


def gen_user_ids(num_users: int, id_length=10) -> List[str]:
    hsh = ''.join(random.choices(string.ascii_lowercase + string.digits, k=id_length * num_users))
    return [hsh[0 + i: id_length + i] for i in range(0, len(hsh), id_length)]


def main():
    database = 'mta'
    table = 'mock_data_imbalanced'

    num_awareness = 100
    num_promo_code = 1
    num_conversion_per_channel = 1

    assert num_promo_code == num_conversion_per_channel

    journey_sources = ['awareness'] * num_awareness + ['promo_code'] * num_promo_code
    journey_conversions = \
        [1] * num_conversion_per_channel + [0] * (num_awareness - num_conversion_per_channel) + \
        [1] * num_promo_code

    assert len(journey_conversions) == len(journey_sources)
    journey_random = [random.random() for _ in journey_sources]
    journey_times = [0 for _ in journey_sources]
    num_users = len(journey_sources)

    user_ids = gen_user_ids(num_users)

    data = list(zip(user_ids, journey_times, journey_sources, journey_conversions, journey_random))

    df = pd.DataFrame(data, columns=['user_id', 'time', 'source', 'conversion', 'ab_rnd'])
    df.sort_values('time', inplace=True)

    # metrics
    conversion_counts = df.groupby('user_id').sum()
    print(conversion_counts.sort_values('conversion'))
    print('==Conversion counts per user histogram')
    print(pd.cut(conversion_counts['conversion'], 10).value_counts().sort_index())

    client = pytd.Client(database=database)
    table = pytd.table.Table(client, database, table)
    writer = pytd.writer.BulkImportWriter()
    writer.write_dataframe(df, table, if_exists='overwrite')

    return df


if __name__ == '__main__':
    main()
