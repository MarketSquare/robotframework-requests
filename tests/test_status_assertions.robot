*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Setup  Run Keywords  Create Session  google  http://www.google.com  AND
...          Create Session  httpstat  http://httpstat.us/

*** Test Cases ***

Request And Status Should Be Different
    [Tags]  get  status
    ${resp}=  Get Request  google  /404
    Run Keyword And Expect Error  Url: http://www.google.com/404 Expected status: 404 != 201  Status Should Be  201  ${resp}

Request And Status Should Be Equal
    [Tags]  get  status
    ${resp}=  Get Request  google  /404
    Status Should Be  404  ${resp}

Request And Status Should Be A Named Status Code
    [Tags]  get  status
    ${resp}=  Get Request  httpstat  418
    Status Should Be  i am a teapot  ${resp}

Request And Status Should Be An Invalid Named Status
    [Tags]  get  status
    ${resp}=  Get Request  httpstat  418
    Run Keyword And Expect Error    UnknownStatusError: i am an alien    Status Should Be  i am an alien  ${resp}

Invalid Response
    [Tags]  get  status
    Run Keyword And Expect Error  InvalidResponse: this-is-not-a-request*
    ...  Status Should Be  123   this-is-not-a-request

Request And Status Should Be With A Message
    [Tags]  get  status
    ${resp}=  Get Request  httpstat  418
    Run Keyword And Expect Error  He should be a teapot! Url: http://httpstat.us//418 Expected status: 418 != 200
    ...   Status Should Be  OK  ${resp}  He should be a teapot!

Request Should Be Successful
    [Tags]  get  status
    ${resp}=  Get Request  google  /
    Request Should Be Successful  ${resp}

Request Should Not Be Successful
    [Tags]  get  status
    ${resp}=  Get Request  httpstat  500
    Run Keyword And Expect Error  HTTPError: 500*  Request Should Be Successful  ${resp}
