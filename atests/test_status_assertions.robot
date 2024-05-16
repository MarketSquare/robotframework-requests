*** Settings ***
Library  RequestsLibrary
Resource  res_setup.robot

*** Test Cases ***

Request And Status Should Be Different
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/404  expected_status=any
    Run Keyword And Expect Error  Url: ${HTTP_LOCAL_SERVER}/status/404 Expected status: 404 != 201  Status Should Be  201  ${resp}

Request And Status Should Be Equal
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/404  expected_status=any
    Status Should Be  404  ${resp}

Request And Status Should Be A Named Status Code
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/418  expected_status=any
    Status Should Be  I am a teapot  ${resp}

Request And Status Should Be An Unknown Named Status
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/418  expected_status=any
    Run Keyword And Expect Error    UnknownStatusError: i am an alien    Status Should Be  i am an alien  ${resp}

Invalid Response
    [Tags]  get  status
    Run Keyword And Expect Error  InvalidResponse: this-is-not-a-response*
    ...  Status Should Be  123   this-is-not-a-response

Request And Status Should Be With A Message
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/418  expected_status=any
    Run Keyword And Expect Error  It should be a teapot! Url: ${HTTP_LOCAL_SERVER}/status/418 Expected status: 418 != 200
    ...   Status Should Be  OK  ${resp}  It should be a teapot!

Request Should Be Successful
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/200
    Request Should Be Successful  ${resp}

Request Should Not Be Successful
    [Tags]  get  status
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/500  expected_status=any
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful  ${resp}

Request And Status Should Be An Invalid Expected Status
    [Tags]  get  status
    ${invalid_expected_status}=     Create Dictionary  a=1
    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /status/500  expected_status=any
    Run Keyword And Expect Error   InvalidExpectedStatus*  Status Should Be  ${invalid_expected_status}  ${resp}

Assert Successful On The Last Request
    [Tags]  get  status
    GET On Session  ${GLOBAL_SESSION}  /status/200
    Request Should Be Successful

Assert Successful Fail On The Last Request
    [Tags]  get  status
    GET On Session  ${GLOBAL_SESSION}  /status/500  expected_status=500
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful

Assert Successful Fail On The Last Request After A Not Failing Request
    [Tags]  get  status
    GET On Session  ${GLOBAL_SESSION}  /status/200
    GET On Session  ${GLOBAL_SESSION}  /status/500  expected_status=500
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful

Assert Successful On The Last Request After A Failing Request
    [Tags]  get  status
    GET On Session  ${GLOBAL_SESSION}  /status/500  expected_status=500
    GET On Session  ${GLOBAL_SESSION}  /status/200
    Request Should Be Successful

Assert Status Should Be OK On The Last Request
    [Tags]  post  status
    POST On Session  ${GLOBAL_SESSION}  /status/200
    Status Should Be  200

Assert Status Should Be Fail On The Last Request
    [Tags]  post  status
    POST On Session  ${GLOBAL_SESSION}  /status/500  expected_status=500
    Run Keyword And Expect Error  Url: ${HTTP_LOCAL_SERVER}/status/500 Expected status: 500 != 200  Status Should Be  OK

Assert Successful On The Last Session-Less Request
    [Tags]  put  status
    PUT  ${HTTP_LOCAL_SERVER}/status/200
    Request Should Be Successful

Assert Successful Fail On The Last Session-Less Request
    [Tags]  put  status
    PUT  ${HTTP_LOCAL_SERVER}/status/500  expected_status=500
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful

Assert Successful Fail On The Last Session-Less Request After A Not Failing Request
    [Tags]  get  post  status
    GET  ${HTTP_LOCAL_SERVER}/status/200
    POST  ${HTTP_LOCAL_SERVER}/status/500  expected_status=500
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful

Assert Successful On The Last Session-Less Request After A Failing Request
    [Tags]  get  status
    HEAD  ${HTTP_LOCAL_SERVER}/status/500  expected_status=500
    PATCH  ${HTTP_LOCAL_SERVER}/status/200
    Request Should Be Successful

Assert Status Should Be OK On The Last Session-Less Request
    [Tags]  get  status
    GET  ${HTTP_LOCAL_SERVER}/status/200
    Status Should Be  200

Assert Status Should Be Fail On The Last Session-Less Request
    [Tags]  post  status
    POST  ${HTTP_LOCAL_SERVER}/status/500  expected_status=500
    Run Keyword And Expect Error  Url: ${HTTP_LOCAL_SERVER}/status/500 Expected status: 500 != 200  Status Should Be  OK
