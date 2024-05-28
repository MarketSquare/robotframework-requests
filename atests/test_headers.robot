*** Settings ***
Library     Collections
Library     RequestsLibrary


*** Test Cases ***
Get Request With Session Headers
    [Tags]    get    headers
    ${sess_headers}=    Create Dictionary    session-header=true
    Create Session    http_server    ${HTTP_LOCAL_SERVER}    ${sess_headers}
    ${resp}=    GET On Session    http_server    /headers
    Dictionary Should Contain Item    ${resp.json()['headers']}    Session-Header    true

Get Request Overriding Session Headers
    [Tags]    get    headers
    ${sess_headers}=    Create Dictionary    session-header=true
    ${get_headers}=    Create Dictionary    session-header=false
    Create Session    http_server    ${HTTP_LOCAL_SERVER}    ${sess_headers}
    ${resp}=    GET On Session    http_server    /headers    headers=${get_headers}
    Dictionary Should Contain Item    ${resp.json()['headers']}    Session-Header    false

Get Request Headers Are Local
    [Tags]    get    headers
    ${sess_headers}=    Create Dictionary    session-header=true
    ${get_headers}=    Create Dictionary    session-header=false
    Create Session    http_server    ${HTTP_LOCAL_SERVER}    ${sess_headers}
    ${resp1}=    GET On Session    http_server    /headers    headers=${get_headers}
    Dictionary Should Contain Item    ${resp1.json()['headers']}    Session-Header    false
    ${resp2}=    GET On Session    http_server    /headers
    Dictionary Should Contain Item    ${resp2.json()['headers']}    Session-Header    true

Post Request Formatting Json According To Header And Case Insensitive For Keys
    [Tags]    post    headers
    ${sess_headers}=    Create Dictionary    content-type=false
    ${post_headers}=    Create Dictionary    Content-Type=application/json
    ${data}=    Create Dictionary    key=value
    Create Session    http_server    ${HTTP_LOCAL_SERVER}    ${sess_headers}
    ${resp}=    POST On Session    http_server    /anything    json=${data}    headers=${post_headers}
    Dictionary Should Contain Item    ${resp.json()['headers']}    Content-Type    application/json
    Dictionary Should Contain Item    ${resp.json()['json']}    key    value
