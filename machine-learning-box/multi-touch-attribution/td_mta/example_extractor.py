import itertools
import more_itertools
from dataclasses import dataclass
from typing import Generator, List, Tuple, Union

from td_mta.parser import Session, Journey

ExampleIndices = List[Tuple[int, int]]


@dataclass
class ExampleExtractor:
    lookback_window_days: int

    def extract_positive(self, journey: Journey) -> Generator[Union[ExampleIndices, None], None, None]:

        segments = more_itertools.split_after(journey, lambda session: session.conversion)

        for segment in segments:
            if segment[-1].conversion:

                def in_window(session: Session) -> bool:
                    return session.date + self.lookback_window_days > segment[-1].date

                def date_action(session: Session) -> Tuple[int, int]:
                    return session.date - segment[-1].date + self.lookback_window_days - 1, session.action

                yield sorted(set(date_action(session) for session in segment if in_window(session)))
            else:
                yield

    def extract_negative(self, journey: Journey) -> Generator[Union[ExampleIndices, None], None, None]:

        if any(session.conversion for session in journey):
            yield  # don't extract negative examples from journeys with conversions
        else:
            # extract all subsequences of length up to lookback_window_days from regressors
            daily_segments = list(more_itertools.split_when(journey, lambda s1, s2: s1.date != s2.date))

            first, last = 0, 1
            while first < len(daily_segments):

                def date_action(session: Session) -> Tuple[int, int]:
                    date = session.date - daily_segments[last - 1][0].date + self.lookback_window_days - 1
                    return date, session.action

                chained_daily_segments = itertools.chain.from_iterable(daily_segments[first:last])
                yield sorted(set(date_action(session) for session in chained_daily_segments))

                if last < len(daily_segments):
                    last += 1
                    while daily_segments[first][0].date + self.lookback_window_days <= daily_segments[last - 1][0].date:
                        first += 1
                else:
                    first += 1
