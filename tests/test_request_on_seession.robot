*** Settings ***
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request On Existing Session
    [Tags]  get
    ${resp}=            Get On Session  ${SESSION}  /anything
    Status Should Be    OK  ${resp}

Get Request On Existing Session With Parameters
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            Get On Session  ${SESSION}  /anything  ${params}
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]

Get Request On Existing Session With Named Parameters
    [Tags]  get
    ${params}=          Create Dictionary   param1=1  param2=2
    ${resp}=            Get On Session  params=${params}  alias=${SESSION}  url=/anything
    Status Should Be    OK  ${resp}
    Dictionaries Should Be Equal  ${params}  ${resp.json()}[args]
