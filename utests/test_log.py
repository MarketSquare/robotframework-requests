import json
import os

from requests import Request

from RequestsLibrary.log import format_data_to_log_string, log_request, log_response
from utests import SCRIPT_DIR
from utests import mock


def test_format_with_data_and_headers_none():
    data_str = format_data_to_log_string(None)
    assert data_str is None


def test_format_with_data_json():
    data = json.dumps({'key': 'value'})
    data_str = format_data_to_log_string(data)
    assert data_str == data


def test_format_with_data_string():
    data = "<xml>text</xml>"
    data_str = format_data_to_log_string(data)
    assert data_str == data


def test_format_with_binary_data():
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string(data)
    assert data_str == data


def test_format_with_utf_encoded_data():
    with open(os.path.join(SCRIPT_DIR, '../atests/data.json'), 'rb') as f:
        data = f.read()
    data_str = format_data_to_log_string(data)
    assert data_str == data


def test_format_with_file_descriptor():
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        data_str = format_data_to_log_string(f)
        assert data_str == repr(f)


@mock.patch('RequestsLibrary.log.logger')
def test_log_request(mocked_logger):
    request = Request(method='get', url='http://mock.rulezz')
    request = request.prepare()
    response = mock.MagicMock()
    response.history = []
    response.request = request
    log_request(response)
    assert mocked_logger.info.call_args[0][0] == ("%s Request : " % request.method +
                                                  "url=%s \n " % request.url +
                                                  "path_url=%s \n " % request.path_url +
                                                  "headers=%s \n " % request.headers +
                                                  "body=%s \n " % request.body)


@mock.patch('RequestsLibrary.log.logger')
def test_log_request_with_redirect(mocked_logger):
    request = Request(method='get', url='http://mock.rulezz/redirected')
    request = request.prepare()
    original = Request(method='get', url='http://mock.rulezz/original')
    original = original.prepare()
    response = mock.MagicMock()
    response.request = request
    response0 = mock.MagicMock()
    response0.request = original
    response.history = [response0, mock.MagicMock]
    log_request(response)
    assert mocked_logger.info.call_args[0][0] == ("%s Request : " % request.method +
                                                  "url=%s (redirected) \n " % response.history[0].request.url +
                                                  "path_url=%s \n " % response.history[0].request.path_url +
                                                  "headers=%s \n " % request.headers +
                                                  "body=%s \n " % request.body)


@mock.patch('RequestsLibrary.log.logger')
def test_log_response(mocked_logger):
    response = mock.MagicMock()
    response.url = 'http://mock.rulezz'
    response.request.method = 'GET'
    response.status_code = 200
    response.reason = 'OK'
    response.text = "<html>body</html>"
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == ("%s Response : url=%s \n " % (response.request.method.upper(),
                                                                                 response.url) +
                                                   "status=%s, reason=%s \n " % (response.status_code,
                                                                                 response.reason) +
                                                   "body=%s \n " % response.text)


def test_format_data_to_log_string_truncated_1():
    data = ''
    for i in range(0, 10000):
        data = data + str(i)
    truncated = format_data_to_log_string(data, 9999)
    assert truncated == data[:9999] + '... (set the log level to DEBUG or TRACE to see the full content)'


def test_format_data_to_log_string_truncated_2():
    data = ''
    for i in range(0, 10):
        data = data + str(i)
    truncated = format_data_to_log_string(data, 0)
    assert truncated == '... (set the log level to DEBUG or TRACE to see the full content)'


def test_format_data_to_log_string_truncated_3():
    data = ''
    for i in range(0, 10):
        data = data + str(i)
    truncated = format_data_to_log_string(data, 10)
    assert truncated == data


@mock.patch('RequestsLibrary.log.logging')
def test_format_data_not_truncate_debug_level(mocked_logger):
    data = ''
    for i in range(0, 100001):
        data = data + str(i)
    mocked_logger.getLogger().level = 10
    truncated = format_data_to_log_string(data)
    assert truncated == data


@mock.patch('RequestsLibrary.log.logging')
def test_format_data_not_truncate_trace_level(mocked_logger):
    data = ''
    for i in range(0, 100001):
        data = data + str(i)
    mocked_logger.getLogger().level = 0
    truncated = format_data_to_log_string(data)
    assert truncated == data


@mock.patch('RequestsLibrary.log.logging')
def test_format_data_truncate_info_level(mocked_logger):
    data = ''
    for i in range(0, 100001):
        data = data + str(i)
    mocked_logger.getLogger().level = 20
    truncated = format_data_to_log_string(data)
    assert truncated == data[:10000] + '... (set the log level to DEBUG or TRACE to see the full content)'
