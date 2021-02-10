*** Settings ***
Library   RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Test On Session Keyword With Verify As Parameter

    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /  verify=${False}
    Status Should Be  OK  ${resp}

Test On Session Keyword With None Cookies As Parameter

    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /  cookies=${None}
    Status Should Be  OK  ${resp}

Test On Session Keyword With Cookies As Parameter

    ${resp}=  GET On Session  ${GLOBAL_SESSION}  /  cookies=${False}
    Status Should Be  OK  ${resp}
