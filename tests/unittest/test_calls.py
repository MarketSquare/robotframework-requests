from unittest import TestCase, mock
from unittest.mock import patch
import RequestsLibrary

lib = RequestsLibrary.RequestsLibrary()
HTTP_LOCAL_SERVER = 'http://localhost:5000'
sess_headers = {'content-type': False}
post_headers = {'Content-Type': 'application/json'}


class TestCalls(TestCase):
    @patch('RequestsLibrary.RequestsLibrary._common_request')
    def test_post_request_with_empty_data(self, common_request):
        lib.create_session('http_server', HTTP_LOCAL_SERVER, sess_headers)
        lib.post_request('http_server', '/anything',  data="",  headers=post_headers)
        common_request.assert_called_with('post', mock.ANY, '/anything', allow_redirects=True, data='',
                                          files=None, headers={'Content-Type': 'application/json'}, json=None, 
                                          params=None, timeout=None)
