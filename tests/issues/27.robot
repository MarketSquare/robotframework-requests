*** Settings ***
Library  Collections
Library  String
Library  ../../src/RequestsLibrary/RequestsKeywords.py
Library  OperatingSystem
Suite Teardown  Delete All Sessions

*** Test Cases ***
Post Request With XML File
    [Tags]  post
    Create Session  httpbin  http://httpbin.org

    ${file_data}=  Get File  ${CURDIR}${/}test.xml
    &{files}=  Create Dictionary  xml=${file_data}
    &{headers}=  Create Dictionary  Authorization=testing-token
    Log  ${headers}
    ${resp}=  Post Request  httpbin  /post  files=${files}  headers=${headers}

    Log  ${resp.json()}

    Set Test Variable  ${req_headers}  ${resp.json()['headers']}

    Dictionary Should Contain Key  ${req_headers}  Authorization
