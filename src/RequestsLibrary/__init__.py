from .RequestsKeywords import RequestsKeywords
from .version import VERSION

_version_ = VERSION


class RequestsLibrary(RequestsKeywords):
    """``RequestsLibrary`` is a HTTP client keyword library that uses
    test library that uses the [https://github.com/kennethreitz/requests|Requests] HTTP client.

    Here is a sample test case:

    | ***** Settings *****   |                                 |                     |                       |               |
    | Library                | Collections                     |                     |                       |               |
    | Library                | RequestsLibrary                 |                     |                       |               |
    | ***** Test Cases ***** |                                 |                     |                       |               |
    | Get Requests           |                                 |                     |                       |               |
    |                        | Create Session                  | github              | http://api.github.com |               |
    |                        | Create Session                  | google              | http://www.google.com |               |
    |                        | ${resp}=                        | Get Request         | google                | /             |
    |                        | Should Be Equal As Strings      | ${resp.status_code} | 200                   |               |
    |                        | ${resp}=                        | Get Request         | github                | /users/bulkan |
    |                        | Should Be Equal As Strings      | ${resp.status_code} | 200                   |               |
    |                        | Dictionary Should Contain Value | ${resp.json()}      | Bulkan Savun Evcimen  |               |
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
