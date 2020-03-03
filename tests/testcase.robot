*** Settings ***
Library  Collections
Library  String
Library  ../src/RequestsLibrary/RequestsKeywords.py
Library  OperatingSystem
Library  customAuthenticator.py
Resource  res_setup.robot

Test Setup      Setup Test Session
Test Teardown   Teardown Test Session
Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Variables ***
${test_session}     local test session created in setup

*** Test Cases ***
Get Requests
    [Tags]  get  skip
    Create Session  google  http://www.google.com
    Create Session  github  https://api.github.com   verify=${CURDIR}${/}cacert.pem
    ${resp}=  Get Request  google  /
    Should Be Equal As Strings  ${resp.status_code}  200
    ${resp}=  Get Request  github  /users/bulkan
    Should Be Equal As Strings  ${resp.status_code}  200
    Dictionary Should Contain Value  ${resp.json()}  Bulkan Evcimen

Get Requests with Url Parameters
    [Tags]  get
    ${params}=   Create Dictionary   key=value     key2=value2
    ${resp}=     Get Request  ${test_session}  /anything    params=${params}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal As Strings     ${jsondata['method']}   GET
    Should Be Equal     ${jsondata['args']}     ${params}

Get Requests with Json Data
    [Tags]  get
    ${data}=    Create Dictionary   latitude=30.496346  longitude=-87.640356
    ${resp}=     Get Request  ${test_session}  /anything    json=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal As Strings     ${jsondata['method']}   GET
    Should Be Equal     ${jsondata['json']}     ${data}

Get HTTPS & Verify Cert
    [Tags]  get     get-cert
    Create Session    httpbin    https://httpbin.org   verify=True
    ${resp}=  Get Request  httpbin  /get
    Should Be Equal As Strings  ${resp.status_code}  200

Get HTTPS & Verify Cert with a CA bundle
    [Tags]  get     get-cert
    Create Session    httpbin    https://httpbin.org   verify=${CURDIR}${/}cacert.pem
    ${resp}=  Get Request  httpbin  /get
    Should Be Equal As Strings  ${resp.status_code}  200

Get HTTPS with Client Side Certificates
    [Tags]  get     get-cert
    @{client_certs}=    Create List     ${CURDIR}${/}clientcert.pem     ${CURDIR}${/}clientkey.pem
    Create Client Cert Session  crtsession  https://server.cryptomix.com/secure     client_certs=@{client_certs}
    ${resp}=    Get Request     crtsession  /
    Should Be Equal As Strings  ${resp.status_code}     200

Get With Auth
    [Tags]  get     get-cert
    ${auth}=  Create List  user   passwd
    Create Session    httpbin    https://httpbin.org     auth=${auth}   verify=${CURDIR}${/}cacert.pem
    ${resp}=  Get Request  httpbin  /basic-auth/user/passwd
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings  ${resp.json()['authenticated']}  True

Get With Custom Auth
    [Tags]  get
    ${auth}=    Get Custom Auth    user   passwd
    Create Custom Session    httpbin    https://httpbin.org     auth=${auth}   verify=${CURDIR}${/}cacert.pem
    ${resp}=  Get Request  httpbin  /basic-auth/user/passwd
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings  ${resp.json()['authenticated']}  True

Get With Digest Auth
    [Tags]    get   get-cert
    ${auth}=    Create List    user    pass
    Create Digest Session    httpbin    https://httpbin.org    auth=${auth}    debug=3   verify=${CURDIR}${/}cacert.pem
    ${resp}=    Get Request    httpbin    /digest-auth/auth/user/pass
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Post Request With URL Params
    [Tags]  post
    ${params}=   Create Dictionary   key=value     key2=value2
    ${resp}=  Post Request  ${test_session}  /anything		params=${params}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST

