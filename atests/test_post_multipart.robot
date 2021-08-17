*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***

Test Post On Session Multipart
    ${file_1}=  Get File For Streaming Upload  atests/randombytes.bin
    ${file_2}=  Get File For Streaming Upload  atests/randombytes.bin
    ${files}=   Create Dictionary  randombytes1  ${file_1}  randombytes2  ${file_2}

    ${resp}=    POST On Session  ${GLOBAL_SESSION}   /anything  files=${files}

    Should Contain  ${resp.json()}[headers][Content-Type]  multipart/form-data; boundary=
    Should Contain  ${resp.json()}[headers][Content-Length]  480
    Should Contain  ${resp.json()}[files]  randombytes1
    Should Contain  ${resp.json()}[files]  randombytes2
