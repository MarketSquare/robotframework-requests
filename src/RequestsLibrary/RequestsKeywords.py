import json
import sys

import robot
from requests.models import Response
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.asserts import assert_equal

from RequestsLibrary import utils, log
from RequestsLibrary.compat import PY3
from RequestsLibrary.exceptions import InvalidResponse, InvalidExpectedStatus
from RequestsLibrary.utils import is_file_descriptor, is_string_type


class WritableObject:
    """ HTTP stream handler """

    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)


class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()
        self.debug = 0

    # TODO maybe this should be a staticmethod
    @keyword("Status Should be")
    def status_should_be(self, expected_status, response, msg=None):
        """
        Fails if response status code is different than the expected.

        ``expected_status`` could be the code number as an integer or as string.
        But it could also be a named status code like 'ok', 'created', 'accepted' or
        'bad request', 'not found' etc.

        The ``response`` is the output of other requests keywords like ``Get Request``.

        A custom message ``msg`` can be added to work like built in keywords.
        """
        self._check_status(expected_status, response, msg)

    # TODO maybe this should be a staticmethod
    @keyword("Request Should Be Successful")
    def request_should_be_successful(self, response):
        """
        Fails if response status code is a client or server error (4xx, 5xx).

        The ``response`` is the output of other requests keywords like ``Get Request``.

        In case of failure an HTTPError will be automatically raised.
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

    def to_json(self, content, pretty_print=False):
        """ Convert a string to a JSON object

        ``content`` String content to convert into JSON

        ``pretty_print`` If defined, will output JSON is pretty print format
        """
        if PY3:
            if isinstance(content, bytes):
                content = content.decode(encoding='utf-8')
        if pretty_print:
            json_ = utils.json_pretty_print(content)
        else:
            json_ = json.loads(content)
        logger.info('To JSON using : content=%s ' % (content))
        logger.info('To JSON using : pretty_print=%s ' % (pretty_print))

        return json_

    def _common_request(
            self,
            method,
            session,
            uri,
            **kwargs):

        method_function = getattr(session, method)
        self._capture_output()

        resp = method_function(
            self._get_url(session, uri),
            params=utils.utf8_urlencode(kwargs.pop('params', None)),
            timeout=self._get_timeout(kwargs.pop('timeout', None)),
            cookies=self.cookies,
            verify=self.verify,
            **kwargs)

        log.log_request(resp)
        self._print_debug()
        session.last_resp = resp
        log.log_response(resp)

        data = kwargs.get('data', None)
        if is_file_descriptor(data):
            data.close()

        return resp

    @staticmethod
    def _check_status(expected_status, resp, msg=None):
        """
        Helper method to check HTTP status
        """
        if not isinstance(resp, Response):
            raise InvalidResponse(resp)
        if expected_status is None:
            resp.raise_for_status()
        else:
            if not is_string_type(expected_status):
                raise InvalidExpectedStatus(expected_status)
            if expected_status.lower() in ['any', 'anything']:
                return
            try:
                expected_status = int(expected_status)
            except ValueError:
                expected_status = utils.parse_named_status(expected_status)
            msg = '' if msg is None else '{} '.format(msg)
            msg = "{}Url: {} Expected status".format(msg, resp.url)
            assert_equal(resp.status_code, expected_status, msg)

    @staticmethod
    def _get_url(session, uri):
        """
        Helper method to get the full url
        """
        url = session.url
        if uri:
            slash = '' if uri.startswith('/') else '/'
            url = "%s%s%s" % (session.url, slash, uri)
        return url

    def _get_timeout(self, timeout):
        return float(timeout) if timeout is not None else self.timeout

    def _capture_output(self):
        if self.debug >= 1:
            self.http_log = WritableObject()
            sys.stdout = self.http_log

    def _print_debug(self):
        if self.debug >= 1:
            sys.stdout = sys.__stdout__  # Restore stdout
            if PY3:
                debug_info = ''.join(
                    self.http_log.content).replace(
                    '\\r',
                    '').replace(
                    '\'',
                    '')
            else:
                debug_info = ''.join(
                    self.http_log.content).replace(
                    '\\r',
                    '').decode('string_escape').replace(
                    '\'',
                    '')

            # Remove empty lines
            debug_info = "\n".join(
                [ll.rstrip() for ll in debug_info.splitlines() if ll.strip()])
            logger.debug(debug_info)
