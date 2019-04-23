*** Settings ***
Library  String
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Teardown  Delete All Sessions

*** Test Cases ***
Get Request With Session Headers
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    Create Session  httpbin  http://httpbin.org  ${sess_headers}
    ${resp}=  Get Request  httpbin  /headers
    Dictionary Should Contain Item  ${resp.json()['headers']}  Session-Header  true

Get Request Overriding Session Headers
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    ${get_headers}=      Create Dictionary  session-header=false
    Create Session  httpbin  http://httpbin.org  ${sess_headers}
    ${resp}=  Get Request  httpbin  /headers  ${get_headers}
    Dictionary Should Contain Item  ${resp.json()['headers']}  Session-Header  false

Get Request Headers Are Local
    [Tags]  get  headers
    ${sess_headers}=     Create Dictionary  session-header=true
    ${get_headers}=      Create Dictionary  session-header=false
    Create Session  httpbin  http://httpbin.org  ${sess_headers}
    ${resp1}=  Get Request  httpbin  /headers  ${get_headers}
    Dictionary Should Contain Item  ${resp1.json()['headers']}  Session-Header  false
    ${resp2}=  Get Request  httpbin  /headers
    Dictionary Should Contain Item  ${resp2.json()['headers']}  Session-Header  true

Post Request Formatting Json According To Header And Case Insensitive For Keys
    [Tags]  post  headers
    ${sess_headers}=     Create Dictionary  content-type=false
    ${post_headers}=     Create Dictionary  Content-Type=application/json
    ${data}=             Create Dictionary  key=value
    Create Session  httpbin  http://httpbin.org  ${sess_headers}
    ${resp}=  Post Request  httpbin  /anything  data=${data}  headers=${post_headers}
    Dictionary Should Contain Item  ${resp.json()['headers']}  Content-Type  application/json
    Dictionary Should Contain Item  ${resp.json()['json']}  key  value
