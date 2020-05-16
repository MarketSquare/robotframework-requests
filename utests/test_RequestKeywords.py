import os

from utests import mock

from RequestsLibrary.RequestsKeywords import RequestsKeywords
from utests import SCRIPT_DIR


def test_common_request_file_descriptor_closing():
    keywords = RequestsKeywords()
    session = keywords.create_session('alias', 'http://mocking.rules')
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        keywords._common_request('get', session,
                                 'http://mocking.rules', data=f)
        assert f.closed is True
