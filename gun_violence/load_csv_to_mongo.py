import csv
import datetime
from itertools import chain, islice

import database


def parse(line):
    parts = line.split('||')
    data = dict()
    for p in parts:
        key, value = p.split('::')
        data[key] = value
    return data


def combine_dicts(d1, d2, d3):
    common_keys = set(d1).intersection(set(d2)).intersection(set(d3))
    return [[d1[key], d2[key], d3[key]] for key in common_keys]


def decode_row(row):
    try:
        participants = combine_dicts(
            parse(row['participant_age_group']),
            parse(row['participant_gender']),
            parse(row['participant_type']),
        )
        data = {
            'date': datetime.datetime.strptime(row['date'], '%Y-%m-%d'),
            'state': row['state'],
            'city': row['city_or_county'],
            'n_killed': int(row['n_killed']),
            'n_injured': int(row['n_injured']),
            'victim_age': ', '.join(set([p[0] for p in participants if p[2] == 'Victim'])),
            'victim_gender': ', '.join(set([p[1] for p in participants if p[2] == 'Victim'])),
            'suspect_age': ', '.join(set([p[0] for p in participants if p[2] != 'Victim'])),
            'suspect_gender': ', '.join(set([p[1] for p in participants if p[2] != 'Victim'])),
        }
        return data
    except:
        return None


def is_empty(foo):
    values = list(foo.values())
    res = None in values or '' in values
    return res


def filter_generator(rows):
    for row in rows:
        data = decode_row(row)
        if data and not is_empty(data):
            yield data


def chunk_generator(iterable, size=1000):
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, size - 1)))


if __name__ == '__main__':
    reader = csv.DictReader(open('data.csv', 'r', encoding='utf-8'))
    collection = database.collection()
    total = 0
    for chunk in chunk_generator(filter_generator(reader)):
        total += len(chunk)
        collection.insert_many(chunk)
        print(f'Всего записей записано в базу данных: {total}')
