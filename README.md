![Python application](https://github.com/MarketSquare/robotframework-requests/workflows/Python%20application/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/MarketSquare/robotframework-requests/branch/master/graph/badge.svg)](https://codecov.io/gh/MarketSquare/robotframework-requests)
[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-requests.svg)](https://pypi.python.org/pypi/robotframework-requests)

🏠 ``RequestsLibrary`` is a [Robot Framework](https://robotframework.org/) test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client.


## Install stable version
```sh
pip install robotframework-requests
```

## 🤖 Example usage
```robotframework
*** Settings ***
Library               Collections
Library               RequestsLibrary

Suite Setup           Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com

*** Test Cases ***

Get Request Test
    Create Session    google             http://www.google.com

    ${resp_google}=   GET On Session     google             /           expected_status=200
    ${resp_json}=     GET On Session     jsonplaceholder    /posts/1

    Should Be Equal As Strings           ${resp_google.reason}    OK
    Dictionary Should Contain Value      ${resp_json.json()}    sunt aut facere repellat provident occaecati excepturi optio reprehenderit

Post Request Test
    &{data}=          Create dictionary  title=Robotframework requests  body=This is a test!  userId=1
    ${resp}=          POST On Session    jsonplaceholder     /posts    json=${data}
    
    Status Should Be                     201    ${resp}
    Dictionary Should Contain Key        ${resp.json()}     id
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

