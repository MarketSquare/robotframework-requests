import json
import os

from requests import Session
from requests.utils import default_headers

from RequestsLibrary.log import format_data_to_log_string


SCRIPT_DIR = os.path.dirname(__file__)


def test_format_with_data_and_headers_none():
    data_str = format_data_to_log_string(None)
    assert data_str is None


def test_format_with_data_json():
    data = json.dumps({'key': 'value'})
    data_str = format_data_to_log_string(data)
    assert data_str == repr(data)


def test_format_with_data_string():
    data = "<xml>text</xml>"
    data_str = format_data_to_log_string(data)
    assert data_str == repr(data)


def test_format_with_binary_data():
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string(data)
    assert data_str == repr(data)


def test_format_with_utf_encoded_data():
    with open(os.path.join(SCRIPT_DIR, '../atests/data.json'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string(data)
    assert data_str == repr(data)


def test_format_with_file_descriptor():
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data_str = format_data_to_log_string(f)
    assert data_str == repr(f)
