*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Setup  Run Keywords  Create Session  google  http://www.google.com  AND
...          Create Session  httpstat  http://httpstat.us

*** Test Cases ***
# TODO in current version i decided not to introduce new keywords
#Get Request And Fail On 404 Error Using Keyword
#    [Tags]  get  fail
#    Run Keyword And Expect Error  HTTPError: 404*   Get Request And Fail On Error  google  /404

#Get Request And Fail On 500 Error Using Keyword
#    [Tags]  get  fail
#    Run Keyword And Expect Error  HTTPError: 500*   Get Request And Fail On Error  httpstat  /500

Get Request Without Failing On 404 Error Using Parameter
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Get Request And Fail On 500 Error Using Parameter
    [Tags]  get  fail
    Run Keyword And Expect Error  HTTPError: 500*   Get Request  httpstat  /500  fail_on_error=${True}

#Post Request And Fail On 404 Error Using Keyword
#    [Tags]  post  fail
#    Run Keyword And Expect Error  HTTPError: 404*   Post Request And Fail On Error  google  /404

Post Request Without Failing On 404 Error Using Parameter
    [Tags]  post  fail
    ${resp}=  Post Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Post Request And Fail On 500 Error Using Parameter
    [Tags]  post  fail
    Run Keyword And Expect Error  HTTPError: 500*   Post Request  httpstat  /500  ${Empty}  fail_on_error=${True}
