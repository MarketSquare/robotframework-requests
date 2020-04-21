import json
import os

from requests import Session
from requests.utils import default_headers

from RequestsLibrary.log import format_data_to_log_string_according_to_headers


SCRIPT_DIR = os.path.dirname(__file__)


def test_format_with_data_and_headers_none():
    session = Session()
    data_str = format_data_to_log_string_according_to_headers(session, None, None)
    assert data_str is None


def test_format_with_headers_none():
    session = Session()
    data_str = format_data_to_log_string_according_to_headers(session, 'data', None)
    # TODO i think this is not the best thing
    assert data_str is None


def test_format_with_data_none():
    session = Session()
    data_str = format_data_to_log_string_according_to_headers(session, None, default_headers())
    assert data_str is None


def test_format_with_header_json_and_data_none():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/json"
    data_str = format_data_to_log_string_according_to_headers(session, None, headers)
    assert data_str is None


def test_format_with_header_json_and_data_json():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/json"
    data = json.dumps({'key': 'value'})
    data_str = format_data_to_log_string_according_to_headers(session, data, headers)
    assert data_str == data


def test_format_with_wrong_header_and_data_json():
    session = Session()
    headers = default_headers()
    headers['Misspelled'] = "text/xml"
    data = "<xml>text</xml>"
    data_str = format_data_to_log_string_according_to_headers(session, data, headers)
    # TODO this should change
    assert data_str is None


def test_format_with_binary_data():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/octet-stream"
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string_according_to_headers(session, data, headers)
    assert data_str == "<application/octet-stream>"


def test_format_with_utf_encoded_data():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/json"
    with open(os.path.join(SCRIPT_DIR, '../atests/data.json'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string_according_to_headers(session, data, headers)
    assert data_str.encode('utf-8') == data


def test_format_with_file_descriptor():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/octet-stream"
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data_str = format_data_to_log_string_according_to_headers(session, f, headers)
    assert data_str == repr(f)
