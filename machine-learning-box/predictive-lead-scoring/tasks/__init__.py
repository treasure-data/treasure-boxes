import csv
import json
import re
from collections import OrderedDict


class TitleMappingGenerator(object):
    """Normalize contacts' titles so that they can be used as categorical variables.
    """

    def run(self):
        # load cluster definitions
        with open('resources/cluster_definitions.json') as f:
            self.cluster_definitions = json.loads(f.read(), object_pairs_hook=OrderedDict)

        # read original title data
        with open('resources/title.csv', newline='') as f:
            reader = csv.DictReader(f)
            titles = {}
            for row in reader:
                titles[row['title']] = row['words']

        # categorize & write to a mapping file
        with open('resources/title_mapping.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'role', 'job'])
            writer.writeheader()
            for raw_title, words in titles.items():
                writer.writerow(self.__categorize(raw_title, words))

    def __categorize(self, raw_title, words):
        # expand clipped words
        transforms = [
            ('sr', 'senior'),
            ('jr', 'junior'),
            ('ceo', 'chief,executive,officer'),
            ('coo', 'chief,operating,officer'),
            ('cto', 'chief,technology,officer'),
            ('cfo', 'chief,finance,officer'),
            ('cio', 'chief,information,officer'),
            ('cmo', 'chief,marketing,officer'),
            ('vp', 'vice,president'),
            ('assoc', 'associate'),
            ('mgr', 'manager')
        ]
        for src, dst in transforms:
            words = re.sub(src, dst, words)

        role = self.__find_category(words, self.cluster_definitions['role'], 'employee')
        job = self.__find_category(words, self.cluster_definitions['job'], 'others')

        return {'title': raw_title, 'role': role, 'job': job}

    def __find_category(self, words, cat2keywords, default):
        cat = default
        for cat_name, keywords in cat2keywords.items():
            found = [w for w in keywords if w in words]
            if len(found) != 0:
                cat = cat_name
                break
        return cat


if __name__ == '__main__':
    TitleMappingGenerator().run()
