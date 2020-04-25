import json
import os

from requests import Request

from RequestsLibrary.log import format_data_to_log_string, log_request
from utests import SCRIPT_DIR
from utests import mock


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


@mock.patch('RequestsLibrary.log.logger')
def test_log_request(mocked_logger):
    request = Request(method='get', url='http://mock.rulezz')
    request = request.prepare()
    log_request(request)
    assert mocked_logger.info.call_args[0][0] == ("%s Request : " % request.method +
                                                  "url=%s \n " % request.url +
                                                  "path_url=%s \n " % request.path_url +
                                                  "headers=%s \n " % request.headers +
                                                  "body=%s \n " % request.body)

