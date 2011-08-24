import requests

import urllib
import urllib2
import json

import robot


class RequestsLibrary(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        '''
        TODO: probably can set global proxy here
        '''

        self._cache = robot.utils.ConnectionCache('No session')


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

        session = requests.session(hooks=dict(args=baseurlhook))
        self._cache.register(session, alias=alias)
        return session


    def delete_all_sessions(self):
        ''' Delete Session: removes all the session objects
        '''

        self._cache.empty_cache()

    
    def get(self, alias, uri, **kwargs):
        ''' Get: send a get request on the session object found using the given alias 
        '''

        session = self._cache.switch(alias)
        resp = session.get(uri, **kwargs)

        # store the last response object
        session.last_resp = resp
        return resp


    
    def to_json(self, content):
        return json.loads(content)


if __name__ == '__main__':
    rl = RequestsLibrary()
    session = rl.create_session('github', 'http://github.com/api/v2/json')
    resp = rl.get('github', '/user/search/bulkan')
    jsondata = rl.to_json(resp.content)

    # sometimes you just need pdb
    import pdb; pdb.set_trace() 

