import tensorflow as tf

METRICS = [
    tf.keras.metrics.TruePositives(name='tp'),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'),
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall'),
    tf.keras.metrics.AUC(name='auc'),
]


class Model(tf.keras.Model):

    def __init__(self, units: int, dropout_rate: float, mask_value: float, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.masking = tf.keras.layers.Masking(mask_value=mask_value)
        self.lstm_1 = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(units=units, dropout=dropout_rate, recurrent_dropout=dropout_rate,
                                 return_sequences=True))
        self.lstm_2 = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(units=units, dropout=dropout_rate, recurrent_dropout=dropout_rate))
        self.dense = tf.keras.layers.Dense(units=units, activation=tf.keras.activations.relu)
        self.sigmoid = tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid)

    def call(self, inputs, training=None, mask=None):
        return self.sigmoid(self.dense(self.lstm_2(self.lstm_1(self.masking(inputs)))))


class CalibratedModel(tf.keras.Model):
    """
    See: https://ieeexplore.ieee.org/abstract/document/7376606
    """
    def __init__(self,
                 class_balanced_model: tf.keras.Model,
                 count_positive: int,
                 count_negative: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_balanced_model = class_balanced_model
        self.beta = tf.constant(count_positive / count_negative, dtype=tf.dtypes.float32)
        assert self.beta <= 1., 'calibration assumes more negative than positive examples'  # FIXME: generalize

    def call(self, inputs, training=None, mask=None):
        class_balanced_probability = self.class_balanced_model(inputs, training=training)
        return self.beta * class_balanced_probability / (1. - (1. - self.beta) * class_balanced_probability)
