import pandas as pd
import tensorflow as tf
from typing import Dict, Tuple

from td_mta.config import Config
from td_mta.mta_train import MTATrain
from td_mta.model import CalibratedModel
from td_mta.dataset_from_tfrecords import dataset_from_tfrecords


def train_model_from_tfrecords(config: Config, count_positive: int, count_negative: int) -> pd.DataFrame:
    dense_shape = config.lookback_window_days, len(config.action_vocab)

    positive_dataset = dataset_from_tfrecords(tfrecords_directory=config.positive_tfrecords_dir,
                                              dense_shape=dense_shape)

    negative_dataset = dataset_from_tfrecords(tfrecords_directory=config.negative_tfrecords_dir,
                                              dense_shape=dense_shape)

    def dict_to_tuple(row: Dict[str, tf.Tensor]) -> Tuple[tf.Tensor, tf.Tensor]:
        return row['features'], row['labels']

    positive_dataset = positive_dataset.map(dict_to_tuple)
    negative_dataset = negative_dataset.map(dict_to_tuple)

    num_validate_positive = int(count_positive * config.validation_fraction)
    num_validate_negative = int(count_negative * config.validation_fraction)
    validate_cardinality = max(num_validate_positive, num_validate_negative)

    num_train_positive = count_positive - num_validate_positive
    num_train_negative = count_negative - num_validate_negative
    train_cardinality = max(num_train_positive, num_train_negative)

    positive_dataset_train, positive_dataset_validate = \
        positive_dataset.skip(num_validate_positive), positive_dataset.take(num_validate_positive)

    negative_dataset_train, negative_dataset_validate = \
        negative_dataset.skip(num_validate_negative), negative_dataset.take(num_validate_negative)

    def random_downsample_bool(features, labels):
        p = config.downsample_epoch_fraction
        r = tf.random.categorical(tf.math.log([[1. - p, p]]), 1)
        return tf.cast(r[0, 0], dtype=tf.dtypes.bool)

    train_cardinality = int(train_cardinality * config.downsample_epoch_fraction)

    dataset_train = tf.data.experimental.choose_from_datasets(
        datasets=[positive_dataset_train.repeat().filter(random_downsample_bool),
                  negative_dataset_train.repeat().filter(random_downsample_bool)],
        choice_dataset=tf.data.Dataset.range(2).repeat(train_cardinality))

    dataset_train = dataset_train.shuffle(buffer_size=config.shuffle_buffer_size)
    dataset_train = dataset_train.batch(batch_size=config.train_batch_size)

    def augment_batch_with_zeros(features, labels):
        features_without_last_day_impressions = features[..., :-1, :]
        zeroed_last_day_impressions = tf.zeros_like(features[..., -1:, :])
        augmented_features = tf.concat((features_without_last_day_impressions, zeroed_last_day_impressions), axis=-2)
        zero_labels = tf.zeros_like(labels)
        return tf.concat((features, augmented_features), axis=0), tf.concat((labels, zero_labels), axis=0)

    dataset_train = dataset_train.map(augment_batch_with_zeros)

    dataset_validate = tf.data.experimental.choose_from_datasets(
        datasets=[positive_dataset_validate.repeat(), negative_dataset_validate.repeat()],
        choice_dataset=tf.data.Dataset.range(2).repeat(validate_cardinality)
    )

    dataset_validate = dataset_validate.batch(config.validation_batch_size)

    hyper_parameters = MTATrain.HyperParameters.from_config(config)
    mta = MTATrain(seq_length=config.lookback_window_days, hyper_parameters=hyper_parameters)
    training_history = mta.train(dataset_train=dataset_train,
                                 dataset_validate=dataset_validate,
                                 filepath=config.model_dir)

    # FIXME: model can also be saved in tf.keras.Model.fit() via tf.keras.callbacks.ModelCheckpoint()

    calibrated_model = CalibratedModel(class_balanced_model=mta.model,
                                       count_positive=count_positive,
                                       count_negative=count_negative)
    _ = calibrated_model.predict(dataset_train.take(1))  # calling once to determine dynamic shapes
    calibrated_model.save(filepath=config.model_dir)

    return pd.DataFrame.from_dict(training_history.history)
