*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Library  OperatingSystem
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Post Request With XML File
    [Tags]  post
    ${file_data}=  Get File  ${CURDIR}${/}test.xml
    ${files}=  Create Dictionary  xml=${file_data}
    ${headers}=  Create Dictionary  Authorization=testing-token
    Log  ${headers}
    ${resp}=  POST On Session   ${GLOBAL_SESSION}  /anything  files=${files}  headers=${headers}

    Log  ${resp.json()}

    Set Test Variable  ${req_headers}  ${resp.json()['headers']}

    Dictionary Should Contain Key  ${req_headers}  Authorization
