import io
import mimetypes
import os
import socket
import threading

import pytest
from requests import Request
from requests.utils import super_len
from urllib3.util.request import rewind_body, set_file_position

from RequestsLibrary import RequestsLibrary
from RequestsLibrary.utils import get_multipart_file_descriptors, is_multipart_encoder
from utests import SCRIPT_DIR
from utests import mock

DATA_JSON = os.path.join(SCRIPT_DIR, '../atests/data.json')
INDEX_HTML = os.path.join(SCRIPT_DIR, '../atests/index.html')


def create_multipart_data(fields=None, files=None, files_first=False):
    return RequestsLibrary().create_multipart_data(fields, files, files_first)


def guessed(filename):
    # mimetypes reads the Windows registry, so don't hardcode what it returns
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def close(encoder):
    for file_descriptor in get_multipart_file_descriptors(encoder):
        file_descriptor.close()


def test_multipart_fields_dictionary():
    encoder = create_multipart_data({'name': 'value', 'number': 1, 'settings': {'a': [1, 2]}})
    assert encoder.fields == [('name', 'value'), ('number', '1'), ('settings', '{"a": [1, 2]}')]


def test_multipart_fields_list_keeps_duplicates():
    encoder = create_multipart_data([('tag', 'one'), ['tag', 'two']])
    assert encoder.fields == [('tag', 'one'), ('tag', 'two')]


def test_multipart_files_dictionary_guesses_filename_and_content_type():
    encoder = create_multipart_data(files={'document': DATA_JSON})
    name, (filename, file_descriptor, content_type) = encoder.fields[0]
    close(encoder)
    assert name == 'document'
    assert filename == 'data.json'
    assert file_descriptor.name == DATA_JSON
    assert content_type == guessed('data.json')


def test_multipart_files_list_with_content_type_and_filename():
    encoder = create_multipart_data(files=[('attachments', DATA_JSON),
                                           ['attachments', INDEX_HTML, 'text/plain', 'renamed.txt']])
    close(encoder)
    assert [field[0] for field in encoder.fields] == ['attachments', 'attachments']
    assert encoder.fields[1][1][0] == 'renamed.txt'
    assert encoder.fields[1][1][2] == 'text/plain'


def test_multipart_files_dictionary_descriptor():
    encoder = create_multipart_data(files=[{'name': 'document', 'path': DATA_JSON, 'filename': 'other.bin'}])
    close(encoder)
    assert encoder.fields[0][1][0] == 'other.bin'
    assert encoder.fields[0][1][2] == guessed('other.bin')


def test_multipart_unknown_extension_defaults_to_octet_stream():
    encoder = create_multipart_data(files=[('file', DATA_JSON, None, 'no_extension')])
    close(encoder)
    assert encoder.fields[0][1][2] == 'application/octet-stream'


def test_multipart_fields_before_files():
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON})
    close(encoder)
    assert [field[0] for field in encoder.fields] == ['name', 'document']


def test_multipart_files_first():
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON}, files_first=True)
    close(encoder)
    assert [field[0] for field in encoder.fields] == ['document', 'name']


@pytest.mark.parametrize('files', [[('attachments', [DATA_JSON, INDEX_HTML])],
                                   {'attachments': [DATA_JSON, INDEX_HTML]}])
def test_multipart_list_of_paths_with_same_name(files):
    encoder = create_multipart_data(files=files)
    close(encoder)
    names = [(field[0], field[1][0]) for field in encoder.fields]
    assert names == [('attachments', 'data.json'), ('attachments', 'index.html')]


@pytest.mark.parametrize('fields', [['not a pair'], [('a', 'b', 'c')]])
def test_multipart_invalid_fields(fields):
    with pytest.raises(ValueError):
        create_multipart_data(fields)


@pytest.mark.parametrize('files', [['not a list'], [('name',)], [{'path': DATA_JSON}], [{'name': 'file'}]])
def test_multipart_invalid_files(files):
    with pytest.raises(ValueError):
        create_multipart_data(files=files)


def test_multipart_missing_file_closes_already_opened_files():
    opened = []
    real_open = open

    def tracking_open(*args, **kwargs):
        file_descriptor = real_open(*args, **kwargs)
        opened.append(file_descriptor)
        return file_descriptor

    with mock.patch('builtins.open', tracking_open):
        with pytest.raises(IOError):
            create_multipart_data(files=[('first', DATA_JSON), ('second', '/does/not/exist')])
    assert len(opened) == 1
    assert opened[0].closed


def test_multipart_without_requests_toolbelt():
    with mock.patch.dict('sys.modules', {'requests_toolbelt': None}):
        with pytest.raises(ImportError, match='robotframework-requests\\[multipart\\]'):
            create_multipart_data({'name': 'value'})


