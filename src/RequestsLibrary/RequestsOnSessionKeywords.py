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
