import random
import time
import string
import pytd
import pandas as pd
from typing import Iterable, List, Tuple
from tqdm import tqdm


def gen_user_ids(num_users: int, id_length=10) -> List[str]:
    hsh = ''.join(random.choices(string.ascii_lowercase + string.digits, k=id_length * num_users))
    return [hsh[0 + i: id_length + i] for i in range(0, len(hsh), id_length)]


def get_impressions(impression_probability: float, conversion_probability: float, num_days: int, start_time: int) -> \
        Iterable[Tuple[int, int]]:
    impressions = random.choices([1, 0], weights=[impression_probability, 1. - impression_probability], k=num_days)
    times = random.choices(range(3600 * 24), k=num_days)
    impression_times = [start_time + idx * 3600 * 24 + t for idx, t in enumerate(times) if impressions[idx] == 1]
    conversions = random.choices([1, 0], weights=[conversion_probability, 1. - conversion_probability],
                                 k=len(impression_times))

    return zip(impression_times, conversions)


def main():
    num_users = 20000
    # converted_users_fraction = 0.2
    num_days = 60
    start_time = int(time.time()) - num_days * 3600 * 24
    user_ids = gen_user_ids(num_users)
    database = 'mta'
    table = 'mock_data'
    impression_distribution = dict(facebook=.05, instagram=.1, google=.05, sfmc=.01, direct=.005)
    conversion_propensity = dict(facebook=.05, instagram=.05, google=.05, sfmc=.05, direct=.05)

    # table = 'mock_data_v1'
    # num_users = 100000
    # converted_users_fraction = 0.2
    # impression_distribution = dict(facebook=.2, instagram=.4, google=.2, sfmc=.1, direct=.05)
    # conversion_propensity = dict(facebook=.2, instagram=.8, google=.2, sfmc=.9, direct=.01)
    #     # == wrote
    #     # 593925
    #     # positive
    #     # examples and 3296588
    #     # negative
    #     # examples
    #     # to
    #     # TFRecord
    #     # files

    sources = list(impression_distribution.keys())

    data = []
    for user_id in tqdm(user_ids):
        ab_rnd = random.random()
        for source in sources:
            conversion_probability = conversion_propensity[source]
            impressions = get_impressions(impression_distribution[source], conversion_probability, num_days, start_time)
            data += [(user_id, t, source, conversion, ab_rnd) for t, conversion in impressions]

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
