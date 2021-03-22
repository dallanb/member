import base64
import logging
import uuid as UUID
from io import BytesIO
from itertools import groupby
from time import time

from src import app


def generate_hash(items):
    frozen = frozenset(items)
    return hash(frozen)


def time_now():
    return int(time() * 1000.0)


def add_years(t, years=0):
    return t + 31104000000 * years


def generate_uuid():
    return UUID.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1]


def allowed_file(filename):
    return file_extension(filename) in app.config["ALLOWED_EXTENSIONS"]


def s3_object_name(filename):
    return f"{app.config['S3_FILEPATH']}{filename}"


def get_image_data(file):
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    return BytesIO(base64.b64decode(image_data))


# provided a hash of contest participants this method will find the participant property with the lowest score field
def find_lowest_scoring_participant(participants):
    return min(participants.values(), key=lambda x: x['score'])


def sort_lowest_scoring_participant(participants):
    return sorted(participants.values(), key=lambda x: x['score'])


def has_tie(sorted_participants):
    if len(sorted_participants) > 1:
        if sorted_participants[0]['score'] == sorted_participants[1]['score']:
            return True
    return False

