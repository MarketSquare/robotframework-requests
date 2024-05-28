from robot.api.deco import keyword

from RequestsLibrary.utils import warn_if_equal_symbol_in_url_on_session

from .SessionKeywords import SessionKeywords


class RequestsOnSessionKeywords(SessionKeywords):

    @keyword("GET On Session")
    @warn_if_equal_symbol_in_url_on_session
    def get_on_session(
        self, alias, url, params=None, expected_status=None, msg=None, **kwargs
    ):
        """
        Sends a GET request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``, while query
        string parameters can be passed as string, dictionary (or list of tuples or bytes)
        through the ``params``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("GET", session, url, params=params, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("POST On Session")
    @warn_if_equal_symbol_in_url_on_session
    def post_on_session(
        self, alias, url, data=None, json=None, expected_status=None, msg=None, **kwargs
    ):
        """
        Sends a POST request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
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
        session = self._cache.switch(alias)
        response = self._common_request(
            "POST", session, url, data=data, json=json, **kwargs
        )
        self._check_status(expected_status, response, msg)
        return response

    @keyword("PATCH On Session")
    @warn_if_equal_symbol_in_url_on_session
    def patch_on_session(
        self, alias, url, data=None, json=None, expected_status=None, msg=None, **kwargs
    ):
        """
        Sends a PATCH request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
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
        session = self._cache.switch(alias)
        response = self._common_request(
            "PATCH", session, url, data=data, json=json, **kwargs
        )
        self._check_status(expected_status, response, msg)
        return response

    @keyword("PUT On Session")
    @warn_if_equal_symbol_in_url_on_session
    def put_on_session(
        self, alias, url, data=None, json=None, expected_status=None, msg=None, **kwargs
    ):
        """
        Sends a PUT request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
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
        session = self._cache.switch(alias)
        response = self._common_request(
            "PUT", session, url, data=data, json=json, **kwargs
        )
        self._check_status(expected_status, response, msg)
        return response

    @keyword("DELETE On Session")
    @warn_if_equal_symbol_in_url_on_session
    def delete_on_session(self, alias, url, expected_status=None, msg=None, **kwargs):
        """
        Sends a DELETE request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to send the request is the ``url`` parameter.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("DELETE", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("HEAD On Session")
    @warn_if_equal_symbol_in_url_on_session
    def head_on_session(self, alias, url, expected_status=None, msg=None, **kwargs):
        """
        Sends a HEAD request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the HTTP headers is the ``url``.

        ``allow_redirects`` parameter is not provided, it will be set to ``${False}`` (as
        opposed to the default behavior ``${True}``).

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)

        # Do not allow redirects for HEAD method by default.
        if "allow_redirects" not in kwargs:
            kwargs["allow_redirects"] = False

        response = self._common_request("HEAD", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("OPTIONS On Session")
    @warn_if_equal_symbol_in_url_on_session
    def options_on_session(self, alias, url, expected_status=None, msg=None, **kwargs):
        """
        Sends an OPTIONS request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("OPTIONS", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("CONNECT On Session")
    @warn_if_equal_symbol_in_url_on_session
    def connect_on_session(self, alias, url, expected_status=None, msg=None, **kwargs):
        """
        Sends a CONNECT request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("CONNECT", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response

    @keyword("TRACE On Session")
    @warn_if_equal_symbol_in_url_on_session
    def trace_on_session(self, alias, url, expected_status=None, msg=None, **kwargs):
        """
        Sends a TRACE request on a previously created HTTP Session.

        Session will be identified using the ``alias`` name.
        The endpoint used to retrieve the resource is the ``url``.

        By default this keyword fails if a status code with error values is returned in the response,
        this behavior can be modified using the ``expected_status`` and ``msg`` parameters,
        read more about it in `Status Should Be` keyword documentation.
        In order to disable this implicit assert mechanism you can pass as ``expected_status`` the values ``any`` or
        ``anything``.

        Other optional requests arguments can be passed using ``**kwargs``
        see the `GET` keyword for the complete list.
        """
        session = self._cache.switch(alias)
        response = self._common_request("TRACE", session, url, **kwargs)
        self._check_status(expected_status, response, msg)
        return response
