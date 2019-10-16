import json
import copy
import types
import sys

import requests
from requests.sessions import merge_setting
from requests.cookies import merge_cookies
from requests.structures import CaseInsensitiveDict
import logging
from requests.packages.urllib3.util import Retry
import robot
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import importlib as importModule
from google.protobuf.json_format import MessageToJson, Parse

from RequestsLibrary.compat import httplib, urlencode, PY3

try:
    from requests_ntlm import HttpNtlmAuth
except ImportError:
    pass


class WritableObject:
    """ HTTP stream handler """

    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)


class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'
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
            logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.ERROR)
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.ERROR)
            requests_log.propagate = True
            if not verify:
                requests.packages.urllib3.disable_warnings()

        # verify can be a Boolean or a String
        if isinstance(verify, bool):
            s.verify = verify
        elif isinstance(verify, str) or isinstance(verify, unicode):
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
        self.verify = verify if self.builtin.convert_to_boolean(verify) != True else None

        s.url = url

        # Enable http verbosity
        if int(debug) >= 1:
            self.debug = int(debug)
            httplib.HTTPConnection.debuglevel = self.debug

        self._cache.register(session, alias=alias)
        return session

    def create_session(self,
                       alias,
                       url,
                       headers={},
                       cookies={},
                       auth=None,
                       timeout=None,
                       proxies=None,
                       verify=False,
                       debug=0,
                       max_retries=3,
                       backoff_factor=0.10,
                       disable_warnings=0,
                       retry_status_list=[],
                       retry_method_list=DEFAULT_RETRY_METHOD_LIST):
        """ Create Session: create a HTTP session to a server

        ``alias`` Robot Framework alias to identify the session

        ``url`` Base url of the server

        ``headers`` Dictionary of default headers

        ``cookies`` Dictionary of cookies

        ``auth`` List of username & password for HTTP Basic Auth

        ``timeout`` Connection timeout

        ``proxies`` Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` Whether the SSL cert will be verified. A CA_BUNDLE path can also be provided.

        ``debug`` Enable http verbosity option more information
                https://docs.python.org/2/library/httplib.html#httplib.HTTPConnection.set_debuglevel

        ``max_retries`` Number of maximum retries each connection should attempt.
                        By default it will retry 3 times in case of connection errors only.
                        A 0 value will disable any kind of retries regardless of other retry settings.
                        In case the number of retries is reached a retry exception is raised.

        ``disable_warnings`` Disable requests warning useful when you have large number of testcases

        ``backoff_factor`` Introduces a delay time between retries that is longer after each retry.
                           eg. if backoff_factor is set to 0.1
                           the sleep between attemps will be: 0.0, 0.2, 0.4
                           More info here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html

        ``retry_method_list`` List of uppercased HTTP method verbs where retries are allowed.
                              By default retries are allowed only on HTTP requests methods that are considered to be
                              idempotent (multiple requests with the same parameters end with the same state).
                              eg. set to ['POST', 'GET'] to retry only those kind of requests.

        ``retry_status_list`` List of integer HTTP status codes that, if returned, a retry is attempted.
                              eg. set to [502, 503] to retry requests if those status are returned.
                              Note that max_retries must be greater than 0.

        """
        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None

        logger.info('Creating Session using : alias=%s, url=%s, headers=%s, \
                    cookies=%s, auth=%s, timeout=%s, proxies=%s, verify=%s, \
                    debug=%s ' % (alias, url, headers, cookies, auth, timeout,
                                  proxies, verify, debug))
        return self._create_session(
            alias=alias,
            url=url,
            headers=headers,
            cookies=cookies,
            auth=auth,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            proxies=proxies,
            verify=verify,
            debug=debug,
            disable_warnings=disable_warnings,
            retry_status_list=retry_status_list,
            retry_method_list=retry_method_list)

    def create_custom_session(
            self,
            alias,
            url,
            auth,
            headers={},
            cookies={},
            timeout=None,
            proxies=None,
            verify=False,
            debug=0,
            max_retries=3,
            backoff_factor=0.10,
            disable_warnings=0,
            retry_status_list=[],
            retry_method_list=DEFAULT_RETRY_METHOD_LIST):
        """ Create Session: create a HTTP session to a server

        ``url`` Base url of the server

        ``alias`` Robot Framework alias to identify the session

        ``headers`` Dictionary of default headers

        ``cookies`` Dictionary of cookies

        ``auth`` A Custom Authentication object to be passed on to the requests library.
                http://docs.python-requests.org/en/master/user/advanced/#custom-authentication

        ``timeout`` Connection timeout

        ``proxies`` Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` Whether the SSL cert will be verified. A CA_BUNDLE path can also be provided.
                 Defaults to False.

        ``debug`` Enable http verbosity option more information
                https://docs.python.org/2/library/httplib.html#httplib.HTTPConnection.set_debuglevel

        ``max_retries`` Number of maximum retries each connection should attempt.
                        By default it will retry 3 times in case of connection errors only.
                        A 0 value will disable any kind of retries regardless of other retry settings.
                        In case the number of retries is reached a retry exception is raised.

        ``disable_warnings`` Disable requests warning useful when you have large number of testcases

        ``backoff_factor`` Introduces a delay time between retries that is longer after each retry.
                           eg. if backoff_factor is set to 0.1
                           the sleep between attemps will be: 0.0, 0.2, 0.4
                           More info here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html

        ``retry_method_list`` List of uppercased HTTP method verbs where retries are allowed.
                              By default retries are allowed only on HTTP requests methods that are considered to be
                              idempotent (multiple requests with the same parameters end with the same state).
                              eg. set to ['POST', 'GET'] to retry only those kind of requests.

        ``retry_status_list`` List of integer HTTP status codes that, if returned, a retry is attempted.
                              eg. set to [502, 503] to retry requests if those status are returned.
                              Note that max_retries must be greater than 0.
        """

        logger.info('Creating Custom Authenticated Session using : alias=%s, url=%s, headers=%s, \
                    cookies=%s, auth=%s, timeout=%s, proxies=%s, verify=%s, \
                    debug=%s ' % (alias, url, headers, cookies, auth, timeout,
                                  proxies, verify, debug))

        return self._create_session(
            alias=alias,
            url=url,
            headers=headers,
            cookies=cookies,
            auth=auth,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            proxies=proxies,
            verify=verify,
            debug=debug,
            disable_warnings=disable_warnings,
            retry_status_list=retry_status_list,
            retry_method_list=retry_method_list)

    def create_ntlm_session(
            self,
            alias,
            url,
            auth,
            headers={},
            cookies={},
            timeout=None,
            proxies=None,
            verify=False,
            debug=0,
            max_retries=3,
            backoff_factor=0.10,
            disable_warnings=0,
            retry_status_list=[],
            retry_method_list=DEFAULT_RETRY_METHOD_LIST):
        """ Create Session: create a HTTP session to a server

        ``url`` Base url of the server

        ``alias`` Robot Framework alias to identify the session

        ``headers`` Dictionary of default headers

        ``cookies`` Dictionary of cookies

        ``auth`` ['DOMAIN', 'username', 'password'] for NTLM Authentication

        ``timeout`` Connection timeout

        ``proxies`` Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` Whether the SSL cert will be verified. A CA_BUNDLE path can also be provided.
                 Defaults to False.

        ``debug`` Enable http verbosity option more information
                https://docs.python.org/2/library/httplib.html#httplib.HTTPConnection.set_debuglevel

        ``max_retries`` Number of maximum retries each connection should attempt.
                        By default it will retry 3 times in case of connection errors only.
                        A 0 value will disable any kind of retries regardless of other retry settings.
                        In case the number of retries is reached a retry exception is raised.

        ``disable_warnings`` Disable requests warning useful when you have large number of testcases

        ``backoff_factor`` Introduces a delay time between retries that is longer after each retry.
                           eg. if backoff_factor is set to 0.1
                           the sleep between attemps will be: 0.0, 0.2, 0.4
                           More info here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html

        ``retry_method_list`` List of uppercased HTTP method verbs where retries are allowed.
                              By default retries are allowed only on HTTP requests methods that are considered to be
                              idempotent (multiple requests with the same parameters end with the same state).
                              eg. set to ['POST', 'GET'] to retry only those kind of requests.

        ``retry_status_list`` List of integer HTTP status codes that, if returned, a retry is attempted.
                              eg. set to [502, 503] to retry requests if those status are returned.
                              Note that max_retries must be greater than 0.
        """
        if not HttpNtlmAuth:
            raise AssertionError('Requests NTLM module not loaded')
        elif len(auth) != 3:
            raise AssertionError('Incorrect number of authentication arguments'
                                 ' - expected 3, got {}'.format(len(auth)))
        else:
            ntlm_auth = HttpNtlmAuth('{}\\{}'.format(auth[0], auth[1]),
                                     auth[2])
            logger.info('Creating NTLM Session using : alias=%s, url=%s, \
                        headers=%s, cookies=%s, ntlm_auth=%s, timeout=%s, \
                        proxies=%s, verify=%s, debug=%s '
                        % (alias, url, headers, cookies, ntlm_auth,
                           timeout, proxies, verify, debug))

            return self._create_session(
                alias=alias,
                url=url,
                headers=headers,
                cookies=cookies,
                auth=ntlm_auth,
                timeout=timeout,
                max_retries=max_retries,
                backoff_factor=backoff_factor,
                proxies=proxies,
                verify=verify,
                debug=debug,
                disable_warnings=disable_warnings,
                retry_status_list=retry_status_list,
                retry_method_list=retry_method_list)

    def create_digest_session(
            self,
            alias,
            url,
            auth,
            headers={},
            cookies={},
            timeout=None,
            proxies=None, verify=False,
            debug=0,
            max_retries=3,
            backoff_factor=0.10,
            disable_warnings=0,
            retry_status_list=[],
            retry_method_list=DEFAULT_RETRY_METHOD_LIST):
        """ Create Session: create a HTTP session to a server

        ``url`` Base url of the server

        ``alias`` Robot Framework alias to identify the session

        ``headers`` Dictionary of default headers

        ``cookies`` Dictionary of cookies

        ``auth`` ['DOMAIN', 'username', 'password'] for NTLM Authentication

        ``timeout`` Connection timeout

        ``proxies`` Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` Whether the SSL cert will be verified. A CA_BUNDLE path can also be provided.
                 Defaults to False.

        ``debug`` Enable http verbosity option more information
                https://docs.python.org/2/library/httplib.html#httplib.HTTPConnection.set_debuglevel

        ``max_retries`` Number of maximum retries each connection should attempt.
                        By default it will retry 3 times in case of connection errors only.
                        A 0 value will disable any kind of retries regardless of other retry settings.
                        In case the number of retries is reached a retry exception is raised.

        ``disable_warnings`` Disable requests warning useful when you have large number of testcases

        ``backoff_factor`` Introduces a delay time between retries that is longer after each retry.
                           eg. if backoff_factor is set to 0.1
                           the sleep between attemps will be: 0.0, 0.2, 0.4
                           More info here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html

        ``retry_method_list`` List of uppercased HTTP method verbs where retries are allowed.
                              By default retries are allowed only on HTTP requests methods that are considered to be
                              idempotent (multiple requests with the same parameters end with the same state).
                              eg. set to ['POST', 'GET'] to retry only those kind of requests.

        ``retry_status_list`` List of integer HTTP status codes that, if returned, a retry is attempted.
                              eg. set to [502, 503] to retry requests if those status are returned.
                              Note that max_retries must be greater than 0.
        """
        digest_auth = requests.auth.HTTPDigestAuth(*auth) if auth else None

        return self._create_session(
            alias=alias,
            url=url,
            headers=headers,
            cookies=cookies,
            auth=digest_auth,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            proxies=proxies,
            verify=verify,
            debug=debug,
            disable_warnings=disable_warnings,
            retry_status_list=retry_status_list,
            retry_method_list=retry_method_list)

    def create_client_cert_session(
            self,
            alias,
            url,
            headers={},
            cookies={},
            client_certs=None,
            timeout=None,
            proxies=None,
            verify=False,
            debug=0,
            max_retries=3,
            backoff_factor=0.10,
            disable_warnings=0,
            retry_status_list=[],
            retry_method_list=DEFAULT_RETRY_METHOD_LIST):
        """ Create Session: create a HTTP session to a server

        ``url`` Base url of the server

        ``alias`` Robot Framework alias to identify the session

        ``headers`` Dictionary of default headers

        ``cookies`` Dictionary of cookies

        ``client_certs`` ['client certificate', 'client key'] PEM files containing the client key and certificate

        ``timeout`` Connection timeout

        ``proxies`` Dictionary that contains proxy urls for HTTP and HTTPS communication

        ``verify`` Whether the SSL cert will be verified. A CA_BUNDLE path can also be provided.
                 Defaults to False.

        ``debug`` Enable http verbosity option more information
                https://docs.python.org/2/library/httplib.html#httplib.HTTPConnection.set_debuglevel

        ``max_retries`` Number of maximum retries each connection should attempt.
                        By default it will retry 3 times in case of connection errors only.
                        A 0 value will disable any kind of retries regardless of other retry settings.
                        In case the number of retries is reached a retry exception is raised.

        ``disable_warnings`` Disable requests warning useful when you have large number of testcases

        ``backoff_factor`` Introduces a delay time between retries that is longer after each retry.
                           eg. if backoff_factor is set to 0.1
                           the sleep between attemps will be: 0.0, 0.2, 0.4
                           More info here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html

        ``retry_method_list`` List of uppercased HTTP method verbs where retries are allowed.
                              By default retries are allowed only on HTTP requests methods that are considered to be
                              idempotent (multiple requests with the same parameters end with the same state).
                              eg. set to ['POST', 'GET'] to retry only those kind of requests.

        ``retry_status_list`` List of integer HTTP status codes that, if returned, a retry is attempted.
                              eg. set to [502, 503] to retry requests if those status are returned.
                              Note that max_retries must be greater than 0.
        """

        logger.info('Creating Session using : alias=%s, url=%s, headers=%s, \
                    cookies=%s, client_certs=%s, timeout=%s, proxies=%s, verify=%s, \
                    debug=%s ' % (alias, url, headers, cookies, client_certs, timeout,
                                  proxies, verify, debug))

        session = self._create_session(
            alias=alias,
            url=url,
            headers=headers,
            cookies=cookies,
            auth=None,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            proxies=proxies,
            verify=verify,
            debug=debug,
            disable_warnings=disable_warnings,
            retry_status_list=retry_status_list,
            retry_method_list=retry_method_list)

        session.cert = tuple(client_certs)
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
            json_ = self._json_pretty_print(content)
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
            timeout=None,
            protobuf_response_type=None,
            protobuf_response_class_type=None):
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
        
        ``protobuf_response_type`` protobuf response module name

        ``protobuf_response_class_type`` protobuf response class name
        """
        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "get",
            session,
            uri,
            protobuf_response_type,
            protobuf_response_class_type,
            params=params,
            headers=headers,
            data=data,
            json=json,
            allow_redirects=redir,
            timeout=timeout)

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
            timeout=None,
            protobuf_request_type=None,
            protobuf_request_class_type=None,
            protobuf_response_type=None,
            protobuf_response_class_type=None):
        """ Send a POST request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the POST request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content
               or passed as such for multipart form data if ``files`` is also
                  defined

        ``json`` a value that will be json encoded
               and sent as POST data if files or data is not specified

        ``params`` url parameters to append to the uri

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to POST to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout

        ``protobuf_request_type`` protobuf request module name

        ``protobuf_request_class_type`` protobuf request class name

        ``protobuf_response_type`` protobuf response module name

        ``protobuf_response_class_type`` protobuf response class name
        """
        session = self._cache.switch(alias)
        if not files:
            data = self._format_data_according_to_header(session, data, headers, protobuf_request_type, protobuf_request_class_type)
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "post",
            session,
            uri,
            protobuf_response_type,
            protobuf_response_class_type,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)
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
            timeout=None,
            protobuf_request_type=None,
            protobuf_request_class_type=None,
            protobuf_response_type=None,
            protobuf_response_class_type=None):
        """ Send a PATCH request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PATCH request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as PATCH data
               or binary data that is sent as the raw body content

        ``json`` a value that will be json encoded
               and sent as PATCH data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``files`` a dictionary of file names containing file data to PATCH to the server

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``params`` url parameters to append to the uri

        ``timeout`` connection timeout

        ``protobuf_request_type`` protobuf request module name

        ``protobuf_request_class_type`` protobuf request class name

        ``protobuf_response_type`` protobuf response module name

        ``protobuf_response_class_type`` protobuf response class name
        """
        session = self._cache.switch(alias)
        data = self._format_data_according_to_header(session, data, headers, protobuf_request_type, protobuf_request_class_type)
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "patch",
            session,
            uri,
            protobuf_response_type,
            protobuf_response_class_type,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

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
            timeout=None,
            protobuf_request_type=None,
            protobuf_request_class_type=None,
            protobuf_response_type=None,
            protobuf_response_class_type=None):
        """ Send a PUT request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the PUT request to

        ``data`` a dictionary of key-value pairs that will be urlencoded
               and sent as PUT data
               or binary data that is sent as the raw body content

        ``json`` a value that will be json encoded
               and sent as PUT data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``params`` url parameters to append to the uri

        ``timeout`` connection timeout

        ``protobuf_request_type`` protobuf request module name

        ``protobuf_request_class_type`` protobuf request class name

        ``protobuf_response_type`` protobuf response module name

        ``protobuf_response_class_type`` protobuf response class name
        """
        session = self._cache.switch(alias)
        data = self._format_data_according_to_header(session, data, headers, protobuf_request_type, protobuf_request_class_type)
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "put",
            session,
            uri,
            protobuf_response_type,
            protobuf_response_class_type,
            data=data,
            json=json,
            params=params,
            files=files,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

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
            timeout=None,
            protobuf_request_type=None,
            protobuf_request_class_type=None,
            protobuf_response_type=None,
            protobuf_response_class_type=None):
        """ Send a DELETE request on the session object found using the
        given `alias`

        ``alias`` that will be used to identify the Session object in the cache

        ``uri`` to send the DELETE request to

        ``json`` a value that will be json encoded
               and sent as request data if data is not specified

        ``headers`` a dictionary of headers to use with the request

        ``allow_redirects`` Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.

        ``timeout`` connection timeout

        ``protobuf_request_type`` protobuf request module name

        ``protobuf_request_class_type`` protobuf request class name

        ``protobuf_response_type`` protobuf response module name

        ``protobuf_response_class_type`` protobuf response class name
        """
        session = self._cache.switch(alias)
        data = self._format_data_according_to_header(session, data, headers, protobuf_request_type, protobuf_request_class_type)
        redir = True if allow_redirects is None else allow_redirects

        response = self._common_request(
            "delete",
            session,
            uri,
            protobuf_response_type,
            protobuf_response_class_type,
            data=data,
            json=json,
            params=params,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

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
        """
        session = self._cache.switch(alias)
        redir = False if allow_redirects is None else allow_redirects
        response = self._common_request(
            "head",
            session,
            uri,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

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
        """
        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects
        response = self._common_request(
            "options",
            session,
            uri,
            headers=headers,
            allow_redirects=redir,
            timeout=timeout)

        return response

    def _common_request(
            self,
            method,
            session,
            uri,
            protobuf_response_type=None,
            protobuf_response_class_type=None,
            **kwargs):

        self._log_request(method, session, uri, **kwargs)
        method_function = getattr(session, method)

        self._capture_output()
        responseData = method_function(
            self._get_url(session, uri),
            params=self._utf8_urlencode(kwargs.pop('params', None)),
            timeout=self._get_timeout(kwargs.pop('timeout', None)),
            cookies=self.cookies,
            verify=self.verify,
            **kwargs)
        self._print_debug()

        resp = self._format_response_data_according_to_header(
            session, responseData, kwargs.get('header'), protobuf_response_type, protobuf_response_class_type)

        session.last_resp = resp
        self._log_response(method, resp)

        return resp

    def _get_url(self, session, uri):
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

    def _json_pretty_print(self, content):
        """
        Pretty print a JSON object

        ``content``  JSON object to pretty print
        """
        temp = json.loads(content)
        return json.dumps(
            temp,
            sort_keys=True,
            indent=4,
            separators=(
                ',',
                ': '))

    def _utf8_urlencode(self, data):
        if self._is_string_type(data):
            return data.encode('utf-8')

        if not isinstance(data, dict):
            return data

        utf8_data = {}
        for k, v in data.items():
            if self._is_string_type(v):
                v = v.encode('utf-8')
            utf8_data[k] = v
        return urlencode(utf8_data)

    def _format_data_according_to_header(self, session, data, headers, protobuf_request_type, protobuf_response_class_type):
        # Merged headers are already case insensitive
        headers = self._merge_headers(session, headers)

        if data is not None and headers is not None and 'Content-Type' in headers and headers['Content-Type'].find("application/x-protobuf") != -1:
            return self._convert_data_to_protobuf(data, protobuf_request_type, protobuf_response_class_type)

        if data is not None and headers is not None and 'Content-Type' in headers and not self._is_json(data):
            if headers['Content-Type'].find("application/json") != -1:
                if not isinstance(data, types.GeneratorType):
                    data = json.dumps(data)
            elif headers['Content-Type'].find("application/x-www-form-urlencoded") != -1:
                data = self._utf8_urlencode(data)
        else:
            data = self._utf8_urlencode(data)

        return data
    
    def _format_response_data_according_to_header(self, session, data, headers, protobuf_response_type, protobuf_response_class_type):
        headers = self._merge_headers(session, headers)

        if headers['Accept'].find("application/x-protobuf") != -1:
            return self._convert_protobuf_data_to_json(data, protobuf_response_type, protobuf_response_class_type)

        return data
    
    def _convert_protobuf_data_to_json(self, data, protobuf_type, protobuf_response_class_type):
        logger.debug('Protobuf object:' + str(data.content))

        protobufObject = self._get_protobuf_object(protobuf_type, protobuf_response_class_type)
        protobufObject.ParseFromString(data.content)

        for k, v in vars(data).items():
            if k == '_content':
                v = self._utf8_urlencode(MessageToJson(protobufObject))
            setattr(data, k, v)

        return data

    def _convert_data_to_protobuf(self, data, protobuf_type, protobuf_response_class_type):
        protobufObject = self._get_protobuf_object(protobuf_type, protobuf_response_class_type)

        Parse(data, protobufObject);
        stringSerilized = protobufObject.SerializeToString()

        logger.debug('Protobuf converted data:' + str(stringSerilized))

        return stringSerilized

    def _get_protobuf_object(self, protobuf_type, protobuf_response_class_type):
        module = importModule.import_module(protobuf_type + "_pb2")

        if protobuf_response_class_type is not None:
            return getattr(module, protobuf_response_class_type)()

        namespaceSplit = protobuf_type.split('.')
        return getattr(module, namespaceSplit[-1])()


    def _format_data_to_log_string_according_to_headers(self, session, data, headers):
        data_str = None
        # Merged headers are already case insensitive
        headers = self._merge_headers(session, headers)

        if data is not None and headers is not None and 'Content-Type' in headers:
            if (headers['Content-Type'].find("application/json") != -1) or \
                    (headers['Content-Type'].find("application/x-www-form-urlencoded") != -1):
                if isinstance(data, bytes):
                    data_str = data.decode('utf-8')
                else:
                    data_str = data
            else:
                data_str = "<" + headers['Content-Type'] + ">"

        return data_str

    def _log_request(
            self,
            method,
            session,
            uri,
            **kwargs):

        # TODO would be nice to add also the alias
        # TODO would be nice to pretty format the headers / json / data
        # TODO move in common the data formatting to have this as @staticmethod

        # kwargs might include: method, session, uri, params, files, headers,
        #                       data, json, allow_redirects, timeout
        args = kwargs.copy()
        args.pop('session', None)
        # This will log specific headers merged with session defined headers
        merged_headers = self._merge_headers(session, args.pop('headers', None))
        formatted_data = self._format_data_to_log_string_according_to_headers(session,
                                                                              args.pop('data', None),
                                                                              merged_headers)
        formatted_json = args.pop('json', None)
        method_log = '%s Request using : ' % method.upper()
        uri_log = 'uri=%s' % uri
        composed_log = method_log + uri_log
        for arg in args:
            composed_log += ', %s=%s' % (arg, kwargs.get(arg, None))
        logger.info(composed_log + '\n' +
                    'headers=%s \n' % merged_headers +
                    'data=%s \n' % formatted_data +
                    'json=%s' % formatted_json)

    @staticmethod
    def _log_response(method, response):
        logger.debug('%s Response : status=%s, reason=%s\n' % (method.upper(),
                                                               response.status_code,
                                                               response.reason) +
                     response.text)

    @staticmethod
    def _merge_headers(session, headers):
        if headers is None:
            headers = {}
        if session.headers is None:
            merged_headers = {}
        else:
            # Session headers are the default but local headers
            # have priority and can override values
            merged_headers = session.headers.copy()

        # Make sure merged_headers are CaseIsensitiveDict
        if not isinstance(merged_headers, CaseInsensitiveDict):
            merged_headers = CaseInsensitiveDict(merged_headers)

        merged_headers.update(headers)
        return merged_headers

    @staticmethod
    def _is_json(data):
        try:
            json.loads(data)
        except (TypeError, ValueError):
            return False
        return True

    @staticmethod
    def _is_string_type(data):
        if PY3 and isinstance(data, str):
            return True
        elif not PY3 and isinstance(data, unicode):
            return True
        return False
