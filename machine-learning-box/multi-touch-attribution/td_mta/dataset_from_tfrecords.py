import os
import tensorflow as tf
from functools import partial
from typing import Optional, Tuple


def dataset_from_tfrecords(tfrecords_directory: str,
                           dense_shape: Tuple[int, int],
                           leave_as_sparse: Optional[bool] = False,
                           ) -> tf.data.Dataset:
    def listdir(directory):
        return [os.path.join(directory, filename) for filename in os.listdir(directory)]

    dataset = tf.data.TFRecordDataset(listdir(tfrecords_directory))

    def make_parse_function():
        features = dict(features=tf.io.FixedLenFeature(shape=(3,), dtype=tf.dtypes.string),  # shape=3 for sparse tensor
                        labels=tf.io.FixedLenFeature(shape=(), dtype=tf.dtypes.int64))
        return partial(tf.io.parse_single_example, features=features)

    def deserialize_sparse_function(inputs):
        features, labels = inputs['features'], inputs['labels']
        features = tf.io.deserialize_many_sparse(features[tf.newaxis, ...], dtype=tf.dtypes.float32)
        if not leave_as_sparse:
            features = tf.sparse.to_dense(features)
            features = tf.squeeze(features, axis=0)
            features = tf.ensure_shape(features, shape=dense_shape)
        return dict(features=features, labels=labels)

    return dataset.map(make_parse_function()).map(deserialize_sparse_function)
