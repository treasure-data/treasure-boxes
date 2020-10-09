import os
import shutil
import itertools
import tensorflow as tf
from typing import Iterable, List, Tuple

from td_mta.config import Config
from td_mta.parser import Parser, Journey
from td_mta.example_extractor import ExampleExtractor
from td_mta.td_connector import TDConnector


def parse_and_save_tfrecords(config: Config) -> Tuple[int, int]:
    for tfrecords_dir in [config.positive_tfrecords_dir, config.negative_tfrecords_dir]:
        print(f'==cleaning up tfrecords directory: {tfrecords_dir}')
        if os.path.isdir(tfrecords_dir):
            shutil.rmtree(tfrecords_dir)
        os.mkdir(tfrecords_dir)

    parser = Parser(action_vocab=config.action_vocab,
                    user_column=config.user_column,
                    action_column=config.action_column,
                    time_column=config.time_column,
                    conversion_column=config.conversion_column)

    dataframes = TDConnector.paginate(db=config.db,
                                      table=config.table,
                                      group_by=parser.user_column,
                                      user_rnd_column=config.user_rnd_column,
                                      count_per_page=config.users_per_tfrecord)

    count_positive, count_negative = 0, 0

    for page_num, dataframe in enumerate(dataframes):

        journeys: Iterable[Journey] = parser.parse(dataframe)

        print(f'==Extracting positive and negative examples')
        example_extractor = ExampleExtractor(lookback_window_days=config.lookback_window_days)

        positive_iterator, negative_iterator = itertools.tee(journeys, 2)
        del journeys

        # bucketing by day and fix number of days window positive and negative features extraction
        positive_examples = map(lambda t: example_extractor.extract_positive(t), positive_iterator)
        negative_examples = map(lambda t: example_extractor.extract_negative(t), negative_iterator)

        positive_examples = itertools.chain.from_iterable(positive_examples)
        negative_examples = itertools.chain.from_iterable(negative_examples)

        positive_examples = filter(None, positive_examples)
        negative_examples = filter(None, negative_examples)

        def serialize_example(indices: List[Tuple[int, int]], label: int) -> bytes:
            dense_shape = config.lookback_window_days, len(config.action_vocab)
            sparse_tensor = tf.sparse.SparseTensor(indices=indices, values=[1.] * len(indices), dense_shape=dense_shape)
            serialized = tf.io.serialize_sparse(sparse_tensor).numpy()
            feature = dict(features=tf.train.Feature(bytes_list=tf.train.BytesList(value=serialized)),
                           labels=tf.train.Feature(int64_list=tf.train.Int64List(value=[label])))
            return tf.train.Example(features=tf.train.Features(feature=feature)).SerializeToString()

        positive_dataset_file_name = os.path.join(config.positive_tfrecords_dir, f'positive_page{page_num}.tfrecord')
        negative_dataset_file_name = os.path.join(config.negative_tfrecords_dir, f'negative_page{page_num}.tfrecord')

        writer = tf.io.TFRecordWriter(positive_dataset_file_name)
        for example in positive_examples:
            writer.write(serialize_example(example, label=1))
            count_positive += 1
        writer.close()

        writer = tf.io.TFRecordWriter(negative_dataset_file_name)
        for example in negative_examples:
            writer.write(serialize_example(example, label=0))
            count_negative += 1
        writer.close()

    print(f'==wrote {count_positive} positive examples and {count_negative} negative examples to TFRecord files')

    return count_positive, count_negative
