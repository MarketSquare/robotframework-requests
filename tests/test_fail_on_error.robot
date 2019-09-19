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

Put Request Without Failing On 404 Error Using Parameter
    [Tags]  put  fail
    ${resp}=  Put Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Put Request And Fail On 500 Error Using Parameter
    [Tags]  put  fail
    Run Keyword And Expect Error  HTTPError: 500*   Put Request  httpstat  /500  ${Empty}  fail_on_error=${True}

Delete Request Without Failing On 404 Error Using Parameter
    [Tags]  delete  fail
    ${resp}=  Delete Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Delete Request And Fail On 500 Error Using Parameter
    [Tags]  delete  fail
    Run Keyword And Expect Error  HTTPError: 500*   Delete Request  httpstat  /500  ${Empty}  fail_on_error=${True}

Options Request Without Failing On 404 Error Using Parameter
    [Tags]  options  fail
    ${resp}=  Options Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Options Request And Fail On 500 Error Using Parameter
    [Tags]  options  fail
    Run Keyword And Expect Error  HTTPError: 500*   Options Request  httpstat  /500  ${Empty}  fail_on_error=${True}

Patch Request Without Failing On 404 Error Using Parameter
    [Tags]  patch  fail
    ${resp}=  Patch Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Patch Request And Fail On 500 Error Using Parameter
    [Tags]  patch  fail
    Run Keyword And Expect Error  HTTPError: 500*   Patch Request  httpstat  /500  ${Empty}  fail_on_error=${True}

Head Request Without Failing On 404 Error Using Parameter
    [Tags]  head  fail
    ${resp}=  Head Request  google  /404    ${Empty}  fail_on_error=${False}
    Should Be Equal As Strings  ${resp.status_code}  404

Head Request And Fail On 500 Error Using Parameter
    [Tags]  head  fail
    Run Keyword And Expect Error  HTTPError: 500*   Head Request  httpstat  /500  ${Empty}  fail_on_error=${True}
