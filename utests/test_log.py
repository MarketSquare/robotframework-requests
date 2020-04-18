from requests import Session
from requests.utils import default_headers
from RequestsLibrary.log import format_data_to_log_string_according_to_headers


def test_format_data_with_data_and_headers_none():
    session = Session()
    data = format_data_to_log_string_according_to_headers(session, None, None)
    assert data is None


def test_format_data_with_headers_none():
    session = Session()
    data = format_data_to_log_string_according_to_headers(session, 'data', None)
    assert data is None


def test_format_data_with_data_none():
    session = Session()
    data = format_data_to_log_string_according_to_headers(session, None, default_headers())
    assert data is None


def test_format_data_with_header_json_and_data_none():
    session = Session()
    headers = default_headers()
    headers['Content-Type'] = "application/json"
    data = format_data_to_log_string_according_to_headers(session, None, headers)
    assert data is None
