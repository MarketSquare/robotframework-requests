*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

*** Test Cases ***
Get Request And Fail On 404 Error Using Keyword
    [Tags]  get  fail
    Create Session  google  http://www.google.com
    Run Keyword And Expect Error  HTTPError: 404*   Get Request And Fail On Error  google  /404

Get Request And Fail On 500 Error Using Keyword
    [Tags]  get  fail
    Create Session  httpstat  http://httpstat.us
    Run Keyword And Expect Error  HTTPError: 500*   Get Request And Fail On Error  httpstat  /500

Get Request Without Failing On 404 Error Using Parameter
    [Tags]  get  fail
    Create Session  google  http://www.google.com
    ${resp}=  Get Request  google  /404  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Get Request And Fail On 500 Error Using Parameter
    [Tags]  get  fail
    Create Session  httpstat  http://httpstat.us
    Run Keyword And Expect Error  HTTPError: 500*   Get Request  httpstat  /500  fail_on_error=${True}
