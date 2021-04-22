![Python application](https://github.com/MarketSquare/robotframework-requests/workflows/Python%20application/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/MarketSquare/robotframework-requests/branch/master/graph/badge.svg)](https://codecov.io/gh/MarketSquare/robotframework-requests)
[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)

🏠 ``RequestsLibrary`` is a [Robot Framework](https://robotframework.org/) library
aimed to provide HTTP api testing functionalities by wrapping the well known [Python Requests Library](https://github.com/kennethreitz/requests).

## Install stable version
```sh
pip install robotframework-requests
```

## 🤖 Quick start
```robotframework
*** Settings ***
Library               RequestsLibrary

*** Test Cases ***

Quick Get Request Test
    ${response}=    GET  https://www.google.com

Quick Get Request With Parameters Test
    ${response}=    GET  https://www.google.com/search  params=query=ciao  expected_status=200

Quick Get A JSON Body Test
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1
    Should Be Equal As Strings    1  ${response.json()}[id]
```

### What's new in 0.9
Sessionless keywords are now available, you can just `GET`, `POST`, etc.. no need to create a session anymore!
```robotframework
${resp}=  GET  https://www.google.com
```

`Status Should Be` and `Request Should Be Successfull` can use the last response, no need to pass the response anymore!
```robotframework
GET  https://www.google.com
Status Should Be  200
```

### What's new in 0.8

**New keywords structure:**
All requests keywords have been rewritten because of many not backward compatible changes
and to allow in the near future requests keywords without a session.
Example `Get Request` become `GET On Session` and soon there will be also just `GET`
when a session is not needed.
Old keywords `* Request` are now deprecated and will be removed in 1.0.0 version.

**Implicit assert on status code:**
`* On Session` keywords automatically fail if an error status code is returned.
`expect_status=` could be used to specify a status code (`201`, `OK`, `Bad request`)
or `any` if you want to evaluate the response in any case.

**Closer to the original Requests library:**
New keywords have the same parameter orders and structure as the original.
Lot of pre-parsing / encoding has been removed to have a more accurate and unchanged behaviour.

**Cleaner project architecture:**
Main keywords file has been split with a more logic division to allow better and faster maintenance.

## 🤖 More examples
```robotframework
*** Settings ***                                                                                       
Library    Collections                                                                                 
Library    RequestsLibrary                                                                             
                                                                                                       
Suite Setup    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com                   
                                                                                                       
*** Test Cases ***                                                                                     
                                                                                                       
Get Request Test                                                                                       
    Create Session    google  http://www.google.com                                                    
                                                                                                       
    ${resp_google}=   GET On Session  google  /  expected_status=200                                   
    ${resp_json}=     GET On Session  jsonplaceholder  /posts/1                                        
                                                                                                       
    Should Be Equal As Strings          ${resp_google.reason}  OK                                      
    Dictionary Should Contain Value     ${resp_json.json()}  sunt aut facere repellat provident        
                                                                                                       
Post Request Test                                                                                      
    &{data}=    Create dictionary  title=Robotframework requests  body=This is a test!  userId=1       
    ${resp}=    POST On Session    jsonplaceholder  /posts  json=${data}  expected_status=anything     
                                                                                                       
    Status Should Be                 201  ${resp}                                                      
```

### 📖 Keywords documentation
Robotframework-requests offers a wide set of keywords which can be found in the [Keywords documentation](http://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html)

### 🔬 Test examples
You can find many test examples inside the `atests` folder.

## 🤝 Contributing ✍️
Feel free to contribute and open an issue in order to discuss it. Before doing it take a look at the [contribution guidelines](CONTRIBUTING.md).

📢 Get in touch with the community via slack and Users group
- [Robot Framework Slack #requests channel](https://robotframework-slack-invite.herokuapp.com/)
- [Robot Framework Users Group](https://groups.google.com/forum/#!forum/robotframework-users)

