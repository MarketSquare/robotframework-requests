*** Settings ***
Suite Teardown    Delete All Sessions
Library           Collections
Library           String
Library           ../src/RequestsLibrary/RequestsKeywords.py
Library           OperatingSystem

*** Test Cases ***
Get Request
    [Tags]    get
    Create Session    google    http://www.google.com
    Create Session    github    https://api.github.com
    ${resp}=    Get Request    google    /
    Should Be Equal As Strings    ${resp.status_code}    200
    ${resp}=    Get Request    github    /users/bulkan
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Value    ${resp.json()}    Bulkan Evcimen

Get Request with Url Parameters
    [Tags]    get
    Create Session    httpbin    http://httpbin.org
    ${params}=    Create Dictionary    key    value    key2    value2
    ${resp}=    Get Request    httpbin    /get    params=${params}
    Should Be Equal As Strings    ${resp.status_code}    200
    ${jsondata}=    To Json    ${resp.content}
    Should be Equal    ${jsondata['args']}    ${params}

Get HTTPS & Verify Cert
    [Tags]    get
    Create Session    httpbin    https://httpbin.org    verify=True
    ${resp}=    Get Request    httpbin    /get
    Should Be Equal As Strings    ${resp.status_code}    200

Get With Auth
    [Tags]    get
    ${auth}=    Create List    user    passwd
    Create Session    httpbin    https://httpbin.org    auth=${auth}
    ${resp}=    Get Request    httpbin    /basic-auth/user/passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Post Request With No Data
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Post Request    httpbin    /post
    Should Be Equal As Strings    ${resp.status_code}    200

Put Request With No Data
    [Tags]    put
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Put Request    httpbin    /put
    Should Be Equal As Strings    ${resp.status_code}    200

Post Request With No Dictionary
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    Set Test Variable    ${data}    some content
    ${resp}=    Post Request    httpbin    /post    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Contain    ${resp.content}    ${data}

Put Request With No Dictionary
    [Tags]    put
    Create Session    httpbin    http://httpbin.org
    Set Test Variable    ${data}    some content
    ${resp}=    Put Request    httpbin    /put    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Contain    ${resp.content}    ${data}

Post Requests
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    ${data}=    Create Dictionary    name    bulkan    surname    evcimen
    ${headers}=    Create Dictionary    Content-Type    application/x-www-form-urlencoded
    ${resp}=    Post Request    httpbin    /post    data=${data}    headers=${headers}
    Dictionary Should Contain Value    ${resp.json()['form']}    bulkan
    Dictionary Should Contain Value    ${resp.json()['form']}    evcimen

Post With Unicode Data
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    ${data}=    Create Dictionary    name    度假村
    ${headers}=    Create Dictionary    Content-Type    application/x-www-form-urlencoded
    ${resp}=    Post Request    httpbin    /post    data=${data}    headers=${headers}
    Dictionary Should Contain Value    ${resp.json()['form']}    度假村

Post Request With File
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    ${file_data}=    Get Binary File    ${CURDIR}${/}data.json
    ${files}=    Create Dictionary    file    ${file_data}
    ${resp}=    Post Request    httpbin    /post    files=${files}
    ${file}=    To Json    ${resp.json()['files']['file']}
    Dictionary Should Contain Key    ${file}    one
    Dictionary Should Contain Key    ${file}    two

Put Requests
    [Tags]    put
    Create Session    httpbin    http://httpbin.org
    ${data}=    Create Dictionary    name    bulkan    surname    evcimen
    ${headers}=    Create Dictionary    Content-Type    application/x-www-form-urlencoded
    ${resp}=    Put Request    httpbin    /put    data=${data}    headers=${headers}
    Dictionary Should Contain Value    ${resp.json()['form']}    bulkan
    Dictionary Should Contain Value    ${resp.json()['form']}    evcimen

Head Request
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Head Request    httpbin    /headers
    Should Be Equal As Strings    ${resp.status_code}    200

Options Request
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Options Request    httpbin    /headers
    Should Be Equal As Strings    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.headers}    allow

Delete Request With No Data
    [Tags]    delete
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Delete Request    httpbin    /delete
    Should Be Equal As Strings    ${resp.status_code}    200

Delete Request With Data
    [Tags]    delete
    Create Session    httpbin    http://httpbin.org
    ${data}=    Create Dictionary    name    bulkan    surname    evcimen
    ${resp}=    Delete Request    httpbin    /delete    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    200
    Log    ${resp.content}
    Comment    Dictionary Should Contain Value    ${resp.json()['data']}    bulkan
    Comment    Dictionary Should Contain Value    ${resp.json()['data']}    evcimen

