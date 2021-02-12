*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Get Request Should Have Get Method
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()}[method]  GET

Get Request With Url Params As Dictionary
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything  ${params}
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request With Url Params As Kwargs String
    [Tags]  get
    ${params}=          Create Dictionary   this_is_a_string=1  p2=2
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     params=this_is_a_string=1&p2=2
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request With Url Params As Escaped String
    [Tags]  get
    ${params}=          Create Dictionary   this_is_a_string=1  p2=2
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     this_is_a_string\=1&p2\=2
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request With Url Duplicated Keys In Params
    [Tags]  get
    ${array}=           Create List   1  2
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     params=key=1&key=2
    Status Should Be    OK  ${resp}
    Lists Should Be Equal  ${array}  ${resp.json()}[args][key]

Get Request With Url Duplicated Keys In Params And PHP Style Array
    [Tags]  get
    ${array}=           Create List   1  2
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     params=key[]=1&key[]=2
    Status Should Be    OK  ${resp}
    Lists Should Be Equal  ${array}  ${resp.json()}[args][key[]]

Get Request With Url Params As PHP Style Array
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     params=key[]=1,2
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  1,2  ${resp.json()}[args][key[]]

Get Request With Url Params As Array
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/anything
    ...                     params=key=[1,2]
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  [1,2]  ${resp.json()}[args][key]

Get Request With Unordered Parameters
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            GET  params=${params}
    ...                 url=${HTTP_LOCAL_SERVER}/anything  data=data  expected_status=200
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]
    Should Be Equal As Strings  data  ${resp.json()}[data]

Get Request And Fail By Default On Http Error
    [Tags]  get
    Run Keyword And Expect Error  HTTPError: 400*
    ...                           GET  ${HTTP_LOCAL_SERVER}/status/400

Get Request And Fail By Expecting A 200 Status
    [Tags]  get
    Run Keyword And Expect Error  Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           GET  ${HTTP_LOCAL_SERVER}/status/404  param  200

Get Request And Fail By Expecting A 200 Status With A Message
    [Tags]  get
    Run Keyword And Expect Error  Custom msg Url: http://localhost:5000/status/404?param Expected status: 404 != 200
    ...                           GET  ${HTTP_LOCAL_SERVER}/status/404  param  200  Custom msg

Get Request Expect An Error And Evaluate Response
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Get Request Expect Any Status And Continue On Error
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/status/404  expected_status=ANY
    Should Be Equal As Strings  NOT FOUND  ${resp.reason}

Get Request Expect Anything Status And Continue On Error
    [Tags]  get
    ${resp}=            GET  ${HTTP_LOCAL_SERVER}/status/404  expected_status=Anything
    Should Be Equal As Strings  NOT FOUND  ${resp.reason}
