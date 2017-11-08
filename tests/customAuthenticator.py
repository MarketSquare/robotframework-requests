from requests.auth import HTTPBasicAuth
    
    # Example of a keyword that a test author would supply in order to use the
    # `Create Custom Session` keyword.  Such a keyword can return any subclass
    # of `AuthBase`.
    # http://docs.python-requests.org/en/master/user/advanced/#custom-authentication
def get_custom_auth(user, pwd):
    return HTTPBasicAuth(user, pwd)