Patch Requests
    [Tags]    patch
    Create Session    httpbin    http://httpbin.org
    ${data}=    Create Dictionary    name    bulkan    surname    evcimen
    ${headers}=    Create Dictionary    Content-Type    application/x-www-form-urlencoded
    ${resp}=    Patch Request    httpbin    /patch    data=${data}    headers=${headers}
    Dictionary Should Contain Value    ${resp.json()['form']}    bulkan
    Dictionary Should Contain Value    ${resp.json()['form']}    evcimen

Get Request With Redirection
    [Tags]    get
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Get Request    httpbin    /redirect/1
    Should Be Equal As Strings    ${resp.status_code}    200
    ${resp}=    Get Request    httpbin    /redirect/1    allow_redirects=${true}
    Should Be Equal As Strings    ${resp.status_code}    200

Get Request Without Redirection
    [Tags]    get
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Get Request    httpbin    /redirect/1    allow_redirects=${false}
    ${status}=    Convert To String    ${resp.status_code}
    Should Start With    ${status}    30

Options Request With Redirection
    [Tags]    options
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Options Request    httpbin    /redirect/1
    Should Be Equal As Strings    ${resp.status_code}    200
    ${resp}=    Options Request    httpbin    /redirect/1    allow_redirects=${true}
    Should Be Equal As Strings    ${resp.status_code}    200

Head Request With Redirection
    [Tags]    head
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Head Request    httpbin    /redirect/1    allow_redirects=${true}
    Should Be Equal As Strings    ${resp.status_code}    200

Head Request Without Redirection
    [Tags]    head
    Create Session    httpbin    http://httpbin.org
    ${resp}=    Head Request    httpbin    /redirect/1
    ${status}=    Convert To String    ${resp.status_code}
    Should Start With    ${status}    30
    ${resp}=    Head Request    httpbin    /redirect/1    allow_redirects=${false}
    ${status}=    Convert To String    ${resp.status_code}
    Should Start With    ${status}    30

Post Request With Redirection
    [Tags]    post
    Create Session    jigsaw    http://jigsaw.w3.org
    ${resp}=    Post Request    jigsaw    /HTTP/300/302.html
    Should Be Equal As Strings    ${resp.status_code}    200
    ${resp}=    Post Request    jigsaw    /HTTP/300/302.html    allow_redirects=${true}
    Should Be Equal As Strings    ${resp.status_code}    200

Post Request Without Redirection
    [Tags]    post
    Create Session    jigsaw    http://jigsaw.w3.org
    ${resp}=    Post Request    jigsaw    /HTTP/300/302.html    allow_redirects=${false}
    ${status}=    Convert To String    ${resp.status_code}
    Should Start With    ${status}    30

Put Request With Redirection
    [Tags]    put
    Create Session    jigsaw    http://jigsaw.w3.org
    ${resp}=    Put Request    jigsaw    /HTTP/300/302.html
    Should Be Equal As Strings    ${resp.status_code}    200
    ${resp}=    Put Request    jigsaw    /HTTP/300/302.html    allow_redirects=${true}
    Should Be Equal As Strings    ${resp.status_code}    200

Put Request Without Redirection
    [Tags]    put
    Create Session    jigsaw    http://jigsaw.w3.org
    ${resp}=    Put Request    jigsaw    /HTTP/300/302.html    allow_redirects=${false}
    ${status}=    Convert To String    ${resp.status_code}
    Should Start With    ${status}    30

Do Not Pretty Print a JSON object
    [Tags]    json
    Comment    Define json variable.
    ${var}=    Create Dictionary    key_one    true    key_two    this is a test string
    ${resp}=    Get Request    httpbin    /get    params=${var}
    Set Suite Variable    ${resp}
    Should Be Equal As Strings    ${resp.status_code}    200
    Log    ${resp.content}
    ${jsondata}=    To Json    ${resp.content}
    Log    ${jsondata['args']}
    Should Be Equal As Strings    ${jsondata['args']}    ${var}

Pretty Print a JSON object
    [Tags]    json
    Comment    Define json variable.
    Log    ${resp}
    ${output}=    To Json    ${resp.content}    pretty_print=True
    Log    ${output}
    Should Contain    ${output}    "key_one": "true"
    Should Contain    ${output}    "key_two": "this is a test string"
    Should Not Contain    ${output}    {u'key_two': u'this is a test string', u'key_one': u'true'}

Set Pretty Print to non-Boolean value
    [Tags]    json
    Comment    Define json variable.
    Log    ${resp}
    ${output}=    To Json    ${resp.content}    pretty_print="Hello"
    Log    ${output}
    Should Contain    ${output}    "key_one": "true"
    Should Contain    ${output}    "key_two": "this is a test string"
    Should Not Contain    ${output}    {u'key_two': u'this is a test string', u'key_one': u'true'}
