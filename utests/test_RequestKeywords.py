import os

from RequestsLibrary import RequestsLibrary
from utests import mock

from utests import SCRIPT_DIR


def build_mocked_session_common_request(alias='alias', url='http://mocking.rules',
                                        verify=None):
    keywords = RequestsLibrary()
    session = keywords.create_session(alias, url, verify=verify)
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    return session, keywords._common_request


def test_common_request_file_descriptor_closing():
    session, m_common_request = build_mocked_session_common_request()
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        m_common_request('get', session,
                         'http://mocking.rules', data=f)
        assert f.closed is True


def test_common_request_verify_overwrite_true():
    session, m_common_request = build_mocked_session_common_request(verify=False)
    m_common_request('get', session, '/', verify=True)
    session.get.assert_called_with('http://mocking.rules/', cookies={}, params=None,
                                   timeout=None, verify=True)


def test_common_request_verify_overwrite_false():
    session, m_common_request = build_mocked_session_common_request(verify=True)
    m_common_request('get', session, '/', verify=False)
    session.get.assert_called_with('http://mocking.rules/', cookies={}, params=None,
                                   timeout=None, verify=False)


def test_common_request_verify_true_default():
    session, m_common_request = build_mocked_session_common_request(verify=True)
    m_common_request('get', session, '/')
    assert session.verify
    session.get.assert_called_with('http://mocking.rules/', cookies={}, params=None,
                                   timeout=None)


def test_common_request_verify_false_default():
    session, m_common_request = build_mocked_session_common_request(verify=False)
    m_common_request('get', session, '/')
    assert not session.verify
    session.get.assert_called_with('http://mocking.rules/', cookies={}, params=None,
                                   timeout=None)
