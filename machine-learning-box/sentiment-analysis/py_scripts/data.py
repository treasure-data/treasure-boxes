import csv
import os
import re
import shutil
from urllib.request import urlopen


def convert_directory_to_csv(directory, polarity, out_file_path):
    with open(out_file_path, "a") as csvfile:
        writer = csv.writer(csvfile)

        for file_path in os.listdir(directory):
            with open(os.path.join(directory, file_path), "r") as f:
                sentence = f.read()
                sentiment = re.match(r"\d+_(\d+)\.txt", file_path).group(1)
                writer.writerow([sentence, sentiment, str(polarity)])


def convert_dataset(directory):
    out_path = os.path.join("resources", "{}.csv".format(directory))

    with open(out_path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sentence", "sentiment", "polarity"])

    convert_directory_to_csv(
        os.path.join("resources", "aclImdb", directory, "pos"), 1, out_path
    )
    convert_directory_to_csv(
        os.path.join("resources", "aclImdb", directory, "neg"), 0, out_path
    )


def load_directory_data(directory):
    import pandas as pd

    data = {}
    data["sentence"] = []
    data["sentiment"] = []

    for file_path in os.listdir(directory):
        with open(os.path.join(directory, file_path), "r") as f:
            data["sentence"].append(f.read())
            data["sentiment"].append(re.match(r"\d+_(\d+)\.txt", file_path).group(1))

    return pd.DataFrame.from_dict(data)


def load_dataset(directory):
    import pandas as pd

    pos_df = load_directory_data(os.path.join(directory, "pos"))
    neg_df = load_directory_data(os.path.join(directory, "neg"))
    pos_df["polarity"] = 1
    neg_df["polarity"] = 0

    return pd.concat([pos_df, neg_df]).sample(frac=1).reset_index(drop=True)


def upload_dataset(database, train_table, test_table):
    import pytd

    apikey = os.environ["TD_API_KEY"]
    apiserver = os.environ["TD_API_SERVER"]
    client = pytd.Client(database=database, apikey=apikey, endpoint=apiserver)

    if client.exists(database, train_table) and client.exists(database, test_table):
        print("Target database and tables exists. Skip")
        return True

    target_url = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    file_name = "aclImdb.tar.gz"
    print(f"Start downloading: {target_url}")
    response = urlopen(target_url)

    with open(file_name, "wb") as f:
        shutil.copyfileobj(response, f)
    print(f"Finished donwloading: {target_url} into {file_name}. Unpacking...")
    shutil.unpack_archive(file_name, "resources")

    print("Unpacked. Load as dataframe")
    train_df = load_dataset(os.path.join("resources", "aclImdb", "train"))
    test_df = load_dataset(os.path.join("resources", "aclImdb", "test"))

    print("Loaded. Upload to Treasure Data")
    client.create_database_if_not_exists(database)
    client.load_table_from_dataframe(train_df, train_table, if_exists="overwrite")
    client.load_table_from_dataframe(test_df, test_table, if_exists="overwrite")

    shutil.rmtree(os.path.join("resources"))
    os.remove(file_name)

    return True


def main():
    convert_dataset("train")
    convert_dataset("test")


if __name__ == "__main__":
    main()
