import sys
import logging

import requests
from requests.cookies import merge_cookies
from requests.sessions import merge_setting
from requests.models import Response

from robot.api import logger
from robot.api.deco import keyword
from robot.utils.asserts import assert_equal

from RequestsLibrary import utils
from RequestsLibrary.compat import httplib, PY3, RetryAdapter
from .RequestsKeywords import RequestsKeywords
from RequestsLibrary.exceptions import InvalidResponse, InvalidExpectedStatus
from RequestsLibrary.utils import is_string_type

try:
    from requests_ntlm import HttpNtlmAuth
except ImportError:
    pass


class SessionKeywords(RequestsKeywords):
    DEFAULT_RETRY_METHOD_LIST = RetryAdapter.get_default_allowed_methods()

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
            retry = RetryAdapter(total=max_retries,
                                 backoff_factor=backoff_factor,
                                 status_forcelist=retry_status_list,
                                 allowed_methods=retry_method_list)
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

        s.url = url

        # Enable http verbosity
        if int(debug) >= 1:
            self.debug = int(debug)
            httplib.HTTPConnection.debuglevel = self.debug

        self._cache.register(session, alias=alias)
        return session

    @keyword("Create Session")
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

    @keyword("Create Client Cert Session")
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

    @keyword("Create Custom Session")
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

    @keyword("Create Digest Session")
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

    @keyword("Create Ntlm Session")
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
        try:
            HttpNtlmAuth
        except NameError:
            raise AssertionError('requests_ntlm module not installed')
        if len(auth) != 3:
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

    @keyword("Session Exists")
    def session_exists(self, alias):
        """Return True if the session has been already created

        ``alias`` that has been used to identify the Session object in the cache
        """
        try:
            self._cache[alias]
            return True
        except RuntimeError:
            return False

    @keyword("Delete All Sessions")
    def delete_all_sessions(self):
        """ Removes all the session objects """
        logger.info('Deleting All Sessions')

        self._cache.empty_cache()

    # TODO this is not covered by any tests
    @keyword("Update Session")
    def update_session(self, alias, headers=None, cookies=None):
        """Updates HTTP Session Headers and Cookies.

        Session will be identified using the ``alias`` name.
        Dictionary of ``headers`` and ``cookies`` to be updated and merged into session data.
        """
        session = self._cache.switch(alias)
        session.headers = merge_setting(headers, session.headers)
        session.cookies = merge_cookies(session.cookies, cookies)

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

    # FIXME might be broken we need a test for this
    def _get_timeout(self, timeout):
        return float(timeout) if timeout is not None else self.timeout

    def _capture_output(self):
        if self.debug >= 1:
            self.http_log = utils.WritableObject()
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
