from robot.api.deco import keyword

from .SessionKeywords import SessionKeywords


class RequestsOnSessionKeywords(SessionKeywords):

    @keyword("GET On Session")
    def get_on_session(self, alias, url, params=None,
                       expected_status=None, msg=None, **kwargs):
        """
        Sends a GET request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as dictionary (or list of tuples or bytes)
        through the ``params``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

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
        | ``verify``  | Either a boolean, in which case it controls whether we verify the server's TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to ``True``. |
        | ``stream`` | if ``False``, the response content will be immediately downloaded. |
        | ``cert`` | if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair. |

        For more updated and complete information verify the official Requests api documentation:
        https://requests.readthedocs.io/en/latest/api/

        """
        session = self._cache.switch(alias)
        response = self._common_request("get", session, url,
                                        params=params, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('POST On Session')
    def post_on_session(self, alias, url, data=None, json=None,
                        expected_status=None, msg=None, **kwargs):
        """
        Sends a POST request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("post", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('PATCH On Session')
    def patch_on_session(self, alias, url, data=None, json=None,
                         expected_status=None, msg=None, **kwargs):
        """
        Sends a PATCH request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("patch", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('PUT On Session')
    def put_on_session(self, alias, url, data=None, json=None,
                       expected_status=None, msg=None, **kwargs):
        """
        Sends a PUT request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to send the request is the ``url`` parameter, while its body
        can be passed using ``data`` or ``json`` parameters.

        ``data`` can be a dictionary, list of tuples, bytes, or file-like object.
        If you want to pass a json body pass a dictionary as ``json`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("put", session, url,
                                        data=data, json=json, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword('DELETE On Session')
    def delete_on_session(self, alias, url,
                          expected_status=None, msg=None, **kwargs):
        """
        Sends a DELETE request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to send the request is the ``url`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("delete", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("HEAD On Session")
    def head_on_session(self, alias, url,
                        expected_status=None, msg=None, **kwargs):
        """
        Sends a HEAD request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the HTTP headers is the ``url``.

        ``allow_redirects`` parameter is not provided, it will be set to `False` (as
        opposed to the default behavior).

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("head", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("OPTIONS On Session")
    def options_on_session(self, alias, url,
                           expected_status=None, msg=None, **kwargs):
        """
        Sends a OPTIONS request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in 'Status Should Be' keyword documentation.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET On Session` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("options", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response
