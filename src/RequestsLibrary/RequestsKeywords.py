import requests
import json
#import vcr

from urllib import urlencode

import robot

from robot.libraries.BuiltIn import BuiltIn

try:
    from requests_ntlm import HttpNtlmAuth
except ImportError:
    pass


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

    def _create_session(self, alias, url, headers, cookies, auth,
                        timeout, proxies, verify):

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
        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None
        return self._create_session(alias, url, headers, cookies, auth,
                                    timeout, proxies, verify)


    def create_ntlm_session(self, alias, url, auth, headers={}, cookies=None,
                            timeout=None, proxies=None, verify=False):

        """ Create Session: create a HTTP session to a server

        `url` Base url of the server

        `alias` Robot Framework alias to identify the session

        `headers` Dictionary of default headers

        `auth` ['DOMAIN', 'username', 'password'] for NTLM Authentication

        `timeout` connection timeout

        `proxies` proxy server url

        `verify` set to True if Requests should verify the certificate
        """
        if not HttpNtlmAuth:
            raise AssertionError('Requests NTLM module not loaded')
        elif len(auth) != 3:
            raise AssertionError('Incorrect number of authentication arguments'
                                 ' - expected 3, got {}'.format(len(auth)))
        else:
            ntlm_auth = HttpNtlmAuth('{}\\{}'.format(auth[0], auth[1]),
                                     auth[2])
            return self._create_session(alias, url, headers, cookies,
                                        ntlm_auth, timeout, proxies, verify)



    def delete_all_sessions(self):
        """ Removes all the session objects """

        self._cache.empty_cache()

    def to_json(self, content, pretty_print=False):
        """ Convert a string to a JSON object

        `content` String content to convert into JSON

        'pretty_print' If defined, will output JSON is pretty print format
        """
        if pretty_print:
            json_ = self._json_pretty_print(content)
        else:
            json_ = json.loads(content)
        
        return json_


    def get_request(self, alias, uri, headers=None, params={}, allow_redirects=None):
        """ Send a GET request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `headers` a dictionary of headers to use with the request
        """
        session = self._cache.switch(alias)
        params = self._utf8_urlencode(params)
        redir = True if allow_redirects is None else allow_redirects
        response = self._get_request(session, uri, headers, params, redir)
            
        return response


    def get(self, alias, uri, headers=None, params={}, allow_redirects=None):
        """ * * *   Depricated - See Get Request now   * * *
        
        Send a GET request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `headers` a dictionary of headers to use with the request
        """
        print "Deprication Warning  Use Get Request in the future"
        session = self._cache.switch(alias)
        params = self._utf8_urlencode(params)
        redir = True if allow_redirects is None else allow_redirects
        response = self._get_request(session, uri, headers, params, redir)
            
        return response


    def post_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ Send a POST request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the POST request to

        `data` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to POST to the server
        """
        print "Deprication Warning  Use Post Request in the future"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._post_request(session, uri, data, headers, files, redir)

        return response


    def post(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ * * *   Depricated - See Post Request now   * * *
        
        Send a POST request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `data` a dictionary of key-value pairs that will be urlencoded
               and sent as POST data
               or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to POST to the server
        """
        print "Deprication Warning  Use Post Request in the future"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._post_request(session, uri, data, headers, files, redir)

        return response


    def patch_request(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ Send a PATCH request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PATCH request to

        `data` a dictionary of key-value pairs that will be urlencoded
               and sent as PATCH data
               or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to PATCH to the server
        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._patch_request(session, uri, data, headers, files, redir)

        return response


    def patch(self, alias, uri, data={}, headers=None, files={}, allow_redirects=None):
        """ * * *   Depricated - See Patch Request now   * * *

        Send a PATCH request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PATCH request to

        `data` a dictionary of key-value pairs that will be urlencoded
               and sent as PATCH data
               or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        `files` a dictionary of file names containing file data to PATCH to the server
        """
        print "Deprication Warning  Use Patch Request in the future"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._patch_request(session, uri, data, headers, files, redir)

        return response


    def put_request(self, alias, uri, data=None, headers=None, allow_redirects=None):
        """ Send a PUT request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PUT request to

        `headers` a dictionary of headers to use with the request

        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._put_request(session, uri, data, headers, redir)

        return response


    def put(self, alias, uri, data=None, headers=None, allow_redirects=None):
        """ * * *   Depricated - See Put Request now   * * *

        Send a PUT request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PUT request to

        `headers` a dictionary of headers to use with the request

        """
        print "Deprication Warning  Use Put Request in the future"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._put_request(session, uri, data, headers, redir)

        return response


    def delete_request(self, alias, uri, data=(), headers=None, allow_redirects=None):
        """ Send a DELETE request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the DELETE request to

        `headers` a dictionary of headers to use with the request

        """
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._delete_request(session, uri, data, headers, redir)

        return response


    def delete(self, alias, uri, data=(), headers=None, allow_redirects=None):
        """ * * *   Depricated - See Delete Request now   * * *

        Send a DELETE request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the DELETE request to

        `headers` a dictionary of headers to use with the request

        """
        print "Deprication Warning  Use Delete Request in the future"
        session = self._cache.switch(alias)
        data = self._utf8_urlencode(data)
        redir = True if allow_redirects is None else allow_redirects
        response = self._delete_request(session, uri, data, headers, redir)

        return response


    def head_request(self, alias, uri, headers=None, allow_redirects=None):
        """ Send a HEAD request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the HEAD request to

        `headers` a dictionary of headers to use with the request

        """
        session = self._cache.switch(alias)
        redir = False if allow_redirects is None else allow_redirects
        response = self._head_request(session, uri, headers, redir)

        return response


    def head(self, alias, uri, headers=None, allow_redirects=None):
        """ * * *   Depricated - See Head Request now   * * *

        Send a HEAD request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the HEAD request to

        `headers` a dictionary of headers to use with the request

        """
        print "Deprication Warning  Use Head Request in the future"
        session = self._cache.switch(alias)
        redir = False if allow_redirects is None else allow_redirects
        response = self._head_request(session, uri, headers, redir)

        return response


    def options_request(self, alias, uri, headers=None, allow_redirects=None):
        """ Send an OPTIONS request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the OPTIONS request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects
        response = self._options_request(session, uri, headers, redir)

        return response


    def options(self, alias, uri, headers=None, allow_redirects=None):
        """ * * *   Depricated - See Options Request now   * * *

        Send an OPTIONS request on the session object found using the
        given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the OPTIONS request to

        `headers` a dictionary of headers to use with the request

        """
        print "Deprication Warning  Use Options Request in the future"
        session = self._cache.switch(alias)
        redir = True if allow_redirects is None else allow_redirects
        response = self._options_request(session, uri, headers, redir)

        return response


    def _get_request(self, session, uri, headers, params, allow_redirects):
        resp = session.get(self._get_url(session, uri),
                           headers=headers,
                           params=params,
                           cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        return resp


    def _post_request(self, session, uri, data, headers, files, allow_redirects):
        resp = session.post(self._get_url(session, uri),
                            data=data, headers=headers,
                            files=files,
                            cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        self.builtin.log("Post response: " + resp.content, 'DEBUG')
        return resp


    def _patch_request(self, session, uri, data, headers, files, allow_redirects):
        resp = session.patch(self._get_url(session, uri),
                            data=data, headers=headers,
                            files=files,
                            cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        self.builtin.log("Patch response: " + resp.content, 'DEBUG')
        return resp


    def _put_request(self, session, uri, data, headers, allow_redirects):
        resp = session.put(self._get_url(session, uri),
                           data=data, headers=headers,
                           cookies=self.cookies, timeout=self.timeout,
                           allow_redirects=allow_redirects)

        self.builtin.log("PUT response: %s DEBUG" % resp.content)

        # store the last response object
        session.last_resp = resp
        return resp


    def _delete_request(self, session, uri, data, headers, allow_redirects):
        resp = session.delete(self._get_url(session, uri), data=data,
                              headers=headers, cookies=self.cookies,
                              timeout=self.timeout,
                              allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        return resp


    def _head_request(self, session, uri, headers, allow_redirects):
        resp = session.head(self._get_url(session, uri), headers=headers,
                            cookies=self.cookies, timeout=self.timeout,
                            allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        return resp


    def _options_request(self, session, uri, headers, allow_redirects):
        resp = session.options(self._get_url(session, uri), headers=headers,
                            cookies=self.cookies, timeout=self.timeout,
                            allow_redirects=allow_redirects)

        # store the last response object
        session.last_resp = resp
        return resp


    def _get_url(self, session, uri):
        ''' Helper method to get the full url
        '''
        url = session.url
        if uri:
            slash = '' if uri.startswith('/') else '/'
            url = "%s%s%s" %(session.url, slash, uri)
        return url


    def _json_pretty_print(self, content):
        """ Pretty print a JSON object
        
        'content'  JSON object to pretty print
        """
        temp = json.loads(content)
        return json.dumps(temp, sort_keys=True, indent=4, separators=(',', ': '))

