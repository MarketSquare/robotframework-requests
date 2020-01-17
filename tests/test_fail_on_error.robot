*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Setup  Run Keywords  Create Session  google  http://www.google.com  AND
...          Create Session  httpstat  http://httpstat.us/

*** Test Cases ***
Get Request And Fail On Status Without Message
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404
    Run Keyword And Expect Error  404 != 201  Status Should Be  201  ${resp}

Get Request And Not Fail On Status Without Message
    [Tags]  get  fail
    ${resp}=  Get Request  google  /404
    Status Should Be  404  ${resp}

#Get Request With Status Should Be OK
    #[Tags]  get  fail
    #${resp}=  Get Request  google  /
    # TODO name is misleading now
    #Status Should Be OK  ${resp}

#Get Request With Status Should Be KO
#    [Tags]  get  fail
#    ${resp}=  Get Request  httpstat  500
     # TODO name is misleading now
#    Run Keyword And Expect Error  HTTPError: 500*  Status Should Be OK  ${resp}

Get Request And Expect A Named Status Code
    [Tags]  get  fail
    ${resp}=  Get Request  httpstat  418
    Status Should Be  i am a teapot  ${resp}

Get Request And Expect An Invalid Named Status
    [Tags]  get  fail
    ${resp}=  Get Request  httpstat  418
    Run Keyword And Expect Error    UnknownStatusError: i am an alien    Status Should Be  i am an alien  ${resp}
