import os
import tensorflow as tf
from dataclasses import dataclass
from typing import Optional

from td_mta.model import Model
from td_mta.config import Config

_dir = os.path.dirname(os.path.abspath(__file__))

METRICS = [
    tf.keras.metrics.RootMeanSquaredError(name='rmse'),
]


class MTATrain:
    mask_value: Optional[float] = -1.

    @dataclass
    class HyperParameters:
        units: int = 128
        dropout_rate: float = 0.5
        train_epochs: int = 10

        @classmethod
        def from_config(cls, config: Config):
            return cls(
                units=config.model_width,
                dropout_rate=config.dropout_rate,
                train_epochs=config.train_epochs,
            )

    def __init__(self, seq_length: int, hyper_parameters: Optional[HyperParameters] = None):
        self._params = MTATrain.HyperParameters() if hyper_parameters is None else hyper_parameters
        self.seq_length = seq_length
        self.model = None
        self.model_train_history = None

    def train(self, dataset_train: tf.data.Dataset, dataset_validate: tf.data.Dataset, filepath: str) -> \
            tf.keras.callbacks.History:
        self.model = Model(units=self._params.units, dropout_rate=self._params.dropout_rate, mask_value=self.mask_value)
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)

        # FIXME: uncomment for saving best model only
        # save_model_callback = tf.keras.callbacks.ModelCheckpoint(filepath=filepath, save_best_only=True)
        # callbacks = [save_model_callback]
        callbacks = []

        history = self.model.fit(dataset_train,
                                 shuffle=False,  # dataset_train assumed shuffled
                                 epochs=self._params.train_epochs,
                                 validation_data=dataset_validate,
                                 callbacks=callbacks,
                                 )
        return history

    def load(self, filepath: str):
        # FIXME: save using file name, not prefix
        self.model = tf.keras.models.load_model(filepath=filepath)
