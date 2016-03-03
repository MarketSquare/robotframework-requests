*** Settings ***
Library  Collections
Library  String
Library  ../../src/RequestsLibrary/RequestsKeywords.py
Library  OperatingSystem
Suite Teardown  Delete All Sessions

*** Variables ***
${JSON_DATA}  '{"file":{"path":"/logo1.png"},"token":"some-valid-oauth-token"}'

*** Test Cases ***
Delete Request With Data
    Create Session   httpbin   http://httpbin.org
    &{headers}=  Create Dictionary  Content-Type=application/json
    ${resp}=   Delete Request   httpbin   /delete   data=${JSON_DATA}   headers=${headers}
    ${jsondata}=   To Json   ${resp.content}
