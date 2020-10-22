![Python application](https://github.com/MarketSquare/robotframework-requests/workflows/Python%20application/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/MarketSquare/robotframework-requests/branch/master/graph/badge.svg)](https://codecov.io/gh/MarketSquare/robotframework-requests)
[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)

``RequestsLibrary`` is a [Robot Framework](https://robotframework.org/) test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client.

# Usage

Install robotframework-requests and it's dependencies via ``pip``

```bash
pip install robotframework-requests
```

Here is a sample test case:

```robotframework
*** Settings ***
Library               Collections
Library               RequestsLibrary

*** Test Cases ***
Get Requests
    Create Session    github          http://api.github.com
    Create Session    google          http://www.google.com
    ${resp}=          GET On Session  google               /
    ${resp}=          GET On Session  github               /users/bulkan
    Dictionary Should Contain Value   ${resp.json()}       Bulkan Evcimen
```
RequestsLibrary follow the same API as requests. 
In the above example, we load in the ``RequestsLibrary`` using the ``Library`` keyword.
To be able to distinguish HTTP requests to different hosts and for ease of creation of test cases, you need to create a `Session`.

The `Create Session` keyword needs two arguments:

* _alias_ to identify the session later
* _url_ to the server

HTTP verbs are mapped keywords which accept two arguments:

* _alias_ identifying the Session we created earlier.
* _url_ to send the request to.

Above we create two Sessions - one to _github_, and the other to _google_. Creating sessions doesn't send any requests.

After we create a Session we can send any of the following ``Get, Post, Put, Patch, Options, Delete, and Head`` requests.
In the above example we send a GET request to the session with the alias _google_ and check the HTTP response code.
Then send a another GET request but this time to the session with the alias _github_ and pass in a `uri`.
In this case it is ``/users/bulkan`` which will return a JSON string.
`RequestsLibrary` returned object provides a method to get the content as a JSON object format called json().

You could also assert on the response status code like below, but the ``GET On Session`` keyword automatically fails if an error is returned.

```robotframework
    Status Should Be  Ok              ${resp}
    Status Should Be  200             ${resp}
    Request Should Be Successful      ${resp}
```  

Here is another test case where an outbound http proxy is used.

```robotframework
*** Settings ***
Library               RequestsLibrary

*** Test Cases ***
Proxy Requests
    ${proxies}=       Create Dictionary  http=http://acme.com:912  https=http://acme.com:913
    Create Session    github             http://api.github.com     proxies=${proxies}
    ${resp}=          Get Request        github                    /
    Status Should Be  OK                 ${resp}
```

Another test case where cookies are sent in the request headers:

```robotframework
*** Settings ***
Library               RequestsLibrary

*** Test Cases ***
Cookies in request
    ${cookies}=       Create Dictionary  userid=1234567         last_visit=2017-12-22
    Create Session    github             http://api.github.com  cookies=${cookies}
    ${resp}=          Get Request        github                 /
    Should Be Equal As Strings           ${resp.status_code}    200
```

For more examples see the `atests` folder which contains testcase files that is used to test the keywords in this library against a [httpbin.org](http://httpbin.org) local server.

# Documentation

For individual keyword documentation see the following:

[Keywords documentation](http://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html)

# Help

Send your questions to the
- [Robot Framework Slack #requests channel](https://robotframework-slack-invite.herokuapp.com/)
- [Robot Framework Users Group](https://groups.google.com/forum/#!forum/robotframework-users)

# Contribute

See the [How To Contribute](CONTRIBUTING.md) to the project page.

### NEW 0.8 pre-release alpha version available

Please install it:

```bash
pip install robotframework-requests --pre
```

and give us feedback!

- [0.8 README](https://github.com/MarketSquare/robotframework-requests/blob/0.8/README.md)
- [0.8 Keywords documentation](https://robotframework-requests.netlify.app/doc/requestslibrary)
