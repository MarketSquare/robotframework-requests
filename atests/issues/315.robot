*** Settings ***
Library   RequestsLibrary
Resource  ../res_setup.robot

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
