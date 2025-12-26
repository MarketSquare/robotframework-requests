import os

import pytest
from requests import Session

from RequestsLibrary import RequestsLibrary
from RequestsLibrary.utils import is_file_descriptor, merge_headers, check_and_process_secrets
from utests import SCRIPT_DIR
from utests import mock

try:
    from robot.api.types import Secret
    secret_type_supported = True
except (ImportError, ModuleNotFoundError):
    secret_type_supported = False


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
    headers = {'Content-Type': 'test'}
    merged = merge_headers(session, headers)
    session.headers.update(headers)
    assert merged == session.headers


@pytest.fixture(scope='function')
def mocked_keywords():
    keywords = RequestsLibrary()
    keywords._cache = mock.MagicMock()
    keywords._common_request = mock.MagicMock()
    keywords._check_status = mock.MagicMock()
    return keywords


@mock.patch('RequestsLibrary.utils.logger')
def test_no_warn_if_url_passed_as_named(mocked_logger, mocked_keywords):
    mocked_keywords.get_on_session('alias', url='http://this.is.an.url')
    mocked_logger.warn.assert_not_called()


@mock.patch('RequestsLibrary.utils.logger')
def test_no_warn_if_url_passed_as_positional(mocked_logger, mocked_keywords):
    mocked_keywords.get_on_session('alias', 'http://this.is.an.url')
    mocked_logger.warn.assert_not_called()


@mock.patch('RequestsLibrary.utils.logger')
def test_warn_that_url_is_missing(mocked_logger, mocked_keywords):
    try:
        mocked_keywords.get_on_session(alias=None)
    except TypeError:
        pass
    mocked_logger.warn.assert_called()


def test_check_and_process_secrets_with_no_secrets():
    auth = ('user', 'password')
    processed_auth, has_secrets = check_and_process_secrets(auth)
    assert processed_auth == ('user', 'password')
    assert has_secrets is False


@pytest.mark.skipif(not secret_type_supported, reason="Running on pre-7.4 robot")
def test_check_and_process_secrets_with_secrets():
    secret_password = Secret('mypassword')
    auth = ('user', secret_password)
    processed_auth, has_secrets = check_and_process_secrets(auth)
    assert processed_auth == ('user', 'mypassword')
    assert has_secrets is True
    assert not isinstance(processed_auth[1], Secret)


@pytest.mark.skipif(not secret_type_supported, reason="Running on pre-7.4 robot")
def test_check_and_process_secrets_with_mixed_secrets():
    secret_user = Secret('myuser')
    secret_password = Secret('mypassword')
    auth = (secret_user, secret_password)
    processed_auth, has_secrets = check_and_process_secrets(auth)
    assert processed_auth == ('myuser', 'mypassword')
    assert has_secrets is True
    assert not isinstance(processed_auth[0], Secret)
    assert not isinstance(processed_auth[1], Secret)


def test_check_and_process_secrets_with_none():
    processed_auth, has_secrets = check_and_process_secrets(None)
    assert processed_auth is None
    assert has_secrets is False


def test_check_and_process_secrets_with_empty_list():
    processed_auth, has_secrets = check_and_process_secrets([])
    assert processed_auth == []
    assert has_secrets is False
