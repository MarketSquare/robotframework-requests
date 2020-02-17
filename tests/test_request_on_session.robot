*** Settings ***
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request On Existing Session
    [Tags]  get
    ${resp}=            GET On Session  ${SESSION}  /anything
    Status Should Be    OK  ${resp}

Get Request With Url Params
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            GET On Session  ${SESSION}  /anything  ${params}
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request With Unordered Parameters
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            GET On Session  params=${params}  alias=${SESSION}
    ...                 url=/anything  data=data  expected_status=200
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]
    Should Be Equal As Strings  data  ${resp.json()}[data]

Get Request And Fail By Default On Http Error
    [Tags]  get
    Run Keyword And Expect Error  HTTPError: 400*
    ...                           GET On Session  ${SESSION}  /status/400

Get Request And Fail By Expecting A 200 Status
    [Tags]  get
    Run Keyword And Expect Error  Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           GET On Session  ${SESSION}  /status/404  param  200

Get Request And Fail By Expecting A 200 Status With A Message
    [Tags]  get
    Run Keyword And Expect Error  Custom msg Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           GET On Session  ${SESSION}  /status/404  param  200  Custom msg

Get Request Expect An Error And Evaluate Response
    [Tags]  get
    ${resp}=    GET On Session  ${SESSION}  /status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Get Request Expect Any Status And Continue On Error
    [Tags]  get
    ${resp}=    GET On Session  ${SESSION}  /status/404  expected_status=ANY
    Should Be Equal As Strings  NOT FOUND  ${resp.reason}

Get Request Expect Anything Status And Continue On Error
    [Tags]  get
    ${resp}=    GET On Session  ${SESSION}  /status/404  expected_status=Anything
    Should Be Equal As Strings  NOT FOUND  ${resp.reason}

Post Request On Existing Session
    [Tags]  post
    ${resp}=            POST On Session  ${SESSION}  /anything
    Status Should Be    OK  ${resp}

Post Request With Data
    [Tags]  post
    ${resp}=            POST On Session  ${SESSION}  /anything  string
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  ${resp.json()}[data]  string

Post Request With Json
    [Tags]  post
    ${body}=            Create Dictionary  a=1  b=2
    ${resp}=            POST On Session  ${SESSION}  /anything  json=${body}
    Status Should Be    OK  ${resp}
    ${data}=            To Json  ${resp.json()}[data]
    Dictionaries Should Be Equal  ${data}  ${body}

Post Request Expect An Error And Evaluate Response
    [Tags]  post
    ${resp}=    POST On Session  ${SESSION}  /status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}
