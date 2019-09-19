*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py  fail_on_error=True

Suite Setup  Run Keywords  Create Session  google  http://www.google.com  AND
...          Create Session  httpstat  http://httpstat.us

*** Test Cases ***
Get Request Wihtout Failing On Error Overriding Import Settings
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Get Request And Fail On Error With Import Settings
    [Tags]  get  fail
    Run Keyword And Expect Error  HTTPError: 500*   Get Request  httpstat  /500

Get Request And Fail On Error With Import Settings And Overriding
    [Tags]  get  fail
    Run Keyword And Expect Error  HTTPError: 500*   Get Request  httpstat  /500  fail_on_error=${True}
