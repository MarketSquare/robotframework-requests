*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Setup  Run Keywords  Create Session  google  http://www.google.com  AND
...          Create Session  httpbin  https://httpbin.org/

*** Test Cases ***
Get Request And Fail On Status Without Message
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404
    Run Keyword And Expect Error  404 != 201  Status Should Be  ${resp}  201

Get Request And Not Fail On Status Without Message
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404
    Status Should Be  ${resp}  404

Get Request With Status Should Be OK
    [Tags]  get  fail
    ${resp}=  Get Request  google  /
    Status Should Be OK  ${resp}

Get Request With Status Should Be KO
    [Tags]  get  fail
    ${resp}=  Get Request  httpbin  get/201
    Status Should Be OK  ${resp}
