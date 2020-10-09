import more_itertools
import pandas as pd
from typing import List, Iterable
from dataclasses import dataclass


@dataclass
class Session:
    action: int
    date: int
    conversion: bool


Journey = List[Session]


@dataclass
class Parser:
    action_vocab: List[str]
    user_column: str
    time_column: str
    action_column: str
    conversion_column: str

    def parse(self, df: pd.DataFrame) -> Iterable[Journey]:
        groups = (group for _, group in df.groupby(self.user_column, sort=False))
        groups = more_itertools.random_permutation(groups)  # randomly shuffle users
        return map(self.extract, groups)

    def extract(self, group: pd.DataFrame) -> Journey:
        session_data = group[[self.time_column, self.action_column, self.conversion_column]]
        session_data = session_data.sort_values(self.time_column).values.tolist()
        return [self.session(timestamp, action, conversion) for timestamp, action, conversion in session_data]

    def session(self, timestamp: int, action: str, conversion: bool) -> Session:
        return Session(action=self.action_vocab.index(action),
                       date=timestamp // (24 * 3600),
                       conversion=conversion)
