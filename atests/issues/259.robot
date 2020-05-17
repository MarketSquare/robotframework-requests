*** Settings ***
Library   RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions


*** Test Cases ***
Post Content application/json With Empty Data Should Have No Body
    ${content-type}=  Create Dictionary  content-type  application/json
    ${resp}=  Post Request  ${GLOBAL_SESSION}  /anything  data=${EMPTY}  headers=${content-type}
    Should Be Empty  ${resp.json()['data']}

Post Content With Empty Data Should Have No Body
    ${resp}=  Post Request  ${GLOBAL_SESSION}  /anything  data=${EMPTY}
    Should Be Empty  ${resp.json()['data']}
