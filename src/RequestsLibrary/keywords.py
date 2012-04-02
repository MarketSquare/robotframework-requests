import requests
import json

from urllib import urlencode

import robot

from robot.libraries.BuiltIn import BuiltIn

class RequestsKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        '''
        TODO: probably can set global proxy here
        '''

        self._cache = robot.utils.ConnectionCache('No sessions created')

        #requests.settings.base_headers['User-Agent'] = 'robotframework-requests'


        self.builtin = BuiltIn()


    def create_session(self, alias, url, headers=None, cookies=None, auth=None, timeout=None, proxies=None):
        """ Create Session: create a HTTP session to a server

        `url` Base url of the server

        `alias` Robot Framework alias to identify the session

        `headers` Dictionary of default headers

        `auth` Dictionary of username & password for HTTP Basic Auth

        `timeout` connection timeout

        `proxies` proxy server url

        """


        def baseurlhook(args):
            # url is the base url. Request url is uri
            args['url'] = '%s%s' %(url, args['url'])
        
        self.builtin.log('Creating session: %s' %alias, 'DEBUG')

        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None

        session = requests.session(hooks=dict(args=baseurlhook), auth=auth, headers=headers,
                cookies=cookies, timeout=timeout, proxies=proxies )

        self._cache.register(session, alias=alias)
        return session


    def delete_all_sessions(self):
        """ Removes all the session objects
        """

        self._cache.empty_cache()


    def to_json(self, content):
        """ Convert a string to a JSON object 

        `content` String content to convert into JSON
        
        """
        return json.loads(content)

    
    def get(self, alias, uri, headers=None):
        """ Send a GET request on the session object found using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        resp = session.get(uri, headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def post(self, alias, uri, data={}, headers=None):
        """ Send a POST request on the session object found using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the GET request to

        `data` a dictionary of key-value pairs that will be urlencoded and sent as POST data
                or binary data that is sent as the raw body content

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        if type(data) is dict:
            resp = session.post(uri, data=urlencode(data), headers=headers)
        else:
            resp = session.post(uri, data=data, headers=headers)

        # store the last response object
        session.last_resp = resp
        self.builtin.log("Post response: " + resp.content, 'DEBUG')
        return resp


    def put(self, alias, uri, data=None, headers=None):
        """ Send a PUT request on the session object found using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the PUT request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        resp = session.put(uri, data=urlencode(data), headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def delete(self, alias, uri, data=(), headers=None):
        """ Send a DELETE request on the session object found using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the DELETE request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        resp = session.delete("%s?%s" %(uri, urlencode(data)), headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def head(self, alias, uri, headers=None):
        """ Send a HEAD request on the session object found using the given `alias`

        `alias` that will be used to identify the Session object in the cache

        `uri` to send the HEAD request to

        `headers` a dictionary of headers to use with the request

        """

        session = self._cache.switch(alias)
        resp = session.head(uri, headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp



if __name__ == '__main__':
     rk = RequestsKeywords()
     rk.create_session('github','http://github.com/api/v2/json')
     resp =  rk.get('github', 'http://github.com/api/v2/json/user/search/bulkan')
     import pdb; pdb.set_trace() 
