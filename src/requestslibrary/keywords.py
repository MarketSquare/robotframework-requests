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

        requests.settings.base_headers['User-Agent'] = 'robotframework-requests'


        self.builtin = BuiltIn()


    def create_session(self, alias, url, headers=None, cookies=None, auth=None, timeout=None, proxies=None):
        ''' Create Session: create a HTTP session to a server

        *url:* Base url of the server
        *alias:* Robot Framework alias to identify the session
        *headers:* Dictionary of default headers
        *auth:* Dictionary of username & password for HTTP Basic Auth
        *timeout:* connection timeout
        *proxies:* proxy server url
        '''

        def baseurlhook(args):
            # url is the base url. Request url is uri
            args['url'] = '%s%s' %(url, args['url'])
        
        self.builtin.log('Creating session: %s' %alias, 'DEBUG')

        session = requests.session(hooks=dict(args=baseurlhook), auth=auth, headers=headers,
                cookies=cookies, timeout=timeout, proxies=proxies )
        self._cache.register(session, alias=alias)
        return session


    def delete_all_sessions(self):
        ''' Delete Session: removes all the session objects
        '''

        self._cache.empty_cache()


    def to_json(self, content):
        return json.loads(content)

    
    def get(self, alias, uri, headers=None):
        ''' Get: send a GET request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.get(uri, headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def post(self, alias, uri, data=(), headers=None):
        ''' Post: send a POST request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.post(uri, data=urlencode(data), headers=headers)

        # store the last response object
        session.last_resp = resp
        self.builtin.log("Post response: " + resp.content, 'DEBUG')
        return resp


    def put(self, alias, uri, data=None, headers=None):
        ''' Put: send a PUT request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.put(uri, data=urlencode(data), headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def delete(self, alias, uri, data=(), headers=None):
        ''' Delete: send a DELETE request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.delete("%s?%s" %(uri, urlencode(data)), headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


    def head(self, alias, uri, headers=None):
        ''' Delete: send a HEAD request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.head(uri, headers=headers)

        # store the last response object
        session.last_resp = resp
        return resp


#if __name__ == '__main__':
#    rl = RequestsLibrary()
#    session = rl.create_session('github', 'http://github.com/api/v2/json')
#    auth = ('user', 'passwd')
#    session = rl.create_session('httpbin', 'http:/httpbin.org', auth=auth)
#    resp = rl.get('httpbin', '/basic-auth/user/passwd')
