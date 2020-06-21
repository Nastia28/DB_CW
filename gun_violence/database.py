import csv
from itertools import chain, islice

import pymongo


def backup(url):
    filepath = 'backup.csv'
    data = collection(url).find()
    with open(filepath, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'state', 'city', 'n_killed', 'n_injured', 'victim_age',
                                               'victim_gender', 'suspect_age', 'suspect_gender'])
        writer.writeheader()
        for row in data:
            row.pop('_id')
            writer.writerow(row)


def restore(url):
    filepath = 'backup.csv'
    col = collection(url)
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for chunk in chunk_generator(reader):
            col.insert_many(chunk)


# 'mongodb://admin1:admin1@ds361998.mlab.com:61998/gun_violence?retryWrites=false'
def collection(url='mongodb://admin1:admin1@ds361998.mlab.com:61998/gun_violence?retryWrites=false'):
    client = pymongo.MongoClient(url)
    return client['gun_violence']['gun_cases']


def chunk_generator(iterable, size=1000):
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))
