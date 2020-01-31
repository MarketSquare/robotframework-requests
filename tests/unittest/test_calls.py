import os
import sys

# Needed to support python 2.7
if sys.version_info >= (3, 3):
    from unittest import TestCase, mock
    from unittest.mock import patch
else:
    import mock
    from unittest import TestCase
    from mock import patch

# I hate it but I can't get the coverage report to work without it, must be before RequestsLibrary import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
import RequestsLibrary


lib = RequestsLibrary.RequestsLibrary()
HTTP_LOCAL_SERVER = 'http://localhost:5000'
sess_headers = {'content-type': False}
post_headers = {'Content-Type': 'application/json'}


class TestCalls(TestCase):
    def test_import_defaults(self):
        RequestsLibrary.RequestsLibrary()

    @patch('RequestsLibrary.RequestsLibrary._common_request')
    def test_post_request_with_empty_data(self, common_request):
        lib.create_session('http_server', HTTP_LOCAL_SERVER, sess_headers)
        lib.post_request('http_server', '/anything',  data="",  headers=post_headers)
        common_request.assert_called_with('post', mock.ANY, '/anything', allow_redirects=True, data='',
                                          files=None, headers=post_headers, json=None,
                                          params=None, timeout=None)
