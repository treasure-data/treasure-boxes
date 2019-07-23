import json
import os
import sys
import tarfile
from logging import DEBUG, StreamHandler, getLogger

import numpy

os.system(f"{sys.executable} -m pip install -U chainer")
os.system(f"{sys.executable} -m pip install -U pytd")

import chainer
import pytd.pandas_td as td

from chainer_utils import nets, nlp_utils

MODEL_URL = "https://workflow-example-public.s3.amazonaws.com/imdb_model.tar.gz"

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def setup_model(device, model_setup):
    setup = json.load(open(model_setup))
    logger.info(json.dumps(setup, indent=2) + "\n")

    vocab = json.load(open(setup["vocab_path"]))
    n_class = setup["n_class"]

    # Setup a model
    if setup["model"] == "rnn":
        Encoder = nets.RNNEncoder
    elif setup["model"] == "cnn":
        Encoder = nets.CNNEncoder
    elif setup["model"] == "bow":
        Encoder = nets.BOWMLPEncoder
    encoder = Encoder(
        n_layers=setup["layer"],
        n_vocab=len(vocab),
        n_units=setup["unit"],
        dropout=setup["dropout"],
    )
    model = nets.TextClassifier(encoder, n_class)
    chainer.serializers.load_npz(setup["model_path"], model)
    model.to_device(device)  # Copy the model to the device

    return model, vocab, setup


def run_batch(
    database, input_table, output_table, device, model, vocab, setup, batchsize=64
):
    def predict_batch(words_batch):
        xs = nlp_utils.transform_to_array(words_batch, vocab, with_label=False)
        xs = nlp_utils.convert_seq(xs, device=device, with_label=False)
        with chainer.using_config("train", False), chainer.no_backprop_mode():
            probs = model.predict(xs, softmax=True)

        # Note: Prediction labels are different from original Chainer example
        #       positive: 1, negative: 0
        answers = model.xp.argmax(probs, axis=1)
        scores = probs[model.xp.arange(answers.size), answers].tolist()

        return answers, scores

    td_api_key = os.environ["TD_API_KEY"]
    endpoint = os.environ["TD_API_SERVER"]

    logger.info("Connect to Treasure Data")

    con = td.connect()
    presto = td.create_engine(f"presto:{database}", con=con)

    logger.info("Fetch data from Treasure Data")
    test_df = td.read_td(
        f"""
        select
            rowid, sentence, sentiment, polarity
        from
            {input_table}
    """,
        presto,
    )

    sentences = test_df["sentence"].tolist()

    logger.info("Start prediction")
    batch = []
    predicted = []
    i = 1
    for sentence in sentences:
        text = nlp_utils.normalize_text(sentence)
        words = nlp_utils.split_text(text, char_based=setup["char_based"])
        batch.append(words)
        if len(batch) >= batchsize:
            _predicted, _ = predict_batch(batch)
            predicted.append(_predicted)
            batch = []
            logger.info(f"Predicted: {i}th batch. batch size {batchsize}")
            i += 1

    if batch:
        _predicted, _ = predict_batch(batch)
        predicted.append(_predicted)

    logger.info("Finish prediction")

    test_df["predicted_polarity"] = numpy.concatenate(predicted, axis=None)

    # Note: Train test split strategy is different from pre trained model and
    #       these tables so that the model includes test data since the model
    #       is trained by Chainer official example.
    #       This accuracy is just for a demo.
    #
    # accuracy = (test_df.polarity == test_df.predicted_polarity).value_counts()[
    #     1
    # ] / len(test_df)
    # print(f"Test set accuracy: {accuracy}")

    con2 = td.connect(apikey=td_api_key, endpoint=endpoint)

    td.to_td(
        test_df[["rowid", "predicted_polarity"]],
        f"{database}.{output_table}",
        con=con2,
        if_exists="replace",
        index=False,
    )

    logger.info("Upload completed")


def download_model():
    path = chainer.dataset.cached_download(MODEL_URL)
    tf = tarfile.open(path, "r")
    tf.extractall()
    return os.path.join("result", "args.json")


def predict_chainer(database, input_table, output_table, device_num=-1):
    device = chainer.get_device(device_num)
    device.use()

    model_setup = download_model()
    logger.info(f"model setup path: {model_setup}")
    model, vocab, setup = setup_model(device, model_setup)
    run_batch(
        database, input_table, output_table, device, model, vocab, setup, batchsize=64
    )


if __name__ == "__main__":
    predict_chainer(
        "sentiment", "movie_review_test_shuffled", "test_predicted_polarities_chainer"
    )
