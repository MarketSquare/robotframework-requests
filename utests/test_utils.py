import os

from requests import Session

from RequestsLibrary.utils import is_file_descriptor, merge_headers
from utests import SCRIPT_DIR


def test_none():
    assert is_file_descriptor(None) is False


def test_is_not_file_descriptor():
    nf = 'a string'
    assert is_file_descriptor(nf) is False


def test_is_file_descriptor():
    with open(os.path.join(SCRIPT_DIR, './test_utils.py')) as fd:
        assert is_file_descriptor(fd) is True


def test_merge_headers_with_session_headers_only():
    session = Session()
    merged = merge_headers(session, None)
    assert merged == session.headers


def test_merge_headers_with_all_none():
    session = Session()
    session.headers = None
    merged = merge_headers(session, None)
    assert merged == {}


def test_merge_headers_with_all():
    session = Session()
    headers =  {'Content-Type': 'test'}
    merged = merge_headers(session, headers)
    session.headers.update(headers)
    assert merged == session.headers
