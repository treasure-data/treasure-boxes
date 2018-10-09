import os
import re
import csv

def convert_directory_to_csv(directory, polarity, out_file_path):
    data = {}
    data["sentence"] = []
    data["sentiment"] = []

    with open(out_file_path, "a") as csvfile:
        writer = csv.writer(csvfile)

        for file_path in os.listdir(directory):
            with open(os.path.join(directory, file_path), "r") as f:
                sentence = f.read()
                sentiment = re.match("\d+_(\d+)\.txt", file_path).group(1)
                writer.writerow([sentence, sentiment, str(polarity)])


def convert_dataset(directory):
    out_path = os.path.join("resources", "{}.csv".format(directory))

    with open(out_path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sentence", "sentiment", "polarity"])

    convert_directory_to_csv(os.path.join("resources", "aclImdb", directory, "pos"), 1, out_path)
    convert_directory_to_csv(os.path.join("resources", "aclImdb", directory, "neg"), 0, out_path)


def main():
    convert_dataset("train")
    convert_dataset("test")


if __name__ == '__main__':
    main()
