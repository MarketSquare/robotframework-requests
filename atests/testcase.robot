*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Library  OperatingSystem
Library  customAuthenticator.py
Library  base64Decode.py
Resource  res_setup.robot

*** Test Cases ***

Post Request With No Data
    [Tags]  post
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST

Put Request With No Data
    [Tags]  put
    ${resp}=  PUT On Session  ${GLOBAL_SESSION}  /anything
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   PUT

Post With Unicode Data
    [Tags]  post
    ${data}=  Create Dictionary  name=度假村
    ${headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    Dictionary Should Contain Value  ${resp.json()['form']}  度假村

Post Request With Unicode Data
    [Tags]  post
    ${data}=  Create Dictionary  name=度假村
    ${headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    Dictionary Should Contain Value  ${resp.json()['form']}  度假村

Post Request With Binary Data in Dictionary
    [Tags]  post
    ${file_data}=  Get Binary File  ${CURDIR}${/}data.json
    ${data}=  Create Dictionary  name=${file_data.strip()}
    ${headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    Should Contain  ${resp.json()['form']['name']}  \u5ea6\u5047\u6751

Post Request With Binary Data
    [Tags]  post
    ${data}=  Get Binary File  ${CURDIR}${/}data.json
    ${headers}=  Create Dictionary  Content-Type=application/x-www-form-urlencoded
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    ${value}=  evaluate  list(${resp.json()['form']}.keys())[0]
    Should Contain  ${value}  度假村

Post Request With Arbitrary Binary Data
    [Tags]  post
    ${data}=  Get Binary File  ${CURDIR}${/}randombytes.bin
    &{headers}=  Create Dictionary  Content-Type=application/octet-stream   Accept=application/octet-stream
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  data=${data}  headers=&{headers}
    ${receivedData}=  Base64 Decode Data  ${resp.json()['data']}
    Should Be Equal  ${receivedData}  ${data}

Post Request With File
    [Tags]  post
    ${file_data}=  Get Binary File  ${CURDIR}${/}data.json
    ${files}=  Create Dictionary  file=${file_data}
    ${resp}=  POST On Session  ${GLOBAL_SESSION}  /anything  files=${files}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings     ${resp.json()['method']}   POST
    ${file}=  Set Variable  ${{dict(${resp.json()['files']['file']})}}
    Dictionary Should Contain Key  ${file}  one
    Dictionary Should Contain Key  ${file}  two

Post Request With Data and File
    [Tags]    post
    &{data}=    Create Dictionary    name=mallikarjunarao    surname=kosuri
    Create File    foobar.txt    content=foobar
    ${file_data}=    Get File    foobar.txt
    &{files}=    Create Dictionary    file=${file_data}
    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    files=${files}    data=${data}
    Should Be Equal As Strings    ${resp.status_code}    200
