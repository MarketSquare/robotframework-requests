import copy

import requests
from requests.packages.urllib3.util import Retry
from robot.api import logger

from .RequestsKeywords import RequestsKeywords

try:
    from requests_ntlm import HttpNtlmAuth
except ImportError:
    pass


class SessionKeywords(RequestsKeywords):
    DEFAULT_RETRY_METHOD_LIST = list(copy.copy(Retry.DEFAULT_METHOD_WHITELIST))

    # FIXME REMOVE ME
    def get_request_deprecated(self):
        pass

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