def test_is_multipart_encoder():
    encoder = create_multipart_data({'name': 'value'})
    assert is_multipart_encoder(encoder) is True
    assert is_multipart_encoder({'name': 'value'}) is False
    assert is_multipart_encoder(b'bytes') is False


def test_common_request_sets_multipart_content_type():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://mock.rulezz'
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON})
    with mock.patch('RequestsLibrary.RequestsKeywords.log'):
        keywords._common_request('POST', session, '/upload', data=encoder)
    headers = session.request.call_args[1]['headers']
    assert headers['content-type'] == encoder.content_type
    assert all(fd.closed for fd in get_multipart_file_descriptors(encoder))


def test_common_request_keeps_explicit_content_type():
    keywords = RequestsLibrary()
    session = mock.MagicMock()
    session.url = 'http://mock.rulezz'
    encoder = create_multipart_data({'name': 'value'})
    with mock.patch('RequestsLibrary.RequestsKeywords.log'):
        keywords._common_request('POST', session, '/upload', data=encoder,
                                 headers={'content-type': 'multipart/related'})
    assert session.request.call_args[1]['headers']['Content-Type'] == 'multipart/related'


def test_get_multipart_file_descriptors_without_fields():
    assert get_multipart_file_descriptors(mock.Mock(spec=['content_type', 'read'])) == []


def test_multipart_rewind_sends_the_same_bytes_again():
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON})
    first = encoder.read(10) + encoder.read()
    assert encoder.tell() == len(first) == encoder.len
    assert encoder.seek(0) == 0
    assert encoder.tell() == 0
    second = encoder.read()
    close(encoder)
    assert first == second


def test_multipart_can_only_be_rewound_to_its_start():
    encoder = create_multipart_data({'name': 'value'})
    with pytest.raises(io.UnsupportedOperation):
        encoder.seek(5)
    with pytest.raises(io.UnsupportedOperation):
        encoder.seek(0, io.SEEK_END)


def test_multipart_rewind_contract_used_by_urllib3_and_requests():
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON})
    expected = encoder.to_string()
    encoder.seek(0)
    assert super_len(encoder) == encoder.len
    position = set_file_position(encoder, None)
    assert position == 0
    encoder.read(100)
    rewind_body(encoder, position)
    body = encoder.read()
    close(encoder)
    assert body == expected


def test_multipart_is_prepared_by_requests_as_a_rewindable_stream():
    encoder = create_multipart_data({'name': 'value'}, {'document': DATA_JSON})
    expected = encoder.to_string()
    encoder.seek(0)
    prepared = Request('POST', 'http://mock.rulezz', data=encoder).prepare()
    # the body position is what requests uses to rewind the body on 307 / 308 redirects
    assert prepared._body_position == 0
    assert prepared.headers['Content-Length'] == str(len(expected))
    assert 'Transfer-Encoding' not in prepared.headers
    assert b''.join(encoder) == expected
    encoder.seek(0)
    assert b''.join(encoder) == expected
    close(encoder)


def _cut_first_connection_server(received):
    """Resets the first connection in the middle of the body, answers 200 to the next one."""
    server = socket.socket()
    server.bind(('127.0.0.1', 0))
    server.listen()

    def read_request(connection):
        data = b''
        while b'\r\n\r\n' not in data:
            data += connection.recv(65536)
        head, _, body = data.partition(b'\r\n\r\n')
        length = int([line.split(b':')[1] for line in head.split(b'\r\n')
                      if line.lower().startswith(b'content-length')][0])
        return body, length

    def serve():
        connection, _ = server.accept()
        body, length = read_request(connection)
        while len(body) < length // 2:
            body += connection.recv(65536)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
        connection.close()
        connection, _ = server.accept()
        body, length = read_request(connection)
        connection.settimeout(5)
        while len(body) < length:
            chunk = connection.recv(65536)
            if not chunk:
                break
            body += chunk
        received.append(body)
        connection.sendall(b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
        connection.close()
        server.close()

    threading.Thread(target=serve, daemon=True).start()
    return 'http://127.0.0.1:%d' % server.getsockname()[1]


def test_put_retried_after_connection_reset_sends_the_whole_body(tmp_path):
    large_file = tmp_path / 'large.bin'
    large_file.write_bytes(os.urandom(4 * 1024 * 1024))
    received = []
    keywords = RequestsLibrary()
    keywords.create_session('flaky', _cut_first_connection_server(received))
    encoder = create_multipart_data({'name': 'value'}, {'document': str(large_file)})
    expected = encoder.to_string()
    encoder.seek(0)
    with mock.patch('RequestsLibrary.RequestsKeywords.log'):
        keywords.put_on_session('flaky', '/upload', data=encoder)
    assert received == [expected]
