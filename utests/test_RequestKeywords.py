import os
import pytest

from RequestsLibrary import RequestsLibrary
from utests import mock

from utests import SCRIPT_DIR


@pytest.fixture
def setup_keywords():
    keywords = RequestsLibrary()
    keywords.save_last_response = mock.MagicMock()
    return keywords


@pytest.fixture
def setup_session(setup_keywords):
    keywords = setup_keywords
    keywords.save_last_response = mock.MagicMock()
    session = keywords.create_session('alias', 'http://mocking.rules')
    # this prevents a real network call from being executed
    session.get = mock.MagicMock()
    return session


def test_common_request_file_descriptor_closing(setup_keywords,
                                                setup_session):
    with open(os.path.join(SCRIPT_DIR, '../atests/randombytes.bin'), 'rb') as f:
        setup_keywords._common_request('post', setup_session,
                                 'http://mocking.rules', data=f)
        assert f.closed is True

def test_common_request_stores_last_response(setup_keywords,
                                             setup_session):
    expected_class_id = setup_session.get.return_value.id
    setup_keywords._common_request('get', setup_session,
                             'http://mocking.rules')

    assert setup_keywords.save_last_response.call_args[0][0].id == expected_class_id
