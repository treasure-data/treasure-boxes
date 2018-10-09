import os


def get_predictions(estimator, input_fn):
    return [x["class_ids"][0] for x in estimator.predict(input_fn=input_fn)]


def run():
    # Original code is published at official document of TensorFlow under Apache License Version 2.0
    # https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub

    # FIXME: Need to create an image including pandas-td by default
    os.system("pip install pandas-td tensorflow_hub")

    import tensorflow as tf
    import tensorflow_hub as hub
    import pandas_td as td

    con = td.connect(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])
    presto = td.create_engine('presto:sentiment', con=con)

    train_df = td.read_td("""
        select
            rowid, sentence, sentiment, polarity
        from
            movie_review_train_shuffled
    """, presto)

    test_df = td.read_td("""
        select
            rowid, sentence, sentiment, polarity
        from
            movie_review_test_shuffled    
    """, presto)

    # Shuffle has been done by HiveQL in the shuffle task
    # train_df = train_df.sample(frac=1).reset_index(drop=True)

    with tf.Session(graph=tf.Graph()) as sess:
        train_input_fn = tf.estimator.inputs.pandas_input_fn(
            train_df, train_df["polarity"], num_epochs=None, shuffle=True)

        embedded_text_feature_column = hub.text_embedding_column(
            key="sentence",
            module_spec="https://tfhub.dev/google/nnlm-en-dim128/1")

        estimator = tf.estimator.DNNClassifier(
            hidden_units=[500, 100],
            feature_columns=[embedded_text_feature_column],
            n_classes=2,
            optimizer=tf.train.AdamOptimizer(learning_rate=0.003)
        )

        estimator.train(input_fn=train_input_fn, steps=1000)

        predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
            train_df, train_df["polarity"], shuffle=False)

        predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
            test_df, test_df["polarity"], shuffle=False)

        # TODO: export TF model on S3
        # tf.saved_model.simple_save(sess,
        #                           "./tfmodel",
        #                           inputs=)

        train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
        test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)
        print("Training set accuracy: {accuracy}".format(**train_eval_result))
        print("Test set accuracy: {accuracy}".format(**test_eval_result))

        results = get_predictions(estimator, predict_test_input_fn)

    test_df['predicted_polarity'] = results

    td.to_td(
        test_df[['rowid', 'predicted_polarity']], 'sentiment.test_predicted_polarities', con=con,
        if_exists='replace', index=False)


if __name__ == '__main__':
    run()
