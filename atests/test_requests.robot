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

Post Request
    [Tags]  post
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Post Request Should Have Post Method
    [Tags]  Post
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()}[method]  POST

Post Request With Data
    [Tags]  post
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/anything  string
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  ${resp.json()}[data]  string

Post Request With Json
    [Tags]  post
    ${body}=            Create Dictionary  a=1  b=2
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/anything  json=${body}
    Status Should Be    OK  ${resp}
    ${data}=            Evaluate  ${resp.json()}[data]
    Dictionaries Should Be Equal  ${data}  ${body}

Post Request Expect An Error And Evaluate Response
    [Tags]  post
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Post Request Expect Anything Status And Continue On Error
    [Tags]  post
    ${resp}=            POST  ${HTTP_LOCAL_SERVER}/status/400  expected_status=anything
    Should Be Equal As Strings  BAD REQUEST  ${resp.reason}

Put Request
    [Tags]  put
    ${resp}=            PUT  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Put Request Should Have Put Method
    [Tags]  put
    ${resp}=            PUT  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()}[method]  PUT

Put Request With Data
    [Tags]  put
    ${resp}=            PUT  ${HTTP_LOCAL_SERVER}/anything  string
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  ${resp.json()}[data]  string

Put Request With Json
    [Tags]  put
    ${body}=            Create Dictionary  a=1  b=2
    ${resp}=            PUT  ${HTTP_LOCAL_SERVER}/anything  json=${body}
    Status Should Be    OK  ${resp}
    ${data}=            Evaluate  ${resp.json()}[data]
    Dictionaries Should Be Equal  ${data}  ${body}

Put Request Expect An Error And Evaluate Response
    [Tags]  put
    ${resp}=            PUT  ${HTTP_LOCAL_SERVER}/status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Head Request
    [Tags]  head
    ${resp}=            HEAD  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Head Request Should Not Have A Body
    [Tags]  head
    ${resp}=            HEAD  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings     ${resp.content}   ${Empty}

Head Request With Kwargs Params
    [Tags]  head
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            HEAD  ${HTTP_LOCAL_SERVER}/anything  params=${params}
    Status Should Be    OK  ${resp}

Head Request With Header
    [Tags]  head
    ${accept_type}=     Set Variable                 application/json
    ${headers}=         Create Dictionary   Accept   ${accept_type}
    ${resp}=            HEAD  ${HTTP_LOCAL_SERVER}/anything  headers=${headers}
    Status Should Be    OK  ${resp}
    ${content_type_response}=  Get From Dictionary      ${resp.headers}   Content-Type
    Should Be Equal   ${accept_type}  ${content_type_response}

Head Request And Fail By Default On Http Error
    [Tags]  head
    Run Keyword And Expect Error  HTTPError: 400*
    ...                           HEAD  ${HTTP_LOCAL_SERVER}/status/400

Head Request Expect An Error And Evaluate Response
    [Tags]  head
    ${resp}=            HEAD  ${HTTP_LOCAL_SERVER}/status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Patch Request
    [Tags]  Patch
    ${resp}=            PATCH  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Patch Request Should Have Patch Method
    [Tags]  Patch
    ${resp}=            PATCH  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()}[method]  PATCH

Patch Request With Data
    [Tags]  Patch
    ${resp}=            PATCH  ${HTTP_LOCAL_SERVER}/anything  string
    Status Should Be    OK  ${resp}
    Should Be Equal As Strings  ${resp.json()}[data]  string

Patch Request With Json
    [Tags]  Patch
    ${body}=            Create Dictionary  a=1  b=2
    ${resp}=            PATCH  ${HTTP_LOCAL_SERVER}/anything  json=${body}
    Status Should Be    OK  ${resp}
    ${data}=            Evaluate  ${resp.json()}[data]
    Dictionaries Should Be Equal  ${data}  ${body}

Patch Request Expect An Error And Evaluate Response
    [Tags]  Patch
    ${resp}=            PATCH  ${HTTP_LOCAL_SERVER}/status/401  expected_status=401
    Should Be Equal As Strings  UNAUTHORIZED  ${resp.reason}

Delete Request
    [Tags]  Delete
    ${resp}=            DELETE  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Delete Request Should Have Delete Method
    [Tags]  Delete
    ${resp}=            DELETE  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()}[method]  DELETE

Delete Request Expect An Error And Evaluate Response
    [Tags]  Delete
    ${resp}=            DELETE  ${HTTP_LOCAL_SERVER}/status/202  expected_status=202
    Should Be Equal As Strings  ACCEPTED  ${resp.reason}

Options Request On Existing Session
    [Tags]  options
    ${resp}=            OPTIONS  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}

Options Request Check Allow Header
    [Tags]  options
    ${allow_header}=    Create List   POST  HEAD  PATCH  GET  TRACE  DELETE  OPTIONS  PUT
    ${resp}=            OPTIONS  ${HTTP_LOCAL_SERVER}/anything
    Status Should Be    OK  ${resp}
    ${allow_response_header}=  Get From Dictionary      ${resp.headers}   Allow
    ${allow_response_header}=  Split String  ${allow_response_header}  ,${SPACE}
    Lists Should Be Equal   ${allow_header}  ${allow_response_header}  ignore_order=True

Options Request And Bad Request Not Fail
    [Tags]  options
    ${resp}=            OPTIONS  ${HTTP_LOCAL_SERVER}/status/400
    Status Should Be    OK  ${resp}

Options Request Expect A Success On Unauthorized Request
    [Tags]  options
    ${resp}=            OPTIONS  ${HTTP_LOCAL_SERVER}/status/401  expected_status=200
    Status Should Be    OK  ${resp}