Post Requests with Json Data
    [Tags]  post
    ${data}=    Create Dictionary   latitude=30.496346  longitude=-87.640356
    ${resp}=     Post Request  ${test_session}  /anything    json=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal As Strings     ${jsondata['method']}   POST
    Should Be Equal     ${jsondata['json']}     ${data}

Put Requests with Json Data
    [Tags]  put
    ${data}=    Create Dictionary   latitude=30.496346  longitude=-87.640356
    ${resp}=     Put Request  ${test_session}  /anything    json=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal As Strings     ${jsondata['method']}   PUT
    Should Be Equal     ${jsondata['json']}     ${data}

Post Request With No Data
    [Tags]  post
    ${resp}=  Post Request  ${test_session}  /anything
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST

Put Request With No Data
    [Tags]  put
    ${resp}=  Put Request  ${test_session}  /anything
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   PUT

Post Request With No Dictionary
    [Tags]  post
    ${data}=  Set Variable  some content
    ${resp}=  Post Request  ${test_session}  /anything  data=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    Should Contain  ${resp.text}  ${data}

Put Request With URL Params
    [Tags]  put
    Create Session  httpbin  http://httpbin.org
    &{params}=   Create Dictionary   key=value     key2=value2
    ${resp}=  Put Request  httpbin  /put  params=${params}
    Should Be Equal As Strings  ${resp.status_code}  200

Put Request With No Dictionary
    [Tags]  put
    Create Session  httpbin  http://httpbin.org
    Set Test Variable  ${data}  some content
    ${resp}=  Put Request  httpbin  /put  data=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Contain  ${resp.text}  ${data}

Post Requests
    [Tags]  post
    Create Session  httpbin  http://httpbin.org
    &{data}=  Create Dictionary  name=bulkan  surname=evcimen
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=${headers}
    Dictionary Should Contain Value  ${resp.json()['form']}  bulkan
    Dictionary Should Contain Value  ${resp.json()['form']}  evcimen

Post With Unicode Data
    [Tags]  post
    Create Session  httpbin  http://httpbin.org    debug=3
    &{data}=  Create Dictionary  name=度假村
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=${headers}
    Dictionary Should Contain Value  ${resp.json()['form']}  度假村

Post Request With Unicode Data
    [Tags]  post
    Create Session  httpbin  http://httpbin.org    debug=3
    &{data}=  Create Dictionary  name=度假村
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=${headers}
    Dictionary Should Contain Value  ${resp.json()['form']}  度假村

Post Request With Binary Data in Dictionary
    [Tags]  post
    Create Session  httpbin  http://httpbin.org    debug=3
    ${file_data}=  Get Binary File  ${CURDIR}${/}data.json
    &{data}=  Create Dictionary  name=${file_data.strip()}
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=${headers}
    Log  ${resp.json()['form']}
    Should Contain  ${resp.json()['form']['name']}  \u5ea6\u5047\u6751

Post Request With Binary Data
    [Tags]  post
    Create Session  httpbin  http://httpbin.org    debug=3
    ${data}=  Get Binary File  ${CURDIR}${/}data.json
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=${headers}
    Log  ${resp.json()['form']}
    ${value}=  evaluate  list(${resp.json()['form']}.keys())[0]
    Should Contain  ${value}  度假村

Post Request With Arbitrary Binary Data
    [Tags]  post
    Create Session  httpbin  http://httpbin.org    debug=3
    ${data}=  Get Binary File  ${CURDIR}${/}randombytes.bin
    &{headers}=  Create Dictionary  Content-Type=application/octet-stream   Accept=application/octet-stream
    ${resp}=  Post Request  httpbin  /post  data=${data}  headers=&{headers}
    # TODO Compare binaries. Content is json with base64 encoded data
    Log    "Success"

Post Request With File
    [Tags]  post
    Create Session  httpbin  http://httpbin.org
    ${file_data}=  Get Binary File  ${CURDIR}${/}data.json
    &{files}=  Create Dictionary  file=${file_data}
    ${resp}=  Post Request  httpbin  /post  files=${files}
    ${file}=  To Json  ${resp.json()['files']['file']}
    Dictionary Should Contain Key  ${file}  one
    Dictionary Should Contain Key  ${file}  two

