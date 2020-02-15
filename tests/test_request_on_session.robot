*** Settings ***
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request On Existing Session
    [Tags]  get
    ${resp}=            Get On Session  ${SESSION}  /anything
    Status Should Be    OK  ${resp}

Get Request With Url Params
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            Get On Session  ${SESSION}  /anything  ${params}
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request With Unordered Parameters
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            Get On Session  params=${params}  alias=${SESSION}
    ...                 url=/anything  data=data  expected_status=200
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]
    Should Be Equal As Strings  data  ${resp.json()}[data]

Get Request And Fail By Default On Http Error
    [Tags]  get
    Run Keyword And Expect Error  HTTPError: 400*
    ...                           Get On Session  ${SESSION}  /status/400

Get Request And Fail By Expecting A 200 Status
    [Tags]  get
    Run Keyword And Expect Error  Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           Get On Session  ${SESSION}  /status/404  param  200

Get Request And Fail By Expecting A 200 Status With A Message
    [Tags]  get
    Run Keyword And Expect Error  Custom msg Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           Get On Session  ${SESSION}  /status/404  param  200  Custom msg
