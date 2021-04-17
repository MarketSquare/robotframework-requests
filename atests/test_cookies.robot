*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***

Test Cookies Passed In Request
    ${cookies}=  Create Dictionary  a=1 b=2
    Create Session  cookies-session  ${HTTP_LOCAL_SERVER}
    ${resp}=  GET On Session  cookies-session  /anything  cookies=${cookies}
    Should Be Equal As Strings  ${resp.json()}[headers][Cookie]  a=1 b=2

Test Default Cookies Passed In Session
    ${cookies}=  Create Dictionary  a=1 b=2
    Create Session  cookies-session  ${HTTP_LOCAL_SERVER}  cookies=${cookies}
    ${resp}=  GET On Session  cookies-session  /anything
    Should Be Equal As Strings  ${resp.json()}[headers][Cookie]  a=1 b=2

Test Default Cookies Passed In Session Override
    ${cookies}=  Create Dictionary  a=1 b=2
    ${override}=  Create Dictionary  a=3 b=4
    Create Session  cookies-session  ${HTTP_LOCAL_SERVER}  cookies=${cookies}
    ${resp}=  GET On Session  cookies-session  /anything  cookies=${override}
    Should Be Equal As Strings  ${resp.json()}[headers][Cookie]  a=3 b=4