Post Request With Data and File
    [Tags]    post
    Create Session    httpbin    http://httpbin.org
    &{data}=    Create Dictionary    name=mallikarjunarao    surname=kosuri
    Create File    foobar.txt    content=foobar
    ${file_data}=    Get File    foobar.txt
    &{files}=    Create Dictionary    file=${file_data}
    ${resp}=    Post Request    httpbin    /post    files=${files}    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    200

Put Requests
    [Tags]  put
    Create Session  httpbin  http://httpbin.org
    &{data}=  Create Dictionary  name=bulkan  surname=evcimen
    &{headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  Put Request  httpbin  /put  data=${data}  headers=${headers}
    Dictionary Should Contain Value  ${resp.json()['form']}  bulkan
    Dictionary Should Contain Value  ${resp.json()['form']}  evcimen

Head Request
    [Tags]  head
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Head Request  httpbin  /headers
    Should Be Equal As Strings  ${resp.status_code}  200

Options Request
    [Tags]  options
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Options Request  httpbin  /headers
    Should Be Equal As Strings  ${resp.status_code}  200
    Dictionary Should Contain Key  ${resp.headers}  allow

Delete Request With URL Params
    [Tags]  delete
    Create Session  httpbin  http://httpbin.org
    &{params}=   Create Dictionary   key=value     key2=value2
    ${resp}=  Delete Request  httpbin  /delete		${params}
    Should Be Equal As Strings  ${resp.status_code}  200

Delete Request With No Data
    [Tags]  delete
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Delete Request  httpbin  /delete
    Should Be Equal As Strings  ${resp.status_code}  200

Delete Request With Data
    [Tags]  delete
    Create Session  httpbin  http://httpbin.org    debug=3
    &{data}=  Create Dictionary  name=bulkan  surname=evcimen
    ${resp}=  Delete Request  httpbin  /delete  data=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    Log  ${resp.content}
    Comment  Dictionary Should Contain Value  ${resp.json()['data']}  bulkan
    Comment  Dictionary Should Contain Value  ${resp.json()['data']}  evcimen

Delete Requests with Json Data
    [Tags]  delete
    Create Session  httpbin     http://httpbin.org
    &{data}=    Create Dictionary   latitude=30.496346  longitude=-87.640356
    ${resp}=     Delete Request  httpbin  /delete    json=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal     ${jsondata['json']}     ${data}

Patch Requests
    [Tags]    patch
    Create Session    httpbin    http://httpbin.org
    &{data}=    Create Dictionary    name=bulkan    surname=evcimen
    &{headers}=    Create Dictionary    Content-Type=application/x-www-form-urlencoded
    ${resp}=    Patch Request    httpbin    /patch    data=${data}    headers=${headers}
    Dictionary Should Contain Value    ${resp.json()['form']}    bulkan
    Dictionary Should Contain Value    ${resp.json()['form']}    evcimen

Patch Requests with Json Data
    [Tags]  patch
    Create Session  httpbin     http://httpbin.org
    &{data}=    Create Dictionary   latitude=30.496346  longitude=-87.640356
    ${resp}=     Patch Request  httpbin  /patch    json=${data}
    Should Be Equal As Strings  ${resp.status_code}  200
    ${jsondata}=  To Json  ${resp.content}
    Should Be Equal     ${jsondata['json']}     ${data}

Create a session and make sure it exists
    [Tags]    session
    Create Session     existing_session  ${HTTP_LOCAL_SERVER}
    ${exists}=         Session Exists    existing_session
    Should Be True     ${exists}

Verify a non existing session
    [Tags]    session
    ${exists}=          Session Exists    non-existing-session
    Should Not Be True  ${exists}
