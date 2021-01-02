*** Settings ***
Library  String
Library  Collections
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions


*** Variables ***
${HTTP_LOCAL_SERVER}    http://localhost:5000


*** Test Cases ***
Get Request With Session Headers
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  ${sess_headers}
    ${resp}=  Get Request  http_server  /headers
    Dictionary Should Contain Item  ${resp.json()['headers']}  Session-Header  true

Get Request Overriding Session Headers
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    ${get_headers}=      Create Dictionary  session-header=false
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  ${sess_headers}
    ${resp}=  Get Request  http_server  /headers  ${get_headers}
    Dictionary Should Contain Item  ${resp.json()['headers']}  Session-Header  false

Get Request Headers Are Local
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    ${get_headers}=      Create Dictionary  session-header=false
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  ${sess_headers}
    ${resp1}=  Get Request  http_server  /headers  ${get_headers}
    Dictionary Should Contain Item  ${resp1.json()['headers']}  Session-Header  false
    ${resp2}=  Get Request  http_server  /headers
    Dictionary Should Contain Item  ${resp2.json()['headers']}  Session-Header  true

Post Request Formatting Json According To Header And Case Insensitive For Keys
    [Tags]  post  headers
    ${sess_headers}=     Create Dictionary  content-type=false
    ${post_headers}=     Create Dictionary  Content-Type=application/json
    ${data}=             Create Dictionary  key=value
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  ${sess_headers}
    ${resp}=  Post Request  http_server  /anything  data=${data}  headers=${post_headers}
    Dictionary Should Contain Item  ${resp.json()['headers']}  Content-Type  application/json
    Dictionary Should Contain Item  ${resp.json()['json']}  key  value
