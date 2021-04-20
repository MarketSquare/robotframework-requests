import sys

import pytest

from RequestsLibrary import RequestsLibrary
from utests import mock


# @mock.patch('RequestsLibrary.RequestsKeywords.requests.get')
# def test_common_request_none_session(mocked_get):
#     keywords = RequestsLibrary.RequestsKeywords()
#     keywords._common_request('get', None, 'http://mock.rules')
#     mocked_get.assert_called_with('http://mock.rules')

def build_mocked_session_keywords(url=''):
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = url
    return session, keywords


def test_get_url_with_none_session():
    keywords = RequestsLibrary()
    url = keywords._get_url(None, 'http://thisisa.url')
    assert url == 'http://thisisa.url'


def test_get_url_with_session_url_only():
    session, keywords = build_mocked_session_keywords('http://www.domain.com')
    url = keywords._get_url(session, '')
    assert url == 'http://www.domain.com'


def test_get_url_with_session_url_and_uri_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com')
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_session_url_slash_and_uri_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com/')
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_session_url_and_uri_slash_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com')
    url = keywords._get_url(session, '/endpoint')
    assert url == 'http://www.domain.com/endpoint'

# breaking change with 0.8 :( #329
def test_get_url_with_session_url_path_and_uri_root_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com/path')
    url = keywords._get_url(session, '/endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_session_url_path_and_uri_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com/path/')
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/path/endpoint'


@pytest.mark.skipif(sys.version_info < (3, 0), reason="different urljoin handling of double slash")
def test_get_url_with_base2trailing_endpoint():
    session, keywords = build_mocked_session_keywords('http://www.domain.com//')
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_base_slash_endpoint_2trailing():
    session, keywords = build_mocked_session_keywords('http://www.domain.com')
    url = keywords._get_url(session, '/endpoint//')
    assert url == 'http://www.domain.com/endpoint//'


def test_get_url_with_url_override_base():
    session, keywords = build_mocked_session_keywords('http://www.domain.com')
    url = keywords._get_url(session, 'https://new.domain.com')
    assert url == 'https://new.domain.com'
