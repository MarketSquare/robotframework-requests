import pytest

from RequestsLibrary import RequestsLibrary
from utests import mock

try:
    from robot.api.types import Secret
    secret_type_supported = True
except (ImportError, ModuleNotFoundError):
    secret_type_supported = False


def test_get_session_secrets_flag_with_none_session():
    """Test _get_session_secrets_flag returns False for None session"""
    lib = RequestsLibrary()
    assert lib._get_session_secrets_flag(None) is False


def test_get_session_secrets_flag_for_session_without_secrets():
    """Test _get_session_secrets_flag returns False for session created without secrets"""
    lib = RequestsLibrary()
    session = lib.create_session('test', 'http://example.com')
    # Session created without secrets should return False
    assert lib._get_session_secrets_flag(session) is False


def test_get_session_secrets_flag_for_unknown_session():
    """Test _get_session_secrets_flag returns False for untracked session object"""
    lib = RequestsLibrary()
    # Create a session but don't register it
    import requests
    untracked_session = requests.Session()
    # Unknown session should return False
    assert lib._get_session_secrets_flag(untracked_session) is False


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_create_session_with_secrets_sets_flag():
    """Test that creating a session with secrets properly sets the flag"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')
    auth = ['user', secret_pwd]

    # Create session with secrets
    session = lib.create_session('test', 'http://example.com', auth=auth)

    # Verify secret flag is tracked
    assert lib._get_session_secrets_flag(session) is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_create_digest_session_with_secrets_sets_flag():
    """Test that creating a digest session with secrets properly sets the flag"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')
    auth = ['user', secret_pwd]

    # Create digest session with secrets
    session = lib.create_digest_session('test', 'http://example.com', auth=auth)

    # Verify secret flag is tracked
    assert lib._get_session_secrets_flag(session) is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_create_client_cert_session_with_secrets_sets_flag():
    """Test that creating a client cert session with secrets properly sets the flag"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')
    auth = ['user', secret_pwd]

    # Create client cert session with secrets
    session = lib.create_client_cert_session(
        'test', 'http://example.com',
        auth=auth,
        client_certs=('cert.pem', 'key.pem')
    )

    # Verify secret flag is tracked
    assert lib._get_session_secrets_flag(session) is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_common_request_with_session_secrets_sets_request_flag():
    """Test _common_request properly checks session secret flag and sets request flag"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')

    # Create session with secrets in auth
    session = lib.create_session('test', 'http://example.com', auth=['user', secret_pwd])

    # Mock the session.request to prevent actual HTTP call
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.text = ''
    mock_response.content = b''
    mock_response.url = 'http://example.com/test'
    session.request = mock.MagicMock(return_value=mock_response)

    # Make a request without any auth parameter
    lib._common_request('GET', session, '/test')

    # Verify _request_has_secrets is set to True due to session having secrets
    assert lib._request_has_secrets is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_common_request_without_session_secrets_does_not_set_request_flag():
    """Test _common_request doesn't set request flag when session has no secrets"""
    lib = RequestsLibrary()

    # Create session without secrets
    session = lib.create_session('test', 'http://example.com', auth=['user', 'plaintext'])

    # Mock the session.request to prevent actual HTTP call
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.text = ''
    mock_response.content = b''
    mock_response.url = 'http://example.com/test'
    session.request = mock.MagicMock(return_value=mock_response)

    # Make a request without any auth parameter
    lib._common_request('GET', session, '/test')

    # Verify _request_has_secrets is False
    assert lib._request_has_secrets is False


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_common_request_with_request_level_secrets():
    """Test _common_request sets flag when secrets are in request auth (not session)"""
    lib = RequestsLibrary()
    request_secret = Secret('request_password')

    # Create session without secrets
    session = lib.create_session('test', 'http://example.com')

    # Mock the session.request to prevent actual HTTP call
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.text = ''
    mock_response.content = b''
    mock_response.url = 'http://example.com/test'
    session.request = mock.MagicMock(return_value=mock_response)

    # Make a request with secrets in auth parameter
    lib._common_request('GET', session, '/test', auth=['user', request_secret])

    # Verify _request_has_secrets is True due to request auth having secrets
    assert lib._request_has_secrets is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_common_request_with_both_session_and_request_secrets():
    """Test _common_request with secrets in both session and request auth"""
    lib = RequestsLibrary()
    session_secret = Secret('session_pwd')
    request_secret = Secret('request_pwd')

    # Create session with secrets
    session = lib.create_session('test', 'http://example.com', auth=['user1', session_secret])

    # Mock the session.request to prevent actual HTTP call
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.text = ''
    mock_response.content = b''
    mock_response.url = 'http://example.com/test'
    session.request = mock.MagicMock(return_value=mock_response)

    # Make a request with different secrets in auth
    lib._common_request('GET', session, '/test', auth=['user2', request_secret])

    # Verify _request_has_secrets is True (secrets from both sources)
    assert lib._request_has_secrets is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_session_secrets_flag_persists_across_requests():
    """Test that session secret flag persists across multiple requests"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')

    # Create session with secrets
    session = lib.create_session('test', 'http://example.com', auth=['user', secret_pwd])

    # Mock the session.request
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.text = ''
    mock_response.content = b''
    mock_response.url = 'http://example.com/test'
    session.request = mock.MagicMock(return_value=mock_response)

    # Make first request
    lib._common_request('GET', session, '/test1')
    assert lib._request_has_secrets is True

    # Make second request
    lib._common_request('GET', session, '/test2')
    assert lib._request_has_secrets is True

    # Session should still have the flag set
    assert lib._get_session_secrets_flag(session) is True


def test_common_request_sessionless_with_no_secrets():
    """Test session-less request without secrets doesn't set flag"""
    lib = RequestsLibrary()

    # Mock requests.request for session-less call
    with mock.patch('requests.request') as mock_request:
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.text = ''
        mock_response.content = b''
        mock_response.url = 'http://example.com/test'
        mock_request.return_value = mock_response

        # Make session-less request with plain auth
        lib._common_request('GET', None, 'http://example.com/test', auth=['user', 'password'])

        # Should not have secrets flag set
        assert lib._request_has_secrets is False


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_common_request_sessionless_with_secrets():
    """Test session-less request with secrets sets flag"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')

    # Mock requests.request for session-less call
    with mock.patch('requests.request') as mock_request:
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.text = ''
        mock_response.content = b''
        mock_response.url = 'http://example.com/test'
        mock_request.return_value = mock_response

        # Make session-less request with secret auth
        lib._common_request('GET', None, 'http://example.com/test', auth=['user', secret_pwd])

        # Should have secrets flag set
        assert lib._request_has_secrets is True


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_multiple_sessions_with_different_secret_flags():
    """Test that multiple sessions can have different secret flags"""
    lib = RequestsLibrary()
    secret_pwd = Secret('mypassword')

    # Create session with secrets
    session1 = lib.create_session('session1', 'http://example1.com', auth=['user', secret_pwd])

    # Create session without secrets
    session2 = lib.create_session('session2', 'http://example2.com', auth=['user', 'plaintext'])

    # Verify flags are tracked independently
    assert lib._get_session_secrets_flag(session1) is True
    assert lib._get_session_secrets_flag(session2) is False


@pytest.mark.skipif(not secret_type_supported, reason="Requires Robot 7.4+")
def test_set_session_secrets_flag_directly():
    """Test _set_session_secrets_flag method directly"""
    lib = RequestsLibrary()
    session = lib.create_session('test', 'http://example.com')

    # Initially should be False
    assert lib._get_session_secrets_flag(session) is False

    # Set to True
    lib._set_session_secrets_flag(session, True)
    assert lib._get_session_secrets_flag(session) is True

    # Set back to False
    lib._set_session_secrets_flag(session, False)
    assert lib._get_session_secrets_flag(session) is False
