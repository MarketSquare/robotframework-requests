*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

*** Test Cases ***
Get Request And Fail On 404 Error
    [Tags]  get  fail
    Create Session  google  http://www.google.com
    Run Keyword And Expect Error  HTTPError: 404*   Get Request And Fail On Error  google  /404

Get Request And Fail On 500 Error
    [Tags]  get  fail
    Create Session  httpstat  http://httpstat.us
    Run Keyword And Expect Error  HTTPError: 500*   Get Request And Fail On Error  httpstat  /500
