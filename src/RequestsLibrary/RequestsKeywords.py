import requests
import robot
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from RequestsLibrary.compat import urljoin
from RequestsLibrary import utils, log
from RequestsLibrary.utils import is_file_descriptor


class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()
        self.debug = 0
        # The following variables are related to session but used in _common_request :(
        self.timeout = None
        self.cookies = None
        self.last_response = None

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
            timeout=self._get_timeout(kwargs.pop('timeout', None)),
            cookies=kwargs.pop('cookies', self.cookies),
            **kwargs)

        log.log_request(resp)
        self._print_debug()

        log.log_response(resp)

        self.last_response = resp

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
    def status_should_be(self, expected_status, response=None, msg=None):
        """
        Fails if response status code is different than the expected.

        ``expected_status`` could be the code number as an integer or as string.
        But it could also be a named status code like 'ok', 'created', 'accepted' or
        'bad request', 'not found' etc.

        ``response`` is the output of other requests keywords like `GET` or `GET On Session`.
        If omitted the last response will be used.

        In case of failure an HTTPError will be automatically raised.
        A custom failure message ``msg`` can be added like in built-in keywords.

        New requests keywords like `GET` or `GET On Session` (starting from 0.8 version) already have an implicit assert
        mechanism that, by default, verifies the response status code.
        `Status Should Be` keyword can be useful when you disable implicit assert using ``expected_status=anything``.

        For example when you have a nested keyword that is used for both OK and ERROR responses:

        |   *** Test Cases ***
        |
        |   Test Get Request And Make Sure Is A 404 Response
        |       ${resp}=            GET Custom Keyword That Returns OK or ERROR Response  case=notfound
        |       Status Should Be    404    ${resp}
        |       Should Be Equal As Strings  NOT FOUND  ${resp.reason}
        |
        |   Test Get Request And Make Sure Is OK
        |       ${resp}=            GET Custom Keyword That Returns OK or ERROR Response  case=pass
        |       Status Should Be    200    ${resp}
        |       Should Be Equal As Strings  OK  ${resp.reason}
        |
        |   *** Keywords ***
        |
        |   GET Custom Keyword That Returns OK or ERROR Response
        |   [Arguments]  $case
        |        [...]
        |       IF $case == notfound
        |           $resp=     GET [...] expected_status=Anything
        |           [Return]   $resp
        |       ELSE
        |        [...]
        """
        if not response:
            response = self.last_response
        self._check_status(expected_status, response, msg)

    @keyword("Request Should Be Successful")
    def request_should_be_successful(self, response=None):
        """
        Fails if response status code is a client or server error (4xx, 5xx).

        ``response`` is the output of other requests keywords like `GET On Session`.
        If omitted the last response will be used.

        In case of failure an HTTPError will be automatically raised.

        For a more versatile assert keyword see `Status Should Be`.
        """
        if not response:
            response = self.last_response
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
        """
        Sends a GET request.

        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as string, dictionary (or list of tuples or bytes)
        through the ``params``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs`` here is a list:

        | ``data``     | Dictionary, list of tuples, bytes, or file-like object to send in the body of the request. |
        | ``json``     | A JSON serializable Python object to send in the body of the request. |
        | ``headers``  | Dictionary of HTTP Headers to send with the request. |
        | ``cookies``  | Dict or CookieJar object to send with the request. |
        | ``files``    | Dictionary of file-like-objects (or ``{'name': file-tuple}``) for multipart encoding upload. |
        | ``file-tuple`` | can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')`` or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers to add for the file. |
        | ``auth`` | Auth tuple to enable Basic/Digest/Custom HTTP Auth. |
        | ``timeout`` | How many seconds to wait for the server to send data before giving up, as a float, or a ``(connect timeout, read timeout)`` tuple. |
        | ``allow_redirects`` | Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``. |
        | ``proxies`` | Dictionary mapping protocol to the URL of the proxy. |
        | ``verify``  | Either a boolean, in which case it controls whether we verify the server's TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to ``True``. Warning: if a session has been created with ``verify=False`` any other requests will not verify the SSL certificate. |
        | ``stream`` | if ``False``, the response content will be immediately downloaded. |
        | ``cert`` | if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair. |

        For more updated and complete information verify the official Requests api documentation:
        https://requests.readthedocs.io/en/latest/api/

        """
        response = self._common_request('get', None, url,
                                        params=params, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('POST')
    def session_less_post(self, url, data=None, json=None,
                          expected_status=None, msg=None, **kwargs):
        """
        Sends a POST request.

        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        response = self._common_request('post', None, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('PUT')
    def session_less_put(self, url, data=None, json=None,
                         expected_status=None, msg=None, **kwargs):
        """
        Sends a PUT request.

        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """

        response = self._common_request("put", None, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('HEAD')
    def session_less_head(self, url,
                          expected_status=None, msg=None, **kwargs):
        """
        Sends a HEAD request.

        The endpoint used to retrieve the HTTP headers is the ``url``.

        ``allow_redirects`` parameter is not provided, it will be set to `False` (as
        opposed to the default behavior).

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        response = self._common_request('head', None, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('PATCH')
    def session_less_patch(self, url, data=None, json=None,
                           expected_status=None, msg=None, **kwargs):
        """
        Sends a PUT request.

        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        response = self._common_request('patch', None, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('DELETE')
    def session_less_delete(self, url,
                            expected_status=None, msg=None, **kwargs):
        """
        Sends a DELETE request.

        The endpoint used to send the request is the ``url`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        response = self._common_request("delete", None, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('OPTIONS')
    def session_less_options(self, url,
                             expected_status=None, msg=None, **kwargs):
        """
        Sends a OPTIONS request.

        The endpoint used to retrieve the resource is the ``url``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        response = self._common_request("options", None, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response
