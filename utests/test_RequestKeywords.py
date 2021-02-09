import os

from RequestsLibrary import RequestsLibrary
from utests import mock

from utests import SCRIPT_DIR


def build_mocked_session_common_request(alias='alias', url='http://mocking.rules',
                                        verify=None, cookies={}):
    keywords = RequestsLibrary()
    session = keywords.create_session(alias, url, verify=verify, cookies=cookies)
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    return session, keywords._common_request


def test_common_request_file_descriptor_closing():
    session, m_common_request = build_mocked_session_common_request()
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        m_common_request('get', session,
                         'http://mocking.rules', data=f)
        assert f.closed is True


def test_common_request_verify_override_true():
    session, m_common_request = build_mocked_session_common_request(verify=False)
    m_common_request('get', session, '/', verify=True)
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={}, verify=True)
    assert session.verify is False


def test_common_request_verify_override_false():
    session, m_common_request = build_mocked_session_common_request(verify=True)
    m_common_request('get', session, '/', verify=False)
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={}, verify=False)
    assert session.verify is True


def test_common_request_verify_true_default():
    session, m_common_request = build_mocked_session_common_request(verify=True)
    m_common_request('get', session, '/')
    assert session.verify is True
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={})


def test_common_request_verify_false_default():
    session, m_common_request = build_mocked_session_common_request(verify=False)
    m_common_request('get', session, '/')
    assert session.verify is False
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={})


def test_common_request_with_cookies_override():
    session, m_common_request = build_mocked_session_common_request()
    m_common_request('get', session, '/', cookies={'a': 1, 'b': 2})
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={'a': 1, 'b': 2})


def test_common_request_with_cookies_override_default():
    session, m_common_request = build_mocked_session_common_request(cookies={'a': 1, 'b': 2})
    m_common_request('get', session, '/', cookies={'a': 3, 'b': 4})
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={'a': 3, 'b': 4})


def test_common_request_with_cookies_default_only():
    session, m_common_request = build_mocked_session_common_request(cookies={'a': 1, 'b': 2})
    m_common_request('get', session, '/')
    session.get.assert_called_with('http://mocking.rules/', params=None,
                                   timeout=None, cookies={'a': 1, 'b': 2})
