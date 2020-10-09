import pandas as pd
import tensorflow as tf
from typing import Callable, Tuple

from td_mta.config import Config
from td_mta.dataset_from_tfrecords import dataset_from_tfrecords
from td_mta.mta_train import MTATrain


def shapley_inputs_one_sample(sparse_positive_example: tf.sparse.SparseTensor, dense_shape: Tuple[int, int]) -> \
        Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    ones_like_values = tf.ones_like(sparse_positive_example.values)
    tf.debugging.assert_equal(sparse_positive_example.values, ones_like_values), 'assuming non-zero elements equal 1.'

    indices = tf.random.shuffle(sparse_positive_example.indices)
    num_indices = tf.shape(indices)[0]

    random_len = tf.random.uniform(shape=(), minval=1, maxval=num_indices + 1, dtype=tf.dtypes.int32)

    ones = tf.ones(shape=(random_len,), dtype=tf.dtypes.bool)
    zeros = tf.zeros(shape=(num_indices - random_len + 1,), dtype=tf.dtypes.bool)
    retain_inclusive = tf.concat((ones, zeros[:-1]), axis=0)
    retain_exclusive = tf.concat((ones[:-1], zeros), axis=0)
    toggled_index = indices[random_len - 1]

    sparse_positive_example_shuffled = tf.sparse.SparseTensor(indices=indices, values=ones_like_values,
                                                              dense_shape=sparse_positive_example.dense_shape)

    example_inclusive = tf.sparse.retain(sp_input=sparse_positive_example_shuffled, to_retain=retain_inclusive)
    example_exclusive = tf.sparse.retain(sp_input=sparse_positive_example_shuffled, to_retain=retain_exclusive)

    example_inclusive = tf.sparse.reorder(example_inclusive)
    example_exclusive = tf.sparse.reorder(example_exclusive)

    example_inclusive = tf.sparse.to_dense(example_inclusive)
    example_exclusive = tf.sparse.to_dense(example_exclusive)

    example_inclusive = tf.ensure_shape(example_inclusive, shape=dense_shape)
    example_exclusive = tf.ensure_shape(example_exclusive, shape=dense_shape)

    return example_exclusive, example_inclusive, toggled_index


def make_shapley_inputs(num_samples: int, dense_shape: Tuple[int, int]) -> \
        Callable[[tf.sparse.SparseTensor], Tuple[tf.Tensor, tf.Tensor, tf.Tensor]]:
    def shapley_inputs(sparse: tf.sparse.SparseTensor) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        # sparse = tf.sparse.from_dense(tensor)

        examples_exclusive, examples_inclusive, included_excluded_indices = [], [], []
        for _ in range(num_samples):
            example_inclusive, example_exclusive, included_excluded_index = \
                shapley_inputs_one_sample(sparse_positive_example=sparse, dense_shape=dense_shape)
            examples_exclusive.append(example_inclusive)
            examples_inclusive.append(example_exclusive)
            included_excluded_indices.append(included_excluded_index)

        examples_exclusive = tf.stack(examples_exclusive)
        examples_inclusive = tf.stack(examples_inclusive)
        included_excluded_indices = tf.stack(included_excluded_indices)

        return examples_exclusive, examples_inclusive, included_excluded_indices

    return shapley_inputs


def make_shapley(model: tf.keras.Model) -> Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor]:
    def shapley(example_exclusive: tf.Tensor, examples_inclusive: tf.Tensor, included_excluded_indices: tf.Tensor) \
            -> tf.Tensor:
        dense_shape = tf.cast(tf.shape(examples_inclusive), dtype=tf.dtypes.int64)

        diff = model(examples_inclusive) - model(example_exclusive)

        arange = tf.range(start=0, limit=tf.shape(included_excluded_indices)[0], dtype=included_excluded_indices.dtype)
        included_excluded_indices = tf.concat((arange[..., tf.newaxis], included_excluded_indices), axis=1)

        diff = tf.squeeze(diff, axis=1)
        diff = tf.sparse.SparseTensor(indices=included_excluded_indices, values=diff, dense_shape=dense_shape)
        return tf.sparse.reduce_sum(sp_input=diff, axis=0)

    return shapley


def squeeze_batch_dim(s: tf.sparse.SparseTensor) -> tf.sparse.SparseTensor:
    return tf.sparse.SparseTensor(indices=s.indices[:, 1:], values=s.values, dense_shape=s.dense_shape[1:])


def calculate_shapley(config: Config) -> Tuple[pd.DataFrame, pd.DataFrame]:
    hyper_parameters = MTATrain.HyperParameters.from_config(config)

    mta = MTATrain(seq_length=config.lookback_window_days, hyper_parameters=hyper_parameters)
    mta.load(filepath=config.model_dir)

    # # FIXME: DEBUG
    # import itertools
    # import numpy as np
    # inputs = np.array(list(map(list, itertools.product((0., 1.), repeat=2))), dtype=np.float32)
    # inputs = inputs[:, np.newaxis, :]
    # print('inputs:\n', inputs)
    # print('outputs:\n', mta.model(inputs).numpy())

    dense_shape = config.lookback_window_days, len(config.action_vocab)

    positive_dataset = dataset_from_tfrecords(tfrecords_directory=config.positive_tfrecords_dir,
                                              dense_shape=dense_shape,
                                              leave_as_sparse=True)
    negative_dataset = dataset_from_tfrecords(tfrecords_directory=config.negative_tfrecords_dir,
                                              dense_shape=dense_shape,
                                              leave_as_sparse=True)

    dataset = positive_dataset.concatenate(negative_dataset)

    features_dataset = dataset.map(lambda row: row['features'])
    features_dataset = features_dataset.map(squeeze_batch_dim)

    num_random_permutations = 10
    shapley_inputs = make_shapley_inputs(num_samples=num_random_permutations, dense_shape=dense_shape)
    shapley_inputs_dataset = features_dataset.map(shapley_inputs)

    shapley = make_shapley(mta.model)
    shapley_outputs_dataset = shapley_inputs_dataset.map(shapley)

    reduced = shapley_outputs_dataset.reduce(initial_state=tf.zeros(shape=dense_shape), reduce_func=tf.math.add)
    shapley_values = (reduced / tf.reduce_sum(reduced)).numpy()

    print('shapley values by time:')
    for day_in_window, value in enumerate(shapley_values.sum(axis=1)):
        print(f'{config.lookback_window_days - 1 - day_in_window} days before conversion: {value}')
    print()

    print('shapley values by channel:')
    for action, value in zip(config.action_vocab, shapley_values.sum(axis=0)):
        print(f'{action}: {value}')
    print()

    print('all shapley values:')
    print(shapley_values)

    df = pd.DataFrame(shapley_values, columns=config.action_vocab)
    df['days_before_conversion'] = range(config.lookback_window_days - 1, -1, -1)
    return df, df.sum().to_frame().transpose().drop('days_before_conversion', axis=1)
