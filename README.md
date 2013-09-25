[![Build Status](https://travis-ci.org/bulkan/robotframework-requests.png?branch=master)](https://travis-ci.org/bulkan/robotframework-requests)

RequestsLibrary is a [Robot Framework](http://code.google.com/p/robotframework/) test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client.

Supports requests=>1.2.3

Usage
=====

Install robotframework-requests via `pip`

    pip install -U robotframework-requests


Here is a sample test case.

|                           |                                  |                     |                                |                      |
| :------------------------ | :------------------------------- | :--------------     | :----------------------------- | :------------------- |
| Settings                  |                                  |                     |                                |
| Library                   | Collections                      |                     |                                |
| Library                   | RequestsLibrary                  |                     |                                |
| Test Cases                |                                  |                     |                                |
| Get Requests              |                                  |                     |                                |
|                           | Create Session                   | github              | http://api.github.com          |
|                           | Create Session                   | google              | http://www.google.com          |
|                           | ${resp}=                         | Get                 | google                         | /                    |
|                           | Should Be Equal As Strings       | ${resp.status_code} | 200                            |
|                           | ${resp}=                         | Get                 | github                         | /users/bulkan        |
|                           | Should Be Equal As Strings       | ${resp.status_code} | 200                            |
|                           | ${jsondata}=                     | To JSON             | ${resp.content}                |
|                           |                                  |                     |                                |
|                           | Dictionary Should Contain Value  | `${jsondata}`       | Bulkan Savun Evcimen           |


RequestsLibrary, tries to follow the same API as requests. In the above example we load in the `RequestsLibrary` using the `Library` keyword.
To be able to distinguish HTTP requests to different hosts and for ease of creation of test cases, you need to create a `Session`. Internally
this will create a `request.Session` object.  The `Create Session` keyword accepts to two arguments an _alias_ to identify the session later
and the _root url_. 

All of the HTTP verbs are mapped to keywords and they at least accept two arguments. The first is the _alias_ identifying the Session we created earlier. 
The second argument is _URI_

Above we create two Sessions one to the _github api_ and the other to _google_. Creating sessions dont send any requests.

After we create a Session we can send any of the following `Get, Post, Put, Delete, Head` requests. Again, in the above example we send a GET request
to the session with the alias _google_ and check the HTTP response code. Then send a another GET request but this time to the session with 
the alias _github_ and pass in a `uri`. In this case it is `/users/bulkan` which will return a JSON string. `RequestsLibrary` provide a convenience 
keyword for loading in a JSON string called `To JSON`.


For individual keyword documentation generated see the following;

http://bulkan.github.io/robotframework-requests/
