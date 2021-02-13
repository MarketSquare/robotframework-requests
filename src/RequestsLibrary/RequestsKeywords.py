import requests
import robot
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.asserts import assert_equal

from RequestsLibrary.compat import urljoin
from RequestsLibrary import utils, log
from RequestsLibrary.utils import is_file_descriptor


class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()
        self.debug = 0

    def _common_request(
            self,
            method,
            session,
            uri,
            **kwargs):

        if session:
            method_function = getattr(session, method)
        else:
            method_function = getattr(requests, method)

        self._capture_output()

        resp = method_function(
            self._get_url(session, uri),
            params=utils.utf8_urlencode(kwargs.pop('params', None)),
            timeout=self._get_timeout(kwargs.pop('timeout', None)),
            cookies=kwargs.pop('cookies', self.cookies),
            **kwargs)

        log.log_request(resp)
        self._print_debug()

        if session:
            session.last_resp = resp

        log.log_response(resp)

        data = kwargs.get('data', None)
        if is_file_descriptor(data):
            data.close()

        return resp

    @staticmethod
    def _get_url(session, uri):
        """
        Helper method to get the full url
        """
        if session:
            base = session.url
        else:
            base = ''
        url = urljoin(base, uri)
        return url

    @keyword("Status Should Be")
    def status_should_be(self, expected_status, response, msg=None):
        """
        Fails if response status code is different than the expected.

        ``expected_status`` could be the code number as an integer or as string.
        But it could also be a named status code like 'ok', 'created', 'accepted' or
        'bad request', 'not found' etc.

        ``response`` is the output of other requests keywords like `GET On Session`.

        In case of failure an HTTPError will be automatically raised.
        A custom failure message ``msg`` can be added like in built-in keywords.

        `* On Session` keywords (like `GET On Session`) already have an implicit assert mechanism, that by default,
        verifies the response status code.
        `Status Should Be` keyword can be useful to do an explicit assert in case of `* On Session` keyword with
        ``expected_status=anything`` to disable implicit assert.
        """
        # TODO add an example in documentation of GET On Session expected=any than assert

        self._check_status(expected_status, response, msg)

    @keyword("Request Should Be Successful")
    def request_should_be_successful(self, response):
        """
        Fails if response status code is a client or server error (4xx, 5xx).

        ``response`` is the output of other requests keywords like `GET On Session`.

        In case of failure an HTTPError will be automatically raised.
        A custom failure message ``msg`` can be added like in built-in keywords.

        For a more versatile assert keyword see `Status Should Be`.
        """
        self._check_status(None, response, msg=None)

    @staticmethod
    @keyword("Get File For Streaming Upload")
    def get_file_for_streaming_upload(path):
        """
        Opens and returns a file descriptor of a specified file to be passed as ``data`` parameter
        to other requests keywords.

        This allows streaming upload of large files without reading them into memory.

        File descriptor is binary mode and read only. Requests keywords will automatically close the file,
        if used outside this library it's up to the caller to close it.
        """
        return open(path, 'rb')

    @keyword('GET')
    def session_less_get(self, url, params=None,
                         expected_status=None, msg=None, **kwargs):
        response = self._common_request('get', None, url,
                                        params=params, **kwargs)
        self._check_status(expected_status, response, msg)
        return response
