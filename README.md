[![Build Status](https://travis-ci.org/bulkan/robotframework-requests.png?branch=master)](https://travis-ci.org/bulkan/robotframework-requests)

RequestsLibrary is a [Robot Framework](http://code.google.com/p/robotframework/) test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client.

Usage
=====

You need to have requests installed

    pip install -U requests

Now install robotframework-requests

    pip install -U robotframework-requests

|                           |                                  |                           |                                |                      |
| :------------------------ | :------------------------------- | :--------------           | :----------------------------- | :------------------- |
| Settings                  |                                  |                           |                                |
| Library                   | Collections                      |                           |                                |
| Library                   | RequestsLibrary                  |                           |                                |
| Test Cases                |                                  |                           |                                |
| Get Requests              |                                  |                           |                                |
|                           | Create Session                   | github                    | http://github.com/api/v2/json  |
|                           | Create Session                   | google                    | http://www.google.com          |
|                           | ${resp}=                         | Get                       | github                         | /                    |
|                           | Should Be Equal As Strings       | ${resp.status_code}       | 200                            |
|                           | ${resp}=                         | Get                       | github                         | /user/search/bulkan  |
|                           | Should Be Equal As Strings       | ${resp.status_code}       | 200                            |
|                           | ${jsondata}=                     | To JSON                   | ${resp.content}                |
|                           |                                  |                           |                                |
|                           | Dictionary Should Contain Value  | `${jsondata['users'][0]}` | Bulkan Savun Evcimen           |
