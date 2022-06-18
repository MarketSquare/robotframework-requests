*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Library  OperatingSystem
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Variables ***
${JSON_DATA}  '{"file":{"path":"/logo1.png"},"token":"some-valid-oauth-token"}'

*** Test Cases ***
Delete Request With Data
    ${headers}=  Create Dictionary  Content-Type=application/json
    ${resp}=   DELETE On Session  ${GLOBAL_SESSION}   /anything   data=${JSON_DATA}   headers=${headers}
    Should Be Equal As Strings    ${resp.json()}[method]  DELETE

