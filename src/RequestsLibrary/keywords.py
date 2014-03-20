import requests
import json
import vcr

from urllib import urlencode

import robot

from robot.libraries.BuiltIn import BuiltIn


class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()

    def _utf8_urlencode(self, data):
        if type(data) is unicode:
            return data.encode('utf-8')

        if not type(data) is dict:
            return data

        utf8_data = {}
        for k,v in data.iteritems():
            utf8_data[k] = unicode(v).encode('utf-8')
        return urlencode(utf8_data)

    def create_session(self, alias, url, headers={}, cookies=None,
                       auth=None, timeout=None, proxies=None,
                       verify=False):

        """ Create Session: create a HTTP session to a server

        `url` Base url of the server

        `alias` Robot Framework alias to identify the session

        `headers` Dictionary of default headers

        `auth` List of username & password for HTTP Basic Auth

        `timeout` connection timeout

        `proxies` proxy server url

        `verify` set to True if Requests should verify the certificate
        """

        self.builtin.log('Creating session: %s' % alias, 'DEBUG')
        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None
        s = session = requests.Session()
        s.headers.update(headers)
        s.auth = auth if auth else s.auth
        s.proxies = proxies if proxies else  s.proxies

        s.verify = self.builtin.convert_to_boolean(verify)

        # cant pass these into the Session anymore
        self.timeout = timeout
        self.cookies = cookies
        self.verify = verify

        # cant use hooks :(
        s.url = url

        self._cache.register(session, alias=alias)
        return session

    def delete_all_sessions(self):
        """ Removes all the session objects """

        self._cache.empty_cache()

    def to_json(self, content):
        """ Convert a string to a JSON object

        `content` String content to convert into JSON
        """
        return json.loads(content)

    
    def _get_url(self, session, uri):
        ''' Helpere method to get the full url
        '''
        url = session.url
        if uri:
            slash = '' if uri.startswith('/') else '/'
            url = "%s%s%s" %(session.url, slash, uri)
        return url

    def get(self, alias, uri, headers=None, cassette=None):
        """ Send a GET request on the session object found using the
            given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `headers` a dictionary of headers to use with the request
        """
        session = self._cache.switch(alias)
        if cassette:
            with vcr.use_cassette(cassette, serializer='json', cassette_library_dir = 'cassettes/GET', record_mode='new_episodes', match_on=['url', 'method', 'headers', 'body']):
                response = self.get_request(session, uri, headers)
        else:
            response = self.get_request(session, uri, headers)

        return response


    def post(self, alias, uri, data={}, headers=None, files={}, cassette=None):
        """ Send a POST request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `data` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to POST to the server
        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        if cassette:
            with vcr.use_cassette(cassette, serializer='json', cassette_library_dir = 'cassettes/POST', record_mode='new_episodes', match_on=['url', 'method', 'headers', 'body']):
                response = self.post_request(session, uri, data, headers, files)
        else:
            response = self.post_request(session, uri, data, headers, files)

        return response


    def put(self, alias, uri, data=None, headers=None, cassette=None):
        """ Send a PUT request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PUT request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        if cassette:
            with vcr.use_cassette(cassette, serializer='json', cassette_library_dir = 'cassettes/PUT', record_mode='new_episodes', match_on=['url', 'method', 'headers', 'body']):
                response = self.put_request(session, uri, data, headers)
        else:
            response = self.put_request(session, uri, data, headers)

        return response



    def delete(self, alias, uri, data=(), headers=None, cassette=None):
        """ Send a DELETE request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the DELETE request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        if cassette:
            with vcr.use_cassette(cassette, serializer='json', cassette_library_dir = 'cassettes/DELETE', record_mode='new_episodes', match_on=['url', 'method', 'headers', 'body']):
                response = self.delete_request(session, uri, data, headers)
        else:
            response = self.delete_request(session, uri, data, headers)

        return response



    def head(self, alias, uri, headers=None, cassette=None):
        """ Send a HEAD request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the HEAD request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        if cassette:
            with vcr.use_cassette(cassette, serializer='json', cassette_library_dir = 'cassettes/HEAD', record_mode='new_episodes', match_on=['url', 'method', 'headers', 'body']):
                response = self.head_request(session, uri, headers)
        else:
            response = self.head_request(session, uri, headers)

        return response


    def get_request(self, session, uri, headers):
        resp = session.get(self._get_url(session, uri),
                           headers=headers,
                           cookies=self.cookies, timeout=self.timeout)

        # store the last response object
        session.last_resp = resp
        return resp

    def post_request(self, session, uri, data, headers, files):
        resp = session.post(self._get_url(session, uri),
                            data=data, headers=headers,
                            files=files,
                            cookies=self.cookies, timeout=self.timeout)

        # store the last response object
        session.last_resp = resp
        self.builtin.log("Post response: " + resp.content, 'DEBUG')
        return resp

    def put_request(self, session, uri, data, headers):
        resp = session.put(self._get_url(session, uri),
                           data=data, headers=headers,
                           cookies=self.cookies, timeout=self.timeout)

        self.builtin.log("PUT response: %s DEBUG" % resp.content)

        # store the last response object
        session.last_resp = resp
        return resp

    def delete_request(self, session, uri, data, headers):
        resp = session.delete(self._get_url(session, uri), data=data,
                              headers=headers, cookies=self.cookies,
                              timeout=self.timeout)

        # store the last response object
        session.last_resp = resp
        return resp

    def head_request(self, session, uri, headers):
        resp = session.head(self._get_url(session, uri), headers=headers,
                            cookies=self.cookies, timeout=self.timeout)

        # store the last response object
        session.last_resp = resp
        return resp
