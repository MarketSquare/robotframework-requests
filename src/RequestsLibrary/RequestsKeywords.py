import copy
import json
import logging
import sys

import requests
import robot
from requests.cookies import merge_cookies
from requests.models import Response
from requests.packages.urllib3.util import Retry
from requests.sessions import merge_setting
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.asserts import assert_equal

from RequestsLibrary import utils, log
from RequestsLibrary.compat import httplib, PY3
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
    # FIXME REMOVE ME
    DEFAULT_RETRY_METHOD_LIST = list(copy.copy(Retry.DEFAULT_METHOD_WHITELIST))

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()
        self.debug = 0

    def _create_session(
            self,
            alias,
            url,
            headers,
            cookies,
            auth,
            timeout,
            proxies,
            verify,
            debug,
            max_retries,
            backoff_factor,
            disable_warnings,
            retry_status_list,
            retry_method_list):

        logger.debug('Creating session: %s' % alias)
        s = session = requests.Session()
        s.headers.update(headers)
        s.auth = auth if auth else s.auth
        s.proxies = proxies if proxies else s.proxies

        try:
            max_retries = int(max_retries)
            retry_status_list = [int(x) for x in retry_status_list] if retry_status_list else None
        except ValueError as err:
            raise ValueError("Error converting session parameter: %s" % err)

        if max_retries > 0:
            retry = Retry(total=max_retries,
                          backoff_factor=backoff_factor,
                          status_forcelist=retry_status_list,
                          method_whitelist=retry_method_list)
            http = requests.adapters.HTTPAdapter(max_retries=retry)
            https = requests.adapters.HTTPAdapter(max_retries=retry)

            # Replace the session's original adapters
            s.mount('http://', http)
            s.mount('https://', https)

        # Disable requests warnings, useful when you have large number of testcase
        # you will observe drastical changes in Robot log.html and output.xml files size
        if disable_warnings:
            # you need to initialize logging, otherwise you will not see anything from requests
            logging.basicConfig()
            logging.getLogger().setLevel(logging.ERROR)
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.ERROR)
            requests_log.propagate = True
            if not verify:
                requests.packages.urllib3.disable_warnings()

        # verify can be a Boolean or a String
        if isinstance(verify, bool):
            s.verify = verify
        elif utils.is_string_type(verify):
            if verify.lower() == 'true' or verify.lower() == 'false':
                s.verify = self.builtin.convert_to_boolean(verify)
            else:
                # String for CA_BUNDLE, not a Boolean String
                s.verify = verify
        else:
            # not a Boolean nor a String
            s.verify = verify

        # cant pass these into the Session anymore
        self.timeout = float(timeout) if timeout is not None else None
        self.cookies = cookies
        self.verify = verify if self.builtin.convert_to_boolean(verify) is not True else None

        s.url = url

        # Enable http verbosity
        if int(debug) >= 1:
            self.debug = int(debug)
            httplib.HTTPConnection.debuglevel = self.debug

        self._cache.register(session, alias=alias)
        return session

    def session_exists(self, alias):
        """Return True if the session has been already created

        ``alias`` that has been used to identify the Session object in the cache
        """
        try:
            self._cache[alias]
            return True
        except RuntimeError:
            return False

    def delete_all_sessions(self):
        """ Removes all the session objects """
        logger.info('Delete All Sessions')

        self._cache.empty_cache()

    def update_session(self, alias, headers=None, cookies=None):
        """Update Session Headers: update a HTTP Session Headers

        ``alias`` Robot Framework alias to identify the session

        ``headers`` Dictionary of headers merge into session
        """
        session = self._cache.switch(alias)
        session.headers = merge_setting(headers, session.headers)
        session.cookies = merge_cookies(session.cookies, cookies)

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

    def get_request(
            self,
            alias,
            uri,
            headers=None,
            data=None,
            json=None,
            params=None,
            allow_redirects=None,
            timeout=None):
        """ Send a GET request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the GET request to

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as GET data
               or binary data that is sent as the raw body content

        ``json`` a value that will be json encoded
               and sent as GET data if data is not specified

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "get",
            session,
            uri,
            params=params,
            headers=headers,
            data=data,
            json=json,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword("GET On Session")
    def get_on_session(self, alias, url, params=None,
                       expected_status=None, msg=None, **kwargs):
        """
        Sends a GET request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as dictionary (list of tuples or bytes)
        through the ``params``.

        By default the response should not have a status code with error values,
        the expected status could be modified using ``expected_status`` that works in the
        same way as the `Status Should Be` keyword.

        Other optional ``requests`` arguments can be passed using ``**kwargs``.
        """
        session = self._cache.switch(alias)
        response = self._common_request("get", session, url,
                                        params=params, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def post_request(
            self,
            alias,
            uri,
            data=None,
            json=None,
            params=None,
            headers=None,
            files=None,
            allow_redirects=None,
            timeout=None):
        """ Send a POST request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the POST request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content
               or passed as such for multipart form data if ``files`` is also defined
               or file descriptor retrieved by Get File For Streaming Upload

        ``json`` a value that will be json encoded
               and sent as POST data if files or data is not specified

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to POST to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        if not files:
            data = utils.format_data_according_to_header(session, data, headers)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "post",
            session,
            uri,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)
        return response

    @keyword('POST On Session')
    def post_on_session(self, alias, url, data=None, json=None,
                        expected_status=None, msg=None, **kwargs):
        """
        Sends a POST request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as dictionary (list of tuples or bytes)
        through the ``params``.

        By default the response should not have a status code with error values,
        the expected status could be modified using ``expected_status`` that works in the
        same way as the `Status Should Be` keyword.

        Other optional ``requests`` arguments can be passed using ``**kwargs``.
        """
        session = self._cache.switch(alias)
        response = self._common_request("post", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def patch_request(
            self,
            alias,
            uri,
            data=None,
            json=None,
            params=None,
            headers=None,
            files=None,
            allow_redirects=None,
            timeout=None):
        """ Send a PATCH request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PATCH request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as PATCH data
               or binary data that is sent as the raw body content
               or file descriptor retrieved by Get File For Streaming Upload

        ``json`` a value that will be json encoded
               and sent as PATCH data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to PATCH to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``params`` url parameters to append to the uri

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        data = utils.format_data_according_to_header(session, data, headers)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "patch",
            session,
            uri,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword('PATCH On Session')
    def patch_on_session(self, alias, url, data=None, json=None,
                         expected_status=None, msg=None, **kwargs):
        """
        Sends a PATCH request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as dictionary (list of tuples or bytes)
        through the ``params``.

        By default the response should not have a status code with error values,
        the expected status could be modified using ``expected_status`` that works in the
        same way as the `Status Should Be` keyword.

        Other optional ``requests`` arguments can be passed using ``**kwargs``.
        """
        session = self._cache.switch(alias)
        response = self._common_request("patch", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def put_request(
            self,
            alias,
            uri,
            data=None,
            json=None,
            params=None,
            files=None,
            headers=None,
            allow_redirects=None,
            timeout=None):
        """ Send a PUT request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PUT request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as PUT data
               or binary data that is sent as the raw body content
               or file descriptor retrieved by Get File For Streaming Upload

        ``json`` a value that will be json encoded
               and sent as PUT data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``params`` url parameters to append to the uri

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        data = utils.format_data_according_to_header(session, data, headers)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "put",
            session,
            uri,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword('PUT On Session')
    def put_on_session(self, alias, url, data=None, json=None,
                       expected_status=None, msg=None, **kwargs):
        """
        Sends a PUT request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as dictionary (list of tuples or bytes)
        through the ``params``.

        By default the response should not have a status code with error values,
        the expected status could be modified using ``expected_status`` that works in the
        same way as the `Status Should Be` keyword.

        Other optional ``requests`` arguments can be passed using ``**kwargs``.
        """
        session = self._cache.switch(alias)
        response = self._common_request("put", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def delete_request(
            self,
            alias,
            uri,
            data=None,
            json=None,
            params=None,
            headers=None,
            allow_redirects=None,
            timeout=None):
        """ Send a DELETE request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the DELETE request to

        ``json`` a value that will be json encoded
               and sent as request data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        data = utils.format_data_according_to_header(session, data, headers)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "delete",
            session,
            uri,
            data=data,
            json=json,
            params=params,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword('DELETE On Session')
    def delete_on_session(self, alias, url,
                          expected_status=None, msg=None, **kwargs):
        """

        Args:
            alias:
            url:
            expected_status:
            msg:
            **kwargs:

        Returns:

        """
        session = self._cache.switch(alias)
        response = self._common_request("delete", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def head_request(
            self,
            alias,
            uri,
            headers=None,
            allow_redirects=None,
            timeout=None):
        """ Send a HEAD request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the HEAD request to

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``headers`` a dictionary of headers to use with the request

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = False if allow_redirects is None else allow_redirects
        response = self._common_request(
            "head",
            session,
            uri,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword("HEAD On Session")
    def head_on_session(self, alias, url,
                        expected_status=None, msg=None, **kwargs):
        """
        Sends a HEAD request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the HTTP header from server about resource of the ``url``.

        By default the response should not have a status code with error values,
        the expected status could be modified using ``expected_status`` that works in the
        same way as the `Status Should Be` keyword.

        Other optional ``requests`` arguments can be passed using ``**kwargs``.
        """
        session = self._cache.switch(alias)
        response = self._common_request("head", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    def options_request(
            self,
            alias,
            uri,
            headers=None,
            allow_redirects=None,
            timeout=None):
        """ Send an OPTIONS request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the OPTIONS request to

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``headers`` a dictionary of headers to use with the request

        ``timeout`` connection timeout
        """
        session = self._cache.switch(alias)
        # XXX workaround to restore library default behaviour. Not needed in new keywords
        redir = True if allow_redirects is None else allow_redirects
        response = self._common_request(
            "options",
            session,
            uri,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    @keyword("OPTIONS On Session")
    def options_on_session(self, alias, url,
                           expected_status=None, msg=None, **kwargs):
        """
        Sends a OPTIONS request on a previously created HTTP Session.
        """
        session = self._cache.switch(alias)
        response = self._common_request("options", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

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
