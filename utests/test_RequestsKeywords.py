from RequestsLibrary import RequestsLibrary
from utests import mock


# @mock.patch('RequestsLibrary.RequestsKeywords.requests.get')
# def test_common_request_none_session(mocked_get):
#     keywords = RequestsLibrary.RequestsKeywords()
#     keywords._common_request('get', None, 'http://mock.rules')
#     mocked_get.assert_called_with('http://mock.rules')


def test_get_url_with_none_session():
    keywords = RequestsLibrary()
    url = keywords._get_url(None, 'http://thisisa.url')
    assert url == 'http://thisisa.url'


def test_get_url_with_base():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com'
    url = keywords._get_url(session, '')
    assert url == 'http://www.domain.com'


def test_get_url_with_base_endpoint():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com'
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_base_slash_endpoint_pre():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com/'
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_base_slash_endpoint_post():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com'
    url = keywords._get_url(session, '/endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_base2trailing_endpoint():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com//'
    url = keywords._get_url(session, 'endpoint')
    assert url == 'http://www.domain.com/endpoint'


def test_get_url_with_base_slash_endpoint_2trailing():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com'
    url = keywords._get_url(session, '/endpoint//')
    assert url == 'http://www.domain.com/endpoint//'


def test_get_url_with_url_override_base():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://www.domain.com'
    url = keywords._get_url(session, 'https://new.domain.com')
    assert url == 'https://new.domain.com'
