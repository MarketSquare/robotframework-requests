import os

from RequestsLibrary import RequestsLibrary
from utests import mock

from utests import SCRIPT_DIR


def test_common_request_file_descriptor_closing():
    keywords = RequestsLibrary()
    keywords.save_last_response = mock.MagicMock()
    session = keywords.create_session('alias', 'http://mocking.rules')
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        keywords._common_request('post', session,
                                 'http://mocking.rules', data=f)
        assert f.closed is True

def test_common_request_stores_last_response():
    keywords = RequestsLibrary()
    keywords.save_last_response = mock.MagicMock()
    session = keywords.create_session('alias', 'http://mocking.rules')
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    session.get.return_value = mock.MagicMock()
    expected_class_id = session.get.return_value.id

    keywords._common_request('get', session,
                             'http://mocking.rules')

    assert keywords.save_last_response.call_args[0][0].id == expected_class_id
